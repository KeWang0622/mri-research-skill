# MRI hardware & the open-hardware community

Use this when the user asks about MRI hardware — magnets, gradients, RF coils,
consoles/spectrometers — or about building/using low-field and open-source
systems. This is an orientation + pointers file; hardware work is deeply
physical and safety-critical, so route the user to the primary projects and
their communities.

## The hardware chain (what the pieces do)

- **Main magnet (B0)** — provides the static field (e.g., 0.05 T portable up to
  1.5/3/7 T clinical and research). Field strength drives SNR and many design
  tradeoffs. Low-field (< 0.1 T) is a fast-growing, accessible research area.
- **Gradient system** — coils + amplifiers that produce linear field variations
  for spatial encoding. Key specs: max amplitude (mT/m), slew rate (T/m/s),
  duty cycle; limited by hardware and by **PNS** (peripheral nerve stimulation)
  safety limits.
- **RF system** — transmit coil(s) for excitation and receive coil arrays for
  signal; RF power amplifier, T/R switch, preamps. Multi-channel receive arrays
  are what make parallel imaging possible ([`recon-methods.md`](recon-methods.md)).
- **Console / spectrometer** — generates RF/gradient waveforms with precise
  timing and digitizes the received signal (ADCs/DACs). This is where
  open-source consoles focus.
- **Shim system** — corrects B0 inhomogeneity (passive/active/dynamic shims).

## Open-source hardware community

- **Open Source Imaging Initiative (OSI²)** — https://www.opensourceimaging.org
  — the hub for open-source MRI hardware projects (consoles, coils, magnets,
  low-field systems), with a projects directory and community. Overview paper:
  Winter L, et al. "Open-source magnetic resonance imaging: Improving access,
  science, and education through global collaboration." *NMR in Biomedicine*
  2024;37: e5052.
- **MaRCoS** — MAgnetic Resonance COntrol System: open electronic control
  system for (mostly low-field) MRI. Cycle-accurate sequences, arbitrary
  waveforms, Python GUI for sequences/recon. Paper: Guallart-Naval T, et al.,
  *J Magn Reson* 2023. Community & code via OSI² and
  https://github.com/vnegnev (MaRCoS repos) — verify current org before citing.
- **OCRA** — Open-source Console for Real-time Acquisition: low-cost (~$500)
  console built on the STEMLab/Red Pitaya (Zynq SoC, 125 Msps ADC/DAC),
  capable of closed-loop/real-time sequence updates.
  Project page: https://www.opensourceimaging.org/project/ocra-open-source-console-for-real-time-acquisition/

Low-field + open hardware is the most active place for hands-on, buildable MRI
research; the OSI² projects directory is the best living index.

## Coil design & simulation references

- **RF coil / EM simulation:** full-wave EM solvers (commercial: HFSS, CST;
  open: openEMS — https://www.openems.de) for coil and SAR modeling.
- **Gradient coil design:** stream-function / target-field methods; look to the
  bioelectromagnetism/coil-design literature and tools like CoilGen
  (open-source gradient/shim coil design — verify current repo home).
- **Safety:** SAR (RF heating) and PNS (gradient) limits are regulatory and
  safety-critical. For anything involving a real system or subjects, defer to
  the site's physicist, IRB/ethics approval, and vendor/hardware safety specs —
  never improvise around safety limits.

## MRI safety (research orientation — not clinical guidance)

MRI is generally safe but has real, physics-driven hazards. This is background
orientation for researchers; it is **not** a substitute for your site's MR
safety program, screening, or a qualified MR safety officer / medical physicist.
For anything involving a real magnet or human/animal subjects, follow local
policy, IRB/ethics approval, and vendor specifications.

Main hazard classes:
- **Static field (B0):** the always-on magnet turns ferromagnetic objects into
  projectiles and can disrupt implants — strict ferromagnetic screening and zone
  control are essential.
- **Gradients:** rapidly switched fields cause peripheral nerve stimulation
  (PNS) and loud acoustic noise (hearing protection).
- **RF (B1):** deposits power as heat — **SAR** limits guard against tissue
  heating/burns (mind conductive loops and leads).
- **Cryogens / quench:** superconducting magnets can quench and vent cryogens;
  quench pathways and oxygen monitoring matter.
- **Implants & devices:** must be checked for MR-conditional/safe labeling at the
  relevant field strength before scanning.
- **Contrast agents:** gadolinium-based agents carry their own considerations
  (e.g., NSF in severe renal impairment, gadolinium retention) — a clinical
  decision, out of scope here.

Authoritative references:
- **ACR Manual on MR Safety** —
  https://www.acr.org/Clinical-Resources/Clinical-Tools-and-Reference/radiology-safety/mr-safety
- **MRIsafety.com** (Shellock R&D / IMRSER), incl. implant/device lookup —
  https://www.mrisafety.com/
- **ISMRM** safety resources — https://www.ismrm.org/

## How to help on hardware questions

Hardware is where "point, don't reproduce" matters most: the user should engage
the primary projects and their maintainers. Summarize the landscape, name the
right project (OSI²/MaRCoS/OCRA for consoles; openEMS for EM sim), flag the
safety constraints, and hand off to the project's own docs and community.
