---
title: Model A/B — latency, size and cost on one text
description: "Race eleven_v3, multilingual_v2, flash and turbo over the same text and voice: wall-clock latency, bytes returned, spoken duration and cost per model, with the results as a markdown table."
lead: "Four models, one text, one voice, several runs each. The vendor's model table tells you the price and the character limit; it cannot tell you what **your** text sounds like or how long **your** connection takes to get it."
order: 12
kind: experiment
family: choosing
app: models
endpoints: "POST /v1/text-to-speech/{id}/with-timestamps"
state_chips: [unrun]
toc: true
---

{{lab-header}}

{{app}}

## What this tests

The published differences between the models are price, character limit and a one-line character sketch {{claim:tts-prices}} {{claim:char-limits}}. The differences that decide a pipeline are:

- **Latency under your own network**, which is the number that determines whether a 16-scene render takes ten seconds or two minutes. Our only measurement is three samples of one model from one connection: 5.0–5.8 s {{claim:latency-5s}}. That is not a distribution, and this lab exists to replace it with one.
- **Spoken duration for identical text**, which changes how much script fits a 60-second cut. Two models reading the same words at the same nominal speed do not produce the same length.
- **Whether the expensive model is audibly better on this text.** Half the price is half the price; if flash is indistinguishable on your workload, that is the finding.

## Method

Same voice, same text, same speed, several runs per model — because one run per model times the weather, not the model. Runs are sequential, not parallel: parallel runs would measure the concurrency limit instead, which is [a different lab](/experiments/concurrency/) with a different failure mode {{claim:concurrency-unknown}}.

The cost estimate above the button is the whole spend, computed before anything is sent: characters × rate × runs × models.

## What to write down

Latency mean and spread per model, spoken duration per model, and — the part no table can give you — whether you could tell them apart with your eyes closed. The **Copy results as markdown** button produces a table with a timestamp; paste it into the repository that cares about the answer.

Our own projection says v3 costs about what the incumbent provider costs and flash costs half {{claim:projected-reel-costs}}. Whether the extra buys anything on a technical explainer is exactly the question this lab is for, and we have not answered it {{claim:labs-unrun}}.
