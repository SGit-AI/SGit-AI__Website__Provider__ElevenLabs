#!/usr/bin/env node
// tts-timestamps.mjs "<text>" <voice_id> [basename] — one request to /with-timestamps, writes
// <basename>.wav (pcm_44100 → RIFF), <basename>.words.json and <basename>.srt.
// ELEVEN_MODEL, SPEED, ELEVEN_DICT (<id>:<version>), ELEVEN_SEED honoured. No dependencies.
import fs from 'node:fs';
const [, , text, voice, base = '/tmp/eleven-ts'] = process.argv;
if (!text || !voice) { console.error('usage: tts-timestamps.mjs "<text>" <voice_id> [basename]'); process.exit(2); }
const key = process.env.ELEVENLABS_API_KEY; if (!key) throw new Error('ELEVENLABS_API_KEY');
const body = { text, model_id: process.env.ELEVEN_MODEL || 'eleven_v3', voice_settings: { stability: 0.5, similarity_boost: 0.75, speed: Number(process.env.SPEED || 1) }, apply_text_normalization: 'auto' };
if (process.env.ELEVEN_DICT) { const [id, ver] = process.env.ELEVEN_DICT.split(':'); body.pronunciation_dictionary_locators = [{ pronunciation_dictionary_id: id, version_id: ver }]; }
if (process.env.ELEVEN_SEED) body.seed = Number(process.env.ELEVEN_SEED);
const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice}/with-timestamps?output_format=pcm_44100`, { method: 'POST', headers: { 'xi-api-key': key, 'content-type': 'application/json' }, body: JSON.stringify(body) });
if (!r.ok) { console.error('HTTP', r.status, await r.text()); process.exit(1); }
const j = await r.json();
const pcm = Buffer.from(j.audio_base64, 'base64');
const wav = Buffer.alloc(44); const sr = 44100;
wav.write('RIFF', 0); wav.writeUInt32LE(36 + pcm.length, 4); wav.write('WAVE', 8); wav.write('fmt ', 12); wav.writeUInt32LE(16, 16); wav.writeUInt16LE(1, 20); wav.writeUInt16LE(1, 22);
wav.writeUInt32LE(sr, 24); wav.writeUInt32LE(sr * 2, 28); wav.writeUInt16LE(2, 32); wav.writeUInt16LE(16, 34); wav.write('data', 36); wav.writeUInt32LE(pcm.length, 40);
fs.writeFileSync(`${base}.wav`, Buffer.concat([wav, pcm]));
// characters → words
const al = j.alignment; const words = []; let cur = null;
al.characters.forEach((ch, i) => { const s = al.character_start_times_seconds[i], e = al.character_end_times_seconds[i];
  if (/\s/.test(ch)) { if (cur) { words.push(cur); cur = null; } return; } cur = cur ? { w: cur.w + ch, s: cur.s, e } : { w: ch, s, e }; });
if (cur) words.push(cur);
fs.writeFileSync(`${base}.words.json`, JSON.stringify(words, null, 1));
// words → SRT (≤84 chars, gap > 0.6 s, ≤ 6 s)
const ts = (t) => `${String(Math.floor(t / 3600)).padStart(2, '0')}:${String(Math.floor(t % 3600 / 60)).padStart(2, '0')}:${String(Math.floor(t % 60)).padStart(2, '0')},${String(Math.round((t % 1) * 1000)).padStart(3, '0')}`;
const cues = []; let cue = null;
for (const w of words) { if (cue && ((cue.t + ' ' + w.w).length > 84 || w.s - cue.e > 0.6 || w.e - cue.s > 6)) { cues.push(cue); cue = null; } cue = cue ? { s: cue.s, e: w.e, t: cue.t + ' ' + w.w } : { s: w.s, e: w.e, t: w.w }; }
if (cue) cues.push(cue);
const wrap2 = (t) => { if (t.length <= 42) return t; const i = t.lastIndexOf(' ', 42); return i > 0 ? t.slice(0, i) + '\n' + t.slice(i + 1) : t; };
fs.writeFileSync(`${base}.srt`, cues.map((c, i) => `${i + 1}\n${ts(c.s)} --> ${ts(c.e)}\n${wrap2(c.t)}\n`).join('\n'));
console.log(`${base}.wav  ${(pcm.length / sr / 2).toFixed(2)} s · ${words.length} words · ${cues.length} cues · request-id ${r.headers.get('request-id') || '?'}`);
