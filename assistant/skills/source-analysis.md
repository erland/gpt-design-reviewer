# Source analysis

## När den aktiveras
Använd vid begäran om källkodsinventering, teknikstack, beroenden, hotspots eller insamling av underlag inför designgranskning.

## Arbetssteg
Inventera källträd, dokumentation, teknikstack, modulgränser, dataflöden, integrationer och tester. Kör valfritt `scripts/analyze_source_tree.py` om Python finns. Validera indikatorer mot faktisk kod; klassificera dem inte automatiskt som designfel. Uppmärksamma okända och ej granskade områden.

## Utdata och överlämning
Lämna inventering med exakta källreferenser, arkitekturöversikt, styrkor, hotspots och evidensluckor. Uppdatera `project-status.yaml`; nästa Skill är `design-review`. Ändra inte källkoden.

## Valfri praktisk verifiering
När faktisk exekvering eller UI-observation behövs för en specifik designhypotes, följ `assistant/policies/companion-review-workflows.md` och evidensreglerna i gemensam kärna. Plugins är valfria; rapportera ej utförda kontroller som NOT VERIFIED och använd VA-åtgärd när evidensen inte räcker.
