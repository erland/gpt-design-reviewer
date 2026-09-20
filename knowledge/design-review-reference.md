# Design Reviewer – stödreferens

Den här filen är stödmaterial för Custom GPT och ersätter inte kärninstruktionen.

## Evidensdimensioner
- severity: konsekvens om problemet lämnas orört
- evidence level: styrkan i underlaget
- confidence: säkerhet i tolkningen
- change pressure: sannolik framtida förändring
- remediation risk: risk i själva åtgärden
- remediation effort: ungefärlig omfattning
- enabling effect: hur mycket åtgärden förenklar senare arbete

## Spårbarhet
Behåll kedjan `DR-*` → `RS/VA/UX-*` → `IP-*`.

## Kontrollfrågor
- Är detta ett faktiskt designproblem eller bara en hotspot?
- Vilken konkret evidens stödjer slutsatsen?
- Finns en enklare, lägre risk-väg?
- Finns fungerande design som måste bevaras?
- Är krav/UX-förändringen explicit och godkännandekrävande?
