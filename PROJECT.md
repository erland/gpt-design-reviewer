# Project – Design Reviewer

## Mål

Skapa en portabel Design Reviewer-assistent som analyserar ett eller flera källkodsträd och tillhörande dokumentation ur ett seniorutvecklar- och arkitekturperspektiv och levererar en spårbar väg från observation till genomförbar förbättring.

## Fokus

- separation of concerns och cohesion,
- starka och olämpliga kopplingar,
- beroenderiktningar och cirkulära beroenden,
- stora ansvarskoncentrationer,
- lagerblandning och läckande abstraktioner,
- testbarhet och förändringsbarhet,
- frontend-state, API-, data- och integrationsdesign,
- krav eller användarflöden som driver onödig teknisk komplexitet,
- positiva designstrukturer som bör bevaras.

## Leveransmodell

Slutresultatet består av:

1. `design-review.md`
2. `recommended-solution-strategy.md`
3. `implementation-plan.md`

Analysen får vara flerstegsbaserad. Ett implementationsteg ska vara ett sammanhängande, verifierbart checkpoint som normalt kan genomföras i en prompt.

## Projektprofil

`zip_first_advanced`, med avvikelsen att extern research är sekundär till den faktiska källkoden och dokumentationen.

## Canonical modell

Produktbeteendet definieras av `assistant/instructions.md`, `gpt-project.yaml` och kontrakten i `contracts/`.

Centrala modeller:

- `DR-*` – designobservationer,
- `RS-*` – lösningsteman,
- `VA-*` – valideringsåtgärder,
- `UX-*` – explicita krav-/UX-alternativ,
- `IP-*` – prompt-stora implementationsteg.

Prioritering bygger inte på severity ensam. Hårda beroenden, evidensgrindar och preserve constraints tillämpas först; därefter vägs nytta, confidence, kostnad, risk, förändringstryck och enabling effect.

## Analysworkflow

`contracts/analysis-workflow-contract.yaml` definierar focused/progressive analys, hotspot-kö, checkpoints, evidence gate, resume och coverage/bias-kontroller.

`Gör nästa steg` ska kunna fortsätta från explicit state utan att redan verifierat arbete görs om.

## Deterministiska verktyg

`scripts/analyze_source_tree.py` ger reproducerbar evidensinsamling. Verktygen gör inga designbedömningar och kärnreviewn ska kunna degradera till vanlig filläsning/sökning om kodexekvering saknas.

## Peer runtimes

Implementerade och validerade från samma canonical kontrakt:

- ChatGPT Chat
- ChatGPT Custom GPT
- Claude Projects
- OpenCode

Runtime parity verifieras med `scripts/check_runtime_parity.py`. Dokumenterade adapterskillnader finns i `docs/runtime-parity.md`.

## Kvalitet

Projektet har schemas, deterministiska evals, lint, hygiene, distributionsvalidering och runtime-parity-kontroll. Release readiness och release-konfiguration följer i planens steg 19–20.


## GitHub Actions

Projektet innehåller CI och releaseautomation under `.github/workflows/`. CI bygger och validerar canonical project samt ChatGPT Chat, Custom GPT, Claude Projects och OpenCode. När en GitHub Release publiceras härleds versionsnumret från releasetaggen och samtliga ZIP-distributioner, checksummor och delivery manifest laddas upp till releasen. Se `docs/release-configuration.md`.
