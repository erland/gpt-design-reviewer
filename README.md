# Design Reviewer

Design Reviewer är ett portabelt GPT-projekt för strukturerad designgranskning av ett eller flera källkodsträd tillsammans med eventuell dokumentation.

Assistenten agerar som en erfaren senior utvecklare och mjukvaruarkitekt. Fokus ligger på förändringsbarhet, begriplighet, testbarhet, kopplingar, ansvarsfördelning och långsiktig underhållbarhet — inte på trivial lint eller kodstil.

## Slutleveranser

Varje färdig review ska kunna producera tre Markdown-artefakter:

- `design-review.md` – problem, evidens, konsekvenser, allvarlighetsgrad, styrkor och vad som bör åtgärdas före viss vidareutveckling.
- `recommended-solution-strategy.md` – prioriterad lösningsstrategi utifrån nytta, risk, förändringstryck, beroenden och enabling effect.
- `implementation-plan.md` – konkreta `IP-*`-steg dimensionerade för att normalt kunna genomföras ett steg per prompt.

## Analysmodell

Design Reviewer kan arbeta focused för mindre kodbaser eller progressive för större system. Progressiv analys använder hotspots, explicita checkpoints, evidence gate och återupptagning med `Gör nästa steg`.

Observationer använder stabila `DR-*`-ID:n. Severity hålls separat från evidensstyrka, confidence, framtida förändringstryck, åtgärdsrisk och enabling effect. En stor fil eller funktion är därför aldrig automatiskt ett designproblem.

Lösningsstrategin använder `RS-*` för åtgärdsteman, `VA-*` för valideringsbehov och `UX-*` för explicita krav-/UX-alternativ. Implementationsplanen använder `IP-*`.

## Canonical source och kontrakt

Den canonical assistentinstruktionen finns i `assistant/instructions.md`. Plattformsneutrala kontrakt finns i `contracts/`, med schemas i `schemas/` och rapportmallar i `templates/`.

Viktiga kontrakt omfattar:

- observationsmodell,
- focused/progressive analysworkflow,
- design review-rapport,
- prioriteringsmodell och lösningsstrategi,
- LLM-anpassad implementationsplanering,
- artifact-, capability-, workspace/state- och tool-kontrakt.

## Deterministisk evidensinsamling

När runtimen kan köra Python kan Design Reviewer använda `scripts/analyze_source_tree.py` för reproducerbar inventering av bland annat filstruktur, stora filer/funktioner, importindikatorer och möjliga duplicerade block.

Verktygsresultaten är endast evidens- och hotspot-signaler. De får aldrig ensamma bli designobservationer. Se `docs/deterministic-analysis-tools.md`.

## Eval och kvalitet

`evals/` innehåller regressionsfall för bland annat välstrukturerad kod, falska hotspots, monoliter, flera repositories, enabling refactoring, svag evidens och UX-/kravalternativ.

Projektverktygen i `scripts/` används för lint, hygiene, evals, runtime parity, build och distributionsvalidering.

## Peer runtimes

Följande runtimes är implementerade från samma canonical produktmodell:

- ChatGPT Chat
- ChatGPT Custom GPT
- Claude Projects
- OpenCode
- OpenAI Plugin

Canonical capabilities, slutartefakter och workspace/resume-state ska vara identiska mellan runtimes. Endast verkliga adapterskillnader får variera. Se `docs/runtime-parity.md`.

## GPT Byggaren 1.5.0

Design Reviewer är migrerad till GPT Byggaren 1.5.0 med bibehållet produktbeteende och fortsatt 20/20 complete produktstatus.

Aktiva runtime-distributioner är ChatGPT Chat, ChatGPT Custom GPT, Claude Projects, OpenCode och OpenAI Plugin. Verklig compatibility redovisas som Chat `equivalent_runtime_dependent`, Custom GPT `equivalent_with_platform_constraints`, Claude Projects `reduced`, OpenCode `equivalent` och OpenAI Plugin `equivalent_runtime_dependent`.

OpenAI Plugin är skills-first och använder hostens filesystem/persistent-state capabilities. `scripts/analyze_source_tree.py` paketeras som rekommenderad script-resurs; saknas code execution fortsätter den semantiska analysen med ärlig degrade. Build, runtime-verifiering, parity och GitHub Release härleds från `runtime-distribution-registry.yaml`, och exakt release-asset-set valideras före publicering.

Se `docs/gpt-builder-1.5-runtime-migration.md`, `docs/openai-plugin-1.5-assessment.md` och `migration-status-1.5.yaml`.

## Projektstatus

Se `STATUS.md` och `project-status.yaml` för aktuell checkpoint. Hela utvecklingsplanen finns i `docs/development-plan.md`.


## GitHub Actions

Projektet innehåller CI och releaseautomation under `.github/workflows/`. CI bygger och validerar canonical project samt ChatGPT Chat, Custom GPT, Claude Projects och OpenCode. När en GitHub Release publiceras härleds versionsnumret från releasetaggen och samtliga ZIP-distributioner, checksummor och delivery manifest laddas upp till releasen. Se `docs/release-configuration.md`.
