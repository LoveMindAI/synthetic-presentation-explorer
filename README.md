# Synthetic presentation explorer

A fully synthetic illustrative dataset for controlled clothing and background changes in person perception: 16 fictional identities, four clothing categories, four background categories, 256 images.

**These are not PARSEL participants and are not the stimuli underlying the reported PARSEL results.** Sensitive PARSEL images, personality profiles, transcripts and raw request logs are excluded. Access to PARSEL material requires separate authorization. This illustrative matrix does not substitute for the manuscript's private stimulus sets or their experimental counts.

Open `index.html` in a browser, or serve this directory using `python -m http.server 8000`. The explorer has no external dependencies, analytics, API calls or external fonts.

- `matrix/`: all 256 lossless, metadata-stripped WebP images; decoded RGB pixels verified against the source PNGs.
- `data/stimuli.json`: file and decoded-pixel hashes, identity and condition coordinates.
- `data/generation_prompts.json`: initial layer prompts, selected repairs, and editor assignments.
- `data/original_authoring_briefs.json`: original design-stage intentions, not validated psychometric profiles; some identities were later recast.
- `data/presentation_briefs.json`: individual clothing and room instructions.
- `prompts/`: participant-free judgment templates with explicit scope notes.
- `code/`: extracted image-generation request, face-lock mathematics, segmentation source and final compositor.
- `example_layers/S01/`: a complete worked synthetic identity for exact final reconstruction.

No new human ratings accompany this bank. Face-core preservation does not validate realism, clothing cues, background cues, or psychological interpretations. Retained ambiguities: S03 evening clothing and S07 clutter.

The explorer is an explanatory companion, not a personality-inference service. Its images and artistic intentions are not evidence that facial appearance reveals true personality.
