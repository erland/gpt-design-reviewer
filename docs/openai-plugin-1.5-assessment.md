# OpenAI Plugin compatibility assessment – Design Reviewer / GPT Byggaren 1.5.0

## Beslut

OpenAI Plugin är **inte en aktiv peer runtime** för Design Reviewer i GPT Byggaren 1.5.0.

Målbilden är:

- status: `not_active`
- compatibility: `reduced`
- mode: `advisory_only`

Detta är ett medvetet preserve-first-beslut. Design Reviewers kärnflöde bygger på konkret projektmaterial, explicit state och spårbara artefakter. En plugin får inte betraktas som full peer runtime om dessa capabilities inte faktiskt finns och kan verifieras.

## Kärnkrav för full peer-runtime parity

Full parity kräver minst:

1. Åtkomst till ett eller flera kompletta källkodsträd/ZIP-filer.
2. Möjlighet att läsa teknisk och funktionell dokumentation tillsammans med koden.
3. Persistent workspace/state utanför chattminnet.
4. Läsning och uppdatering av `project-status.yaml` som auktoritativ state.
5. Stöd för `Gör nästa steg` utan att tidigare chatthistorik är enda sanningskälla.
6. Faktisk skrivning av:
   - `design-review.md`
   - `recommended-solution-strategy.md`
   - `implementation-plan.md`
7. Möjlighet att skapa/uppdatera komplett project package.
8. Tillförlitlig validering av state, artefakter och paketering.
9. Kontrollerad mutation av workspace-filer med tydlig approval-/safety-gräns.
10. No-false-PASS: unrun verification får aldrig redovisas som PASS.

## Tillåtet advisory-beteende

En reducerad advisory-plugin får bland annat:

- förklara Design Reviewers observations- och prioriteringsmodell,
- resonera om DR/RS/VA/UX/IP-semantik,
- analysera användartillhandahållna kodutdrag eller dokumentutdrag,
- föreslå hotspots och frågor att verifiera,
- föreslå designobservationer med explicit evidensnivå,
- föreslå lösningsstrategi och implementation themes,
- föreslå innehåll till de tre slutartefakterna,
- förklara befintliga validation-/eval-resultat som användaren tillhandahåller.

## Förbjudna claims utan backing capability

En advisory-plugin får inte utan faktisk capability hävda att:

- ett helt repository eller källkodsträd har analyserats,
- persistent workspace-state har lästs eller uppdaterats,
- `project-status.yaml` har muterats,
- `Gör nästa steg` återupptagit från verklig persistent checkpoint,
- deterministiska scripts har körts,
- validering/evals har passerat,
- de tre slutartefakterna har skapats som faktiska filer,
- komplett project package har byggts,
- en kontroll som inte körts är PASS.

## Aktiveringskriterier

OpenAI Plugin får flyttas till aktiv runtime först genom en separat förändring där konkreta plugin tools/MCP-integreringar mappas mot Design Reviewers canonical capabilities och regressionstestas.

Minimikrav för aktivering:

- verifierad source-tree/file access,
- persistent workspace/state,
- filesystem write,
- artifact generation som faktiska filer,
- reliable validation,
- project package generation,
- no-false-PASS,
- regression mot canonical capability-, artifact-, workspace/state- och tool-kontrakt.

Fram till dess finns ingen OpenAI Plugin-distribution, inget build target och ingen release asset.
