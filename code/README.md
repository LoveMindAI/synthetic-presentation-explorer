# Image construction

Use this code to inspect the image-construction method and reproduce one complete example. We extracted the relevant functions from the research pipeline and removed identifying information. Participant-derived personality text remains private.

[Explore the images](https://anonymous.4open.science/w/synthetic-presentation-explorer-7E83/) · [Browse all research materials](https://anonymous.4open.science/r/synthetic-presentation-explorer-7E83/)

## Deterministic worked example

Install Pillow in your own Python environment, then from the repository root:

```sh
python code/compose.py --layers example_layers/S01 --output reconstructed_S01
```

The supplied S01 layers reconstruct all 16 illustrated S01 cells. Compare their decoded RGB hashes with `data/stimuli.json`. PNG and lossless WebP file hashes differ, while decoded pixels match. Only one worked identity's layers are included to limit download size; all 256 final images are included.

## Generation

`data/generation_prompts.json` contains initial clothing/background trial prompts, selected repair prompts, and the override map identifying the replacement source for each repaired layer. `generate_one.py` extracts the original image API request pattern into a standalone one-call utility. Dry-run is the default. `--go` uses the caller's `OPENROUTER_API_KEY` and can incur charges. No key is supplied, no calls run in the explorer, and no automatic retries occur. The reference must be supplied explicitly; repair prompts may expect an empty-room image rather than a portrait.

We used `google/gemini-3-pro-image` and `openai/gpt-image-2.5-flare` in the balanced layer design. Endpoints and provider behavior may change. Image generation is stochastic, so a new call can produce a different image. The supplied final layers support exact reconstruction of the worked example.

## Face locking before composition

`face_lock.py` contains the extracted alignment and face-lock mathematics from the construction pipeline. The input arrays are a canonical RGB source and its person mask, an edited RGB foreground and mask, and facial landmarks. Eye-center alignment uses a similarity transform; a feathered jaw/head boundary combines the canonical upper region with the aligned clothing. The inner face is explicitly overwritten with source pixels and made opaque. Final layers are composited with Pillow.

We used Apple's Vision framework to locate the person and facial landmarks; `segment_person.swift` is included. Some images needed reviewed face selection or individual boundary adjustments. The final layers and pixel checks document the resulting construction, while visual inspection addresses the quality of the image itself.

## Limits

The original character briefs record intended impressions. Their scores have no psychometric validation, and some identities were recast after those briefs were written. The initial editor assignment was balanced across categories; the records identify later repairs separately. Human evaluation would be needed to establish how viewers respond to the finished images.
