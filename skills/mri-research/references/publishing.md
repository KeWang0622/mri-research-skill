# Publishing MRI research: journals, LaTeX, reporting standards

Use this when the user is writing up MRI work — choosing a venue, finding a
journal's author guidelines or LaTeX template, meeting a reporting/reproducibility
standard, or submitting an abstract/preprint. Links point to official author
pages; summarize requirements rather than pasting them.

Note: several publisher pages (Wiley, Elsevier, RSNA, MIT Press) block automated
fetching but open normally in a browser — they are not login-gated. If a link
appears to fail programmatically, it's the bot-block, not a dead URL.

## Where MRI work tends to go

- **MR-methods & physics** → *Magnetic Resonance in Medicine* (MRM) — the ISMRM
  flagship and the default home for reconstruction, acquisition, and pulse-
  sequence methods.
- **Computational / ML imaging** → *IEEE Transactions on Medical Imaging* (TMI)
  and *Medical Image Analysis* (MedIA).
- **Neuroimaging** → *NeuroImage* and *Imaging Neuroscience*.
- **Clinical / applications** → *JMRI*, *Radiology*, *Radiology: AI*.
- **Preprint first** → arXiv (eess.IV, physics.med-ph, cs.CV) is standard for
  recon/ML work; check each journal's preprint policy (most MR journals allow
  it).

## Journal author guidelines (and LaTeX support)

- **Magnetic Resonance in Medicine (MRM, Wiley)** — guidelines:
  https://onlinelibrary.wiley.com/page/journal/15222594/homepage/author-guidelines
  · **Official MRM LaTeX class:**
  https://onlinelibrary.wiley.com/journal/15222594/la_tex_class_file
- **Journal of Magnetic Resonance Imaging (JMRI, Wiley)** —
  https://onlinelibrary.wiley.com/page/journal/15222586/homepage/forauthors.html
  (Word-based; no official LaTeX template).
- **NMR in Biomedicine (Wiley)** —
  https://analyticalsciencejournals.onlinelibrary.wiley.com/hub/journal/10991492/homepage/forauthors.html
  (use the generic Wiley LaTeX template).
- **MAGMA — Magn. Reson. Materials in Physics, Biology and Medicine (Springer)**
  — https://link.springer.com/journal/10334/submission-guidelines (accepts Word
  or the Springer Nature LaTeX template).
- **IEEE Transactions on Medical Imaging (TMI)** —
  https://ieeetmi.org/authors-instructions/ (use the IEEEtran LaTeX class).
- **Medical Image Analysis (Elsevier)** —
  https://www.sciencedirect.com/journal/medical-image-analysis/publish/guide-for-authors
  (LaTeX via elsarticle).
- **NeuroImage (Elsevier)** —
  https://www.sciencedirect.com/journal/neuroimage/publish/guide-for-authors
  (LaTeX via elsarticle).
- **Imaging Neuroscience (MIT Press)** —
  https://direct.mit.edu/imag/pages/guide_for_authors (single all-in-one PDF at
  initial submission; LaTeX accepted at revision).
- **Radiology (RSNA)** —
  https://pubs.rsna.org/page/radiology/author-instructions (Word-based).
- **Radiology: Artificial Intelligence (RSNA)** —
  https://pubs.rsna.org/page/ai/author-instructions (Word-based).

## LaTeX templates & classes

- **Wiley** (covers MRM/JMRI/NMR in Biomed): the MRM class file above, plus the
  general Wiley template:
  https://authors.wiley.com/author-resources/Journal-Authors/Prepare/latex-template.html
- **IEEEtran** (IEEE TMI and other IEEE venues): https://ctan.org/pkg/ieeetran
  (also on the IEEE Author Center and Overleaf).
- **elsarticle** (Elsevier — MedIA, NeuroImage): https://ctan.org/pkg/elsarticle
  · Elsevier LaTeX instructions:
  https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions
- **Springer Nature** (MAGMA):
  https://www.springernature.com/gp/authors/campaigns/latex-author-support
- **Overleaf template gallery** (many of the above, ready to fork):
  https://www.overleaf.com/gallery
- **arXiv submission help** (LaTeX source requirements):
  https://info.arxiv.org/help/submit/index.html

## Reporting & reproducibility standards

Increasingly expected — and often required — especially for ML/quantitative work:

- **COBIDAS** (OHBM) — best-practice reporting for (f)MRI studies:
  https://www.humanbrainmapping.org/COBIDAS/ (2016 MRI report PDF:
  https://www.humanbrainmapping.org/files/2016/COBIDASreport.pdf).
- **CLAIM** — Checklist for Artificial Intelligence in Medical Imaging (RSNA):
  https://pubs.rsna.org/page/ai/claim (2024 update: doi:10.1148/ryai.240300).
- **TRIPOD+AI** — reporting for clinical prediction models using AI:
  https://www.tripod-statement.org/
- **ISMRM Reproducible Research Study Group (RRSG)** — code-and-data sharing
  practices; partners with MRM on optional code review:
  https://ismrm.github.io/rrsg/ (MRM also states its reproducible-research
  policy in the author guidelines above).

## Abstracts & meetings

- **ISMRM Annual Meeting** — the field's main conference; abstracts are the
  primary way MR methods are first presented:
  https://www.ismrm.org/abstract-submission-and-review/ (current call:
  https://www.ismrm.org/26m/call/).

## Practical notes

- **Match venue to contribution:** a new recon algorithm → MRM or IEEE TMI; a
  clinical validation → JMRI/Radiology; a neuroimaging analysis → NeuroImage.
- **Share code and data** (respecting dataset DUAs — see [`data-and-formats.md`](data-and-formats.md)):
  a public repo with a fixed release/DOI (e.g., via Zenodo) strengthens review
  and satisfies reproducibility policies.
- **Cite primary methods** from [`recon-methods.md`](recon-methods.md) and tools from [`tools.md`](tools.md)
  correctly; many MR toolboxes request a specific citation.
