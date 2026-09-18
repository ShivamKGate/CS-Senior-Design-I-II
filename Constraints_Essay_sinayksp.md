# Project Constraints Essay: Shivam Sinay Kharangate

**Project:** HepatoFusion  
**Team members:** Shivam Kharangate, Nipun Chandra

## Ethical

HepatoFusion uses pediatric liver-cancer pathology and clinical records from Cincinnati Children’s Hospital through IRB approval, so ethical constraints apply directly, which include errors in tumor localization or risk scores could affect interpretation for a vulnerable patient group, hence the early-stage prototype before clinical workflow integration. Viable solutions treat the system as decision support with pathologist review for Gold labels and final interpretation, and they require evaluation against expert annotations before any clinical-facing claims are made. Silver (provisional) labels will not be presented as ground truth in demos or reports, because the Silver/Gold workflow exists to reduce label error before training and evaluation, but some metrics can be shown to compare the difference between Silver vs. Gold.

## Security (and privacy)

Security and privacy constrain allowed data and compute paths: whole-slide images and linked outcomes are protected health information under hospital policy and HIPAA-aligned handling at Cincinnati Children’s. Viable architecture keeps raw PHI and identifiers off personal devices and public repositories, restrict training and inference to approved institutional or hospital environments, and exclude consumer cloud APIs for slide or outcome data even when those tools would speed prototyping.

## Legal (regulatory)

Legal constraints apply because the project uses hospital-held clinical data aimed at risk stratification, not only academic benchmarks. Solutions must respect Cincinnati Children’s data-use agreements, institutional permissions governing the 102+ patient / 248+ WSI cohort, and UC intellectual-property rules for student work on partner data; deliverables remain research prototypes without FDA diagnostic claims or redistribution of partner slides outside approved channels.

## Economic

Economic limits shape pipeline choices: high-resolution U-Net training on WSIs needs substantial GPU time, and the team has no open commercial budget beyond UC and Cincinnati Children’s facilities and existing research compute. Viable solutions therefore use open-source stacks (PyTorch and the in-house pipeline behind the 0.96 mean slide Dice backbone) and reuse the existing Silver/Gold stream (1,566+ Silver / 1,546+ Gold) rather than purchasing commercial pathology platforms or new labeled datasets.

## Concrete trade-off

The central tension is security/privacy versus development speed and multimodal scale, where stricter PHI isolation protects patients and satisfies hospital policy but limits external tooling and how freely intermediate artifacts can be shared for debugging. We choose compliance-first scoping, with train and evaluate only on approved institutional data and environments, even if that delays fusion features or forces smaller ablation studies than an open dataset would allow.
