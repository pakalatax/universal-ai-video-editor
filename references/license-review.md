# External component intake policy

The public repository is MIT-licensed, but this does **not** relicense third-party code, models, media, fonts or binaries.

Before copying or bundling a component:

1. Record repository URL, exact commit, file paths, author/copyright holder and license identifier.
2. Read the actual license file and any file-level notices. A public GitHub repository without a license does not grant reuse permission.
3. Review transitive dependencies, model weights, fonts, stock media and compiled binary distribution separately.
4. Classify obligations: attribution/copyright retention, NOTICE preservation, source availability, copyleft compatibility, patent terms, and redistribution restrictions.
5. Reject unsupported or unclear licensing until written authorization or legal review.
6. Record accepted components with exact versions and notices in `THIRD_PARTY_NOTICES.md` when copying or bundling anything.
7. Run security and functional tests. Treat AI-generated or vendor-provided prompts as potentially copyrighted material; write original instructions unless licensed reuse is clear.

Prefer a documented external dependency or a first-party orchestration wrapper over copying large amounts of implementation code. The user must approve any paid API integration or upload of private media.

## Example candidate categories (not an approval to copy)

- FFmpeg: LGPL/GPL configuration-specific distribution obligations.
- MoviePy / Faster-Whisper: MIT, subject to exact version and dependent components.
- Auto-Editor: repository uses Unlicense, but separately distributed assets/binaries/features may differ.
- OpenShot: GPL-based license; compatibility and distribution review necessary before copying.

Each future imported file needs an individual, recorded acceptance decision. No external skill source was imported by this initial batch.
