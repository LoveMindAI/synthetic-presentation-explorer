# Image construction

This release contains portable, scrubbed code rather than the private experiment orchestration system. No participant-derived personality text is included.

## Deterministic worked example

Install Pillow in your own Python environment, then from the repository root:

```sh
python code/compose.py --layers example_layers/S01 --output reconstructed_S01
```

The supplied S01 layers reconstruct all 16 illustrated S01 cells. Compare their decoded RGB hashes with `data/stimuli.json`. PNG and lossless WebP file hashes differ, while decoded pixels match. Only one worked identity's layers are included to limit download size; all 256 final images are included.

## Generation

`data/generation_prompts.json` contains initial clothing/background trial prompts, selected repair prompts, and the override map identifying the replacement source for each repaired layer. `generate_one.py` extracts the original image API request pattern into a standalone one-call utility. Dry-run is the default. `--go` uses the caller's `OPENROUTER_API_KEY` and can incur charges. No key is supplied, no calls run in the explorer, and no automatic retries occur. The reference must be supplied explicitly; repair prompts may expect an empty-room image rather than a portrait.

Historical model identifiers are `google/gemini-3-pro-image` and `openai/gpt-image-2.5-flare` for the balanced layer design. Endpoints and provider behavior may change. Generated outputs are stochastic; the utility is not a guarantee of regenerating identical pixels.

## Face locking before composition

`face_lock.py` contains the extracted alignment and face-lock mathematics from the construction pipeline. The input arrays are a canonical RGB source and its person mask, an edited RGB foreground and mask, and facial landmarks. Eye-center alignment uses a similarity transform; a feathered jaw/head boundary combines the canonical upper region with the aligned clothing. The inner face is explicitly overwritten with source pixels and made opaque. Final layers are composited with Pillow.

Person segmentation and landmarks in the source pipeline used Apple's Vision framework; `segment_person.swift` is provided. Reviewed face selection and per-identity boundary adjustments are not replaced by a claim that segmentation always succeeds. Final source layers, visual inspection, and decoded-pixel checks are distinct evidence.

## Limits

Original character briefs describe intended impressions, not validated personality scores. Some identities were subsequently recast, so those original briefs are labeled design-stage history, not exact final-character profiles. The initial editor assignment was balanced across categories; selected repairs are documented separately. Neither a deterministic pixel check nor model cue ratings establish human validity.
