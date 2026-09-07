/* lab.js — the shared runtime for every experiment on this site.
 *
 * Three things it does, and nothing else:
 *   1. keeps your ElevenLabs keys in this browser's localStorage (several of them,
 *      named, switchable) — never on a server, never in this repository;
 *   2. calls exactly one host, https://api.elevenlabs.io, with your key in the
 *      xi-api-key header, and logs every call it makes;
 *   3. does the arithmetic the labs share: characters -> cost, alignment -> words
 *      -> cues -> SRT/VTT, results -> markdown you can paste back.
 *
 * It is deliberately small and readable, because the site's whole argument is
 * about where a credential goes: you should be able to check that claim by
 * reading this file, and by watching the network tab.
 */
(function () {
  'use strict';

  var API = 'https://api.elevenlabs.io/v1';
  var STORE = 'el.keys.v1';           // { active: <id>, items: [{ id, label, key }] }
  var LEGACY = 'elevenlabs-key';      // the vault bench's single-key slot
  var EL = (window.EL = {});

  EL.API = API;
  EL.RATES = {                        // $ per 1,000 characters, list, Sep 2026 — vendor docs
    eleven_v3: 0.10, eleven_multilingual_v2: 0.10, eleven_flash_v2_5: 0.05,
    eleven_turbo_v2_5: 0.05, eleven_flash_v2: 0.05, eleven_turbo_v2: 0.05
  };
  EL.LIMITS = { eleven_v3: 5000, eleven_multilingual_v2: 10000, eleven_flash_v2_5: 40000, eleven_turbo_v2_5: 40000 };
  EL.MODELS = [
    ['eleven_v3', 'eleven_v3 — most expressive, audio tags, 5,000 chars, $0.10/1k'],
    ['eleven_multilingual_v2', 'eleven_multilingual_v2 — stable long-form, 10,000 chars, $0.10/1k'],
    ['eleven_flash_v2_5', 'eleven_flash_v2_5 — fastest and cheapest, 40,000 chars, $0.05/1k'],
    ['eleven_turbo_v2_5', 'eleven_turbo_v2_5 — quality/latency balance, $0.05/1k']
  ];
  EL.SAMPLES = {
    'a vault scene': "This is the vault, opened read-only in the SG/Vault browser. The presenter app, the deck, the screenshots and the sources: four megabytes, encrypted before they left the author's machine.",
    'numbers': 'Fifty-three controls, a hundred and forty-four requirements, two thousand seven hundred and eighty-eight nodes, eleven thousand six hundred and ten edges — and a green gate with zero errors.',
    'names to test': 'sgit.ai, SG/Vault, SGraph, AIUC-1, SHA-256, llms.txt, OWASP, José Bota, VoiceDebrief, PT-BR, v0.1.29.',
    'the hacks we use today': 'sgit dot ai, A I U C one, S H A two five six, llms dot txt, version zero point one point twenty-nine.',
    'a v3 read': '[thoughtful] And here is the argument. A control is not a row in a list… it is what its edges say it is.'
  };
  EL.TAGS = ['[thoughtful]', '[whispers]', '[excited]', '[sighs]', '[laughs]', '[sarcastic]', '[pause]', '[slowly]', '…'];

  /* ------------------------------------------------------------- storage --- */

  function read() {
    var raw = null;
    try { raw = localStorage.getItem(STORE); } catch (e) { /* private mode */ }
    var box = { active: null, items: [] };
    if (raw) { try { box = JSON.parse(raw) || box; } catch (e) {} }
    if (!box.items.length) {                       // adopt the vault bench's key, once
      try {
        var old = localStorage.getItem(LEGACY);
        if (old) { box.items = [{ id: 'k1', label: 'imported', key: old }]; box.active = 'k1'; write(box); }
      } catch (e) {}
    }
    return box;
  }
  function write(box) {
    try { localStorage.setItem(STORE, JSON.stringify(box)); } catch (e) {}
    try { if (window.sg && sg.state) sg.state.set(LEGACY, EL.key() || ''); } catch (e) {}
  }

  EL.keys = {
    all: function () { return read().items; },
    activeId: function () { return read().active; },
    add: function (label, key) {
      var box = read();
      // Unique even when two keys are added in the same millisecond.
      var id, n = 0;
      do { id = 'k' + (Date.now() % 1e7) + (n ? '-' + n : ''); n++; }
      while (box.items.some(function (k) { return k.id === id; }));
      box.items.push({ id: id, label: label || ('key ' + (box.items.length + 1)), key: key });
      box.active = id; write(box); return id;
    },
    remove: function (id) {
      var box = read();
      box.items = box.items.filter(function (k) { return k.id !== id; });
      if (box.active === id) box.active = box.items.length ? box.items[0].id : null;
      write(box);
    },
    use: function (id) { var box = read(); box.active = id; write(box); },
    clear: function () {
      try { localStorage.removeItem(STORE); localStorage.removeItem(LEGACY); } catch (e) {}
      try { if (window.sg && sg.state) sg.state.remove(LEGACY); } catch (e) {}
    }
  };
  EL.key = function () {
    var box = read(), hit = box.items.filter(function (k) { return k.id === box.active; })[0];
    return hit ? hit.key : (box.items[0] ? box.items[0].key : '');
  };
  EL.hasKey = function () { return !!EL.key(); };

  /* ----------------------------------------------------------- the key bar --- */

  EL.mountKeyBar = function (host) {
    if (!host) return;
    function draw() {
      var box = read();
      var chips = box.items.map(function (k) {
        return '<span class="k' + (k.id === box.active ? ' active' : '') + '" data-id="' + k.id + '">' +
          esc(k.label) + ' <span class="dim">' + esc(mask(k.key)) + '</span> <x data-del="' + k.id + '" title="Forget this key">&times;</x></span>';
      }).join('');
      host.innerHTML =
        '<div class="ttl">Your key, in your browser</div>' +
        '<div class="keys">' + (chips || '<span class="dim small">No key stored on this device.</span>') + '</div>' +
        '<div class="row fill"><input type="password" id="el-key" placeholder="sk_…" autocomplete="off" spellcheck="false">' +
        '<input type="text" id="el-label" placeholder="label — e.g. tts-only, scoped" style="max-width:16rem">' +
        '<button id="el-add" style="flex:0 0 auto">Save on this device</button>' +
        '<button class="secondary" id="el-clear" style="flex:0 0 auto">Forget all</button></div>' +
        '<p>Stored in this browser&rsquo;s <code>localStorage</code> under <code>' + STORE + '</code> (and mirrored to ' +
        '<code>sg.state</code> when this page runs inside a vault app). It is sent to one host, <code>api.elevenlabs.io</code>, ' +
        'in the <code>xi-api-key</code> header, by calls you start. It is never sent here, never logged, and this site has no ' +
        'server to send it to. Keep several keys if you want to compare a scoped key against a full one.</p>' +
        '<p class="small" id="el-keystatus"></p>';
      host.querySelectorAll('.k').forEach(function (el) {
        el.addEventListener('click', function (ev) {
          var del = ev.target.getAttribute('data-del');
          if (del) { EL.keys.remove(del); draw(); EL.emit('keychange'); return; }
          EL.keys.use(el.getAttribute('data-id')); draw(); EL.emit('keychange');
        });
      });
      host.querySelector('#el-add').addEventListener('click', function () {
        var v = host.querySelector('#el-key').value.trim();
        if (!v) return;
        EL.keys.add(host.querySelector('#el-label').value.trim(), v);
        draw(); EL.emit('keychange');
      });
      host.querySelector('#el-clear').addEventListener('click', function () {
        EL.keys.clear(); draw(); EL.emit('keychange');
      });
    }
    draw();
  };
  function mask(k) { return k ? k.slice(0, 6) + '…' + k.slice(-4) : ''; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }
  EL.esc = esc;

  var listeners = {};
  EL.on = function (ev, fn) { (listeners[ev] = listeners[ev] || []).push(fn); };
  EL.emit = function (ev, arg) { (listeners[ev] || []).forEach(function (f) { try { f(arg); } catch (e) {} }); };

  /* ------------------------------------------------------------------ api --- */

  EL.log = function (msg) {
    var el = document.getElementById('log');
    if (!el) return;
    el.textContent = new Date().toISOString().slice(11, 19) + '  ' + msg + '\n' + el.textContent;
  };
  EL.status = function (id, msg, cls) {
    var el = typeof id === 'string' ? document.getElementById(id) : id;
    if (!el) return;
    el.textContent = msg; el.className = 'status' + (cls ? ' ' + cls : '');
  };

  /** One fetch, one host, your key. Returns { res, ms, requestId }. */
  EL.raw = async function (path, opts) {
    opts = opts || {};
    if (!EL.hasKey()) throw new Error('No key on this device — save one above first.');
    var headers = { 'xi-api-key': EL.key() };
    if (opts.json) { headers['content-type'] = 'application/json'; opts.body = JSON.stringify(opts.json); }
    var t0 = performance.now();
    var res = await fetch(API + path, { method: opts.method || 'GET', headers: headers, body: opts.body });
    var ms = Math.round(performance.now() - t0);
    var rid = res.headers.get('request-id') || res.headers.get('x-request-id') || '';
    EL.log((opts.method || 'GET') + ' ' + path.split('?')[0] + ' → ' + res.status + ' in ' + ms + ' ms' + (rid ? '  request-id ' + rid : ''));
    if (!res.ok) {
      var detail = '';
      try { detail = JSON.stringify((await res.json()).detail).slice(0, 400); } catch (e) {}
      var err = new Error('HTTP ' + res.status + ' ' + path.split('?')[0] + (detail ? ' — ' + detail : ''));
      err.status = res.status; err.detail = detail; err.ms = ms;
      throw err;
    }
    return { res: res, ms: ms, requestId: rid };
  };
  EL.get = async function (path) { var r = await EL.raw(path); return r.res.json(); };
  EL.post = async function (path, json) { var r = await EL.raw(path, { method: 'POST', json: json }); return r; };
  EL.postForm = async function (path, form) {
    if (!EL.hasKey()) throw new Error('No key on this device — save one above first.');
    var t0 = performance.now();
    var res = await fetch(API + path, { method: 'POST', headers: { 'xi-api-key': EL.key() }, body: form });
    var ms = Math.round(performance.now() - t0);
    EL.log('POST ' + path + ' → ' + res.status + ' in ' + ms + ' ms');
    if (!res.ok) { var d = ''; try { d = (await res.text()).slice(0, 400); } catch (e) {} throw new Error('HTTP ' + res.status + ' ' + d); }
    return { res: res, ms: ms };
  };

  /** The one call every speech lab makes. */
  EL.speak = async function (o) {
    var body = {
      text: o.text,
      model_id: o.model,
      voice_settings: {
        stability: num(o.stability, 0.5), similarity_boost: num(o.similarity, 0.75),
        style: num(o.style, 0), use_speaker_boost: o.boost !== false, speed: num(o.speed, 1)
      },
      apply_text_normalization: o.normalize || 'auto'
    };
    if (o.language) body.language_code = o.language;
    if (o.seed) body.seed = Number(o.seed);
    if (o.previousText) body.previous_text = o.previousText;
    if (o.nextText) body.next_text = o.nextText;
    if (o.dictId && o.dictVersion) body.pronunciation_dictionary_locators = [{ pronunciation_dictionary_id: o.dictId, version_id: o.dictVersion }];
    var withTs = o.timestamps !== false;
    var path = '/text-to-speech/' + encodeURIComponent(o.voice) + (withTs ? '/with-timestamps' : '') +
      '?output_format=' + encodeURIComponent(o.format || 'mp3_44100_128');
    var r = await EL.post(path, body);
    var blob, words = [], alignment = null;
    if (withTs) {
      var j = await r.res.json();
      alignment = j.alignment || j.normalized_alignment || null;
      blob = new Blob([b64(j.audio_base64)], { type: 'audio/mpeg' });
      words = EL.groupWords(alignment);
    } else blob = await r.res.blob();
    return {
      blob: blob, url: URL.createObjectURL(blob), words: words, alignment: alignment,
      ms: r.ms, requestId: r.requestId, bytes: blob.size,
      chars: o.text.length, cost: (o.text.length / 1000) * (EL.RATES[o.model] || 0.1)
    };
  };
  function num(v, d) { return v === undefined || v === null || v === '' || isNaN(+v) ? d : +v; }
  function b64(s) { var bin = atob(s), out = new Uint8Array(bin.length); for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i); return out; }

  /* ------------------------------------------------------------ arithmetic --- */

  /** Characters -> words. A word is a run of non-whitespace; its start is the
   *  first character's start and its end the last character's end. */
  EL.groupWords = function (al) {
    if (!al || !al.characters) return [];
    var out = [], cur = null;
    al.characters.forEach(function (ch, i) {
      var s = al.character_start_times_seconds[i], e = al.character_end_times_seconds[i];
      if (/\s/.test(ch)) { if (cur) { out.push(cur); cur = null; } return; }
      if (!cur) cur = { w: ch, s: s, e: e }; else { cur.w += ch; cur.e = e; }
    });
    if (cur) out.push(cur);
    return out;
  };
  /** Words -> cues. Ours, not the vendor's: break at maxChars, or a gap over
   *  gap seconds, or maxSecs of running time. */
  EL.buildCues = function (words, o) {
    o = o || {};
    var maxChars = o.maxChars || 84, gap = o.gap === undefined ? 0.6 : o.gap, maxSecs = o.maxSecs || 6;
    var cues = [], cue = null;
    words.forEach(function (w) {
      if (cue && ((cue.t + ' ' + w.w).length > maxChars || w.s - cue.e > gap || w.e - cue.s > maxSecs)) { cues.push(cue); cue = null; }
      cue = cue ? { s: cue.s, e: w.e, t: cue.t + ' ' + w.w } : { s: w.s, e: w.e, t: w.w };
    });
    if (cue) cues.push(cue);
    return cues;
  };
  EL.tc = function (t, comma) {
    var h = Math.floor(t / 3600), m = Math.floor((t % 3600) / 60), s = Math.floor(t % 60), ms = Math.round((t % 1) * 1000);
    return pad(h) + ':' + pad(m) + ':' + pad(s) + (comma ? ',' : '.') + String(ms).padStart(3, '0');
  };
  function pad(n) { return String(n).padStart(2, '0'); }
  EL.wrap2 = function (t, w) {
    w = w || 42;
    if (t.length <= w) return t;
    var i = t.lastIndexOf(' ', w);
    return i > 0 ? t.slice(0, i) + '\n' + t.slice(i + 1) : t;
  };
  EL.srt = function (cues, wrapAt) {
    return cues.map(function (c, i) {
      return (i + 1) + '\n' + EL.tc(c.s, true) + ' --> ' + EL.tc(c.e, true) + '\n' + EL.wrap2(c.t, wrapAt) + '\n';
    }).join('\n');
  };
  EL.vtt = function (cues, wrapAt) {
    return 'WEBVTT\n\n' + cues.map(function (c) {
      return EL.tc(c.s) + ' --> ' + EL.tc(c.e) + '\n' + EL.wrap2(c.t, wrapAt) + '\n';
    }).join('\n');
  };
  EL.money = function (n) { return '$' + n.toFixed(n < 0.1 ? 4 : 3); };
  EL.estimate = function (chars, model) { return (chars / 1000) * (EL.RATES[model] || 0.1); };

  /* ---------------------------------------------------------------- output --- */

  EL.karaoke = function (audio, box, words) {
    if (!audio || !box) return;
    audio.ontimeupdate = function () {
      if (!words || !words.length) return;
      var t = audio.currentTime;
      for (var i = 0; i < box.children.length; i++) {
        var el = box.children[i], w = words[+el.dataset.i];
        if (!w) continue;
        el.className = t >= w.e ? 'past' : (t >= w.s ? 'on' : '');
      }
    };
  };
  EL.renderWords = function (box, words) {
    box.innerHTML = '';
    words.forEach(function (x, i) {
      var s = document.createElement('span');
      s.textContent = x.w + ' '; s.dataset.i = i; s.title = x.s.toFixed(2) + '–' + x.e.toFixed(2) + ' s';
      box.appendChild(s);
    });
  };
  EL.download = function (name, data, type) {
    var blob = data instanceof Blob ? data : new Blob([data], { type: type || 'text/plain;charset=utf-8' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
  };
  EL.copy = async function (text, statusEl) {
    try { await navigator.clipboard.writeText(text); EL.status(statusEl, 'Copied.', 'ok'); }
    catch (e) { EL.status(statusEl, 'Clipboard refused — select the text and copy it by hand.', 'warn'); }
  };
  /** Results -> a markdown table, so a run can be pasted straight back into the
   *  vault (or into this repository) as evidence. */
  EL.toMarkdown = function (headers, rows, title) {
    var out = title ? ('### ' + title + '\n\n') : '';
    out += '| ' + headers.join(' | ') + ' |\n|' + headers.map(function () { return '---'; }).join('|') + '|\n';
    rows.forEach(function (r) { out += '| ' + r.map(function (c) { return String(c).replace(/\|/g, '\\|'); }).join(' | ') + ' |\n'; });
    out += '\nRun ' + new Date().toISOString() + ' from ' + location.host + ' — unverified by the site authors.\n';
    return out;
  };

  /* -------------------------------------------------------------- helpers --- */

  EL.fillModels = function (sel, only) {
    if (!sel) return;
    sel.innerHTML = EL.MODELS.filter(function (m) { return !only || only.indexOf(m[0]) >= 0; })
      .map(function (m) { return '<option value="' + m[0] + '">' + esc(m[1]) + '</option>'; }).join('');
  };
  EL.loadVoices = async function (sel, keep) {
    var j = await EL.get('/voices');
    var voices = (j.voices || []).sort(function (a, b) {
      return (a.category || '').localeCompare(b.category || '') || a.name.localeCompare(b.name);
    });
    if (sel) {
      var prev = keep ? sel.value : '';
      sel.innerHTML = voices.map(function (v) {
        var l = v.labels || {};
        return '<option value="' + esc(v.voice_id) + '">' + esc(v.name) + ' · ' + esc(v.category || '') +
          (l.accent ? ' · ' + esc(l.accent) : '') + (l.gender ? ' · ' + esc(l.gender) : '') + '</option>';
      }).join('');
      if (prev) sel.value = prev;
    }
    EL.voices = voices;
    return voices;
  };
  EL.sampleChips = function (host, textarea, after) {
    if (!host) return;
    Object.keys(EL.SAMPLES).forEach(function (k) {
      var s = document.createElement('span');
      s.textContent = k;
      s.onclick = function () { textarea.value = EL.SAMPLES[k]; if (after) after(); };
      host.appendChild(s);
    });
  };
  /** A magnitude bar for a table cell. One hue for every row — the length is the
   *  encoding, so colour is free to mean state instead of rank. `failed` is the
   *  only thing that recolours a bar, and it is always labelled as well. */
  EL.bar = function (value, max, failed, unit) {
    var pct = Math.max(2, Math.min(100, (value / (max || 1)) * 100));
    var label = value + (unit || '');
    return '<span class="bar' + (failed ? ' bad' : '') + '" title="' + label + '">' +
      '<i style="width:' + pct.toFixed(1) + '%"></i><b>' + label + '</b></span>';
  };
  /** One row of a request timeline: a bar placed by start offset, sized by duration. */
  EL.span = function (startMs, durMs, totalMs, failed, label) {
    var left = Math.max(0, (startMs / (totalMs || 1)) * 100);
    var w = Math.max(1.2, (durMs / (totalMs || 1)) * 100);
    return '<span class="bar timeline' + (failed ? ' bad' : '') + '" title="' + (label || (durMs + ' ms')) + '">' +
      '<i style="left:' + left.toFixed(2) + '%;width:' + w.toFixed(2) + '%"></i></span>';
  };

  /* ------------------------------------------------------------------ boot --- */

  document.addEventListener('DOMContentLoaded', function () {
    var nav = document.querySelector('nav.site'), btn = nav && nav.querySelector('.nav-toggle');
    if (btn) btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    EL.mountKeyBar(document.getElementById('keybar'));
    try { window.parent && window.parent !== window && window.parent.postMessage({ type: 'sg-app-ready' }, '*'); } catch (e) {}
  });
})();
