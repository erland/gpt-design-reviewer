# Canonical contracts

Detta katalogträd innehåller Design Reviewers plattformsneutrala kärnkontrakt.

- `analysis-workflow-contract.yaml` – focused/progressive analys, faser, hotspots, checkpointing, resume och evidence gate.
- `design-observation-contract.yaml` – designproblem, styrkor, osäkerheter och förbättringsmöjligheter.
- `design-review-report-contract.yaml` – canonical struktur för `design-review.md`.
- `solution-prioritization-contract.yaml` – prioritering efter nytta, risk, förändringstryck, beroenden och enabling effect.
- `solution-strategy-report-contract.yaml` – canonical struktur för `recommended-solution-strategy.md`.
- `implementation-planning-contract.yaml` – nedbrytning till prompt-stora `IP-*`-checkpoints.
- `implementation-plan-report-contract.yaml` – canonical struktur, checkpoint-logg och resume-regler för `implementation-plan.md`.
- `deterministic-analysis-tools.yaml` – regler för deterministisk evidensinsamling.
- `eval-suite-contract.yaml` – regressionssvitens coverage- och kvalitetskrav.

Capability-, artifact-, workspace/state- och tool-kontrakt finns i `gpt-project.yaml` och valideras mot schemas i `schemas/`.

Runtime-adaptrar får mappa dessa kontrakt till sin plattform men får inte ändra produktens grundläggande analysbeteende.
