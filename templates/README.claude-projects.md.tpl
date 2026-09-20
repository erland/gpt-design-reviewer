# {{GPT_NAME}} – Claude Projects

Version: {{VERSION}}

Detta paket är Claude Projects-distributionen av Design Reviewer. Den bygger på samma canonical design-review-kontrakt som övriga runtimes.

## Installation

1. Skapa ett Claude Project.
2. Använd `project/instructions.md` som projektets instruktioner.
3. Lägg filerna under `project/knowledge/` i projektets kunskapsmaterial när det är praktiskt.
4. Använd `project/runtime-contract.json` som referens för runtime-capabilities och kända begränsningar.
5. Lägg sedan in ett eller flera källkodsträd och eventuell dokumentation som projekt-/chatinput.

## Arbetsflöde

Design Reviewer ska inventera materialet innan den drar designslutsatser. Mindre kodbaser kan analyseras sammanhängande; större kodbaser ska delas upp progressivt med explicit checkpoint-state.

Vid progressiv analys fortsätter du med:

`Gör nästa steg`

Slutleveransen består av:

- `design-review.md`
- `recommended-solution-strategy.md`
- `implementation-plan.md`

## Claude Projects-specifika begränsningar

Detta paket bäddar inte in lokala shell- eller Pythonverktyg. Deterministiska analysverktyg från canonical-projektet är därför ett valfritt evidensstöd, inte ett krav. Om lokal kodexekvering saknas ska assistenten använda filläsning, sökning och semantisk analys i stället.

Projektets kontext får inte ersätta explicit analysstate vid längre reviews. Observationer, analyserade områden, kvarvarande hotspots, evidensluckor och skapade artefakter ska hållas tydligt spårbara så att arbetet kan återupptas utan att hela reviewn görs om.
