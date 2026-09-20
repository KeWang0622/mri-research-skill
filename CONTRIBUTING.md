# Contributing to the mri-research skill

Thanks for helping keep this a high-quality entry point for the MRI
reconstruction research community. Contributions that add landmark papers, new
toolboxes, corrected or updated links, additional vendor/format notes, or new
open datasets are all welcome.

## Design philosophy (please preserve it)

This is a **pointer / reference skill**, not a data or textbook dump. The value
is in accurate navigation and good judgment, so:

- **Link and summarize; do not vendor.** Never add datasets, model weights, or
  copyrighted text (textbook chapters, paywalled paper bodies). Cite the source
  and describe it in your own words.
- **Point to primary sources.** Prefer the original paper/repo over a
  secondary summary. Use awesome-lists as living indexes, not as the citation.
- **Keep the "which tool for which task" framing.** The reference files are
  organized to help a researcher *decide*, not just to enumerate.

## Quality bar for additions

- **Verify every link and citation before submitting.** Confirm the URL
  resolves and the repo/paper exists (e.g., `gh repo view <owner>/<repo>`, or
  open the DOI). Broken or hallucinated links are the one thing that makes a
  reference hub worse than nothing.
- **Cite consistently.** Papers as `Author(s). "Title." Venue Year;Vol(Issue):
  Pages. doi:…` (or an `arXiv:XXXX.XXXXX` id). Repos as full GitHub URLs.
- **Match the file.** The reference set (under `skills/mri-research/references/`)
  is: `foundations.md` (physics/courses/handbooks), `sequences-and-trajectories.md`
  (acquisition, RF, trajectories, SMS, correction), `hardware.md` (hardware +
  safety), `recon-methods.md` (reconstruction methods/papers + denoising +
  metrics), `tools.md` (reconstruction software), `data-and-formats.md`
  (formats + datasets), `analysis-processing.md` (structural/fMRI/dMRI, cardiac/
  body/MSK, segmentation, radiomics), `quantitative-and-spectroscopy.md`
  (qMRI + MRS), `literature-access.md` (paper/data APIs & MCP), `publishing.md`
  (journals, LaTeX, reporting standards), `radiology-primer.md` (contrast
  reading, non-diagnostic). Put each addition in the matching file; if a topic
  spans files, add a short cross-reference rather than duplicating.
- **Stay concise.** Each entry should earn its place — one to three lines of
  what it is and when to reach for it.

## How to propose a change

1. Fork and create a branch.
2. Make your edit in the appropriate `references/*.md` (or `SKILL.md` routing
   table if you add a new area).
3. Add a bullet to `CHANGELOG.md` under an `## [Unreleased]` heading.
4. Open a pull request describing the addition and linking the primary source
   you verified.

## Scope reminders

- The **radiology primer** is deliberately non-diagnostic background. Do not
  turn it into clinical guidance.
- Respect **dataset access terms** (e.g., the fastMRI data-use agreement). Do
  not add instructions that circumvent an access gate.

Questions or larger proposals (e.g., a new reference area) are welcome as an
issue first, so we can align on scope before you invest the work.
