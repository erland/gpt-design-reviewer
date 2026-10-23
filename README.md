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

## Aktiva distributioner och GPT Byggaren 1.6.26

Det auktoritativa distributionsregistret `runtime-distribution-registry.yaml` anger byggmotor **1.6.26** och följande fem aktiva runtime-mål:

- ChatGPT Chat (`chat`)
- OpenAI Plugin (`plugin`)
- Claude Project (`claude_project`)
- Claude Skills (`claude_skills`)
- OpenCode (`opencode`)

**Custom GPT är pensionerad** i det aktuella distributionsregistret. Projektets tidigare 1.5-dokumentation finns kvar som historik men beskriver inte det aktuella release-asset-setet. Canonical produktbeteende är gemensamt; faktiska runtimebegränsningar måste fortfarande verifieras.

## Valfri verklighetsbaserad evidens

Agent Workspace kan ge isolerad teknisk build/test-evidens, PWA Preview kan tillgängliggöra en säker statisk webbapp och Browser Screenshot kan ge visuella eller interaktiva observationer. Verktygen är **valfria** och får aldrig krävas för den vanliga designgranskningen. En lyckad preview är inte ett funktionstest, och en skärmbild bevisar inte ett underliggande arkitekturfel.

Policy: `assistant/policies/optional-companion-evidence.md` och `assistant/policies/companion-review-workflows.md`. PR #11–#12 införde instruktioner och offlinekontrakt; PR #13 lade till **17 simulerade fallbacktestfall**. Dessa tester gör inga live-MCP-anrop och bevisar inte faktiskt språkmodellbeteende med installerade plugins.

## Projektstatus

Se `STATUS.md` och `project-status.yaml` för aktuell checkpoint. Hela utvecklingsplanen finns i `docs/development-plan.md`.


## GitHub Actions

Projektet innehåller CI och releaseautomation under `.github/workflows/`. CI bygger och validerar canonical project samt de fem runtime-målen i distributionsregistret. När en GitHub Release publiceras härleds versionsnumret från releasetaggen och samtliga ZIP-distributioner, checksummor och delivery manifest laddas upp till releasen. Se `docs/release-configuration.md`.
