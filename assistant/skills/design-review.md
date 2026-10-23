# Design review

## När den aktiveras
Använd när användaren vill ha en designgranskning eller risk- och observationsrapport, även utan en färdig källinventering.

## Arbetssteg
Skapa först tillräcklig systemförståelse. Bedöm ansvarsfördelning, koppling, abstraktioner, testbarhet, data- och UI-flöden samt ändringsrisk. Skilj verifierat designproblem, starkt indicium, möjlig förbättring och informationsbrist. Sätt separata nivåer för severity, confidence och remediation risk. Dokumentera design som bör bevaras.

## Utdata och överlämning
Leverera `design-review.md` enligt rapportkontraktet med DR-001 och följande ID:n, evidens och bevarandekrav. Godkända DR-ID:n är underlag för `solution-strategy`. Nedgradera ogrundade påståenden.

## Valfri praktisk verifiering
När faktisk exekvering eller UI-observation behövs för en specifik designhypotes, följ `assistant/policies/companion-review-workflows.md` och evidensreglerna i gemensam kärna. Plugins är valfria; rapportera ej utförda kontroller som NOT VERIFIED och använd VA-åtgärd när evidensen inte räcker.
