# AWS Breaking Barriers GenAI Hackathon Project

![AWS Hackathon Cover](image-assets/aws-hackathon-logo.png)

## Overview

This repository documents and (soon) implements a hackathon project for the AWS Breaking Barriers Challenge 2026.

The initial solution focus is Stop the Traffik: Survivor‑Powered Supply Chain Intelligence — turning survivor narratives and field reports into real‑time supply chain risk signals using Amazon Bedrock, Comprehend, SageMaker, and serverless AWS services. Code snippets and Architecture Decision Records (ADRs) will be added as the build progresses.

## Quick Links

- [Hackathon Solution Architecture](generated-docs/Stop_the_Traffik_AWS_Hackathon_Solution.md)
- [10 AWS AI Solutions for Stop the Traffik](generated-docs/Stop_the_Traffik_10_AWS_AI_Solutions.md)
- [7‑Day GenAI Hackathon Preparation Plan](generated-docs/AWS_GenAI_Hackathon_7Day_Plan%20%281%29.md)

## Architecture at a Glance

- High‑level architecture, data flow, and MVP scope are detailed in the Hackathon Solution document (see the section “High‑Level Architecture Diagram”).
- Direct link to the diagram section: [Stop_the_Traffik_AWS_Hackathon_Solution.md#high-level-architecture-diagram](generated-docs/Stop_the_Traffik_AWS_Hackathon_Solution.md#high-level-architecture-diagram)

![AWS Hackathon Image](image-assets/aws-hackathon-image.png)

## Getting Started

This repository currently contains generated documentation and image assets that frame the solution. Implementation code and runnable demos will be added during and after the hackathon.

- Browse the architecture and MVP scope in the Hackathon Solution document.
- Use the 7‑Day Plan to ramp up on Bedrock, RAG, serverless patterns, and security.
- Review the “10 AWS AI Solutions” document for adjacent ideas and future roadmap items.

When code is added, this section will include:

- Setup instructions (requirements, environment variables, AWS credentials)
- Local development and deployment steps (SAM/CDK, IaC, endpoints)
- Example requests and test data

## Repository Layout

- generated-docs/
  - AWS_GenAI_Hackathon_7Day_Plan (1).md
  - Stop_the_Traffik_10_AWS_AI_Solutions.md
  - Stop_the_Traffik_AWS_Hackathon_Solution.md
- image-assets/
  - aws-hackathon-cover-image.png
  - aws-hackathon-image.png
  - aws-hackathon-logo.png
- (to be added) src/ — code snippets and services for the MVP
- (to be added) docs/adr/ — Architecture Decision Records

## Architecture Decision Records (ADRs)

This project will track key technical decisions as ADRs (one file per decision). Once ADRs are added under `docs/adr/` (or `adr/`), they will be indexed here.

Recommended conventions:

- ADR format: Title, Status, Context, Decision, Consequences
- Filenames: `ADR-0001-title.md`, `ADR-0002-title.md`, …

## Contributing

- Open an issue for questions, bugs, or proposed enhancements.
- Use small, focused PRs that link to the relevant doc section(s).
- Please avoid committing any sensitive data. For secrets, plan to use AWS Secrets Manager or Parameter Store.

## License

TBD. If you plan to reuse or extend the work, please add a LICENSE file or contact the maintainers.

## Acknowledgements

- Stop the Traffik and partner organizations for domain insights.
- AWS AI/ML services teams and open resources cited throughout the generated docs.
