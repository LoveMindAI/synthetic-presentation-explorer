# Synthetic presentation explorer

[Open the interactive explorer](https://anonymous.4open.science/w/synthetic-presentation-explorer-7E83/) to choose a person, change their outfit or setting, and compare images side by side.

This collection contains 16 fictional people, each shown in four outfits and four settings: 256 fully synthetic images. It illustrates how we constructed controlled presentation changes for person-perception research.

**Everyone pictured in the explorer is fully synthetic.** The paper's PARSEL results come from a separate, sensitive participant dataset. PARSEL photographs, participant-derived personality profiles, transcripts and raw request logs remain private. Access to that material requires separate authorization. The manuscript describes the private stimulus sets used in its analyses and gives their experimental counts.

Open `index.html` in a browser, or serve this directory using `python -m http.server 8000`. The authored explorer has no external dependencies, author-operated analytics, API calls or external fonts. Hosting providers may inject their own telemetry; that is separate from this companion's code.

- `matrix/`: all 256 lossless, metadata-stripped WebP images; decoded RGB pixels verified against the source PNGs.
- `data/stimuli.json`: file and decoded-pixel hashes, identity and condition coordinates.
- `data/generation_prompts.json`: initial layer prompts, selected repairs, and editor assignments.
- `data/original_authoring_briefs.json`: the original character briefs and artistic intentions, written before some identities were recast. The intended impression scores have no psychometric validation.
- `data/presentation_briefs.json`: individual clothing and room instructions.
- `prompts/`: participant-free judgment templates with explicit scope notes.
- `code/`: extracted image-generation request, face-lock mathematics, segmentation source and final compositor.
- `example_layers/S01/`: a complete worked synthetic identity for exact final reconstruction.

We have not collected human ratings of this synthetic collection. Pixel checks establish that the central face region stays consistent across each person's grid. Realism and the impressions evoked by the clothing and rooms still need human evaluation. Two changes remain less clear than intended: S03's evening outfit and the clutter in S07's room.

The explorer helps readers inspect the construction method. Any relationship between these artistic intentions and viewers' judgments would require a separate study.
