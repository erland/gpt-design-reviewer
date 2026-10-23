# Full design-review workflow

## När den aktiveras
Använd när användaren uttryckligen vill ha en fullständig sammanhängande granskning från källkod till implementationsplan.

## Arbetssteg
Samordna i ordning `source-analysis`, `design-review`, `solution-strategy` och `implementation-planning`. Använd respektive Skills kontrakt och artefakter i stället för att duplicera dess detaljerade instruktioner. Kontrollera evidens innan slutrapporter skapas. För stora system: inventera, granska hotspots och tvärgående kopplingar i omgångar och spara checkpoint-state.

## Utdata
Tre separata Markdownfiler: `design-review.md`, `recommended-solution-strategy.md` och `implementation-plan.md`. Verifiera att RS refererar DR och IP refererar RS; rapportera evidensluckor. Fortsätt med `Gör nästa steg` utifrån projektstatus.

## Valfri praktisk verifiering
När faktisk exekvering eller UI-observation behövs för en specifik designhypotes, följ `assistant/policies/companion-review-workflows.md` och evidensreglerna i gemensam kärna. Plugins är valfria; rapportera ej utförda kontroller som NOT VERIFIED och använd VA-åtgärd när evidensen inte räcker.
