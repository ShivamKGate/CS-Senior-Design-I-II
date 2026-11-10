# Project Constraints Essay: Nipun Chandra

**Project:** HepatoFusion
**Team members:** Nipun Chandra, Shivam Kharangate

## Ethical

HepatoFusion is scoped as a decision-support system for pediatric liver cancer, and that framing is enforced architecturally: the pipeline terminates in tumor maps and risk scores surfaced to a pathologist, never in an autonomous diagnostic output, which constrains the API surface, logging, and UI to always expose a human review step. The Silver/Gold annotation workflow is itself an ethical design choice, because provisional (Silver) labels are segregated from expert-validated (Gold) labels in the data layer so training, evaluation, and reporting cannot silently mix the two.

## Security (and privacy)

Security constraints shape the deployment topology before they shape any model, since whole-slide images and linked outcomes are PHI and must stay on approved institutional compute rather than personal laptops or consumer cloud GPUs. This rules out third-party hosted inference endpoints and shared notebooks with embedded slide data, pushing the design toward on-prem training with scripted, reproducible pipelines instead of ad-hoc exploratory tooling, and it forces checkpoints and intermediate tiles to be treated as sensitive artifacts throughout the system.

## Legal (regulatory)

The Cincinnati Children’s data-use agreement and UC IP rules for student work bound what the system is allowed to emit, not just what it can ingest, so slide tiles, derived annotations, and trained weights cannot be redistributed outside approved channels. That shapes the evaluation harness as an offline, in-institution component rather than a public leaderboard submission, and keeps deliverables as research prototypes without FDA diagnostic claims in this phase.

## Economic

With no commercial budget and only UC and Cincinnati Children’s research compute available, model and pipeline choices are bounded directly: U-Net resolution, tile size, batch size, and multimodal fusion depth all have to fit inside existing GPU allocations. The viable design reuses the open-source PyTorch stack and the existing Silver/Gold ingestion pipeline rather than buying commercial pathology platforms, so engineering effort is spent on fusion and evaluation instead of rebuilding infrastructure the project already owns.

## Concrete trade-off

The sharpest tension is economic compute limits versus multimodal scale: jointly training pathology WSIs, radiology, DNA, and outcome records end-to-end at full resolution would exceed the available GPU budget, so the design favors a staged fusion architecture where the pathology U-Net is trained once and its features are reused downstream, accepting weaker end-to-end joint optimization in exchange for a system that actually fits inside the compute envelope that security and economic constraints leave us.
