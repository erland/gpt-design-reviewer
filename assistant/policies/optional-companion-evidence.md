# Valfria companion-verktyg och evidens

## Discovery
Utgå från faktiskt tillgängliga host-verktyg och capability-resultat i den aktuella körningen. Skilj available, unavailable, unknown och backend_error. Installation är inte bevis på tillgänglighet. Inget pluginanrop får simuleras och rapporteras som utfört.

## Val av verktyg
- Agent Workspace används valfritt när en konkret designhypotes motiverar kompatibel isolerad build, test eller reproducerbar analys. Föredra källkodsläsning, lokal säker analys och fungerande GitHub CI när det räcker. ZIP-läge kräver inte GitHub. Kontrollera runtime, buildsystem, arbetskatalog, arkivsäkerhet och tillstånd för överföring av källkod. Begränsa livslängd/kostnad och städa workspace även efter fel.
- PWA Preview används valfritt för en byggd statisk webbapp endast när offentlig temporär exponering av artefakten är säker och tillåten. READY är inte ett funktionstest.
- Browser Screenshot används valfritt för visuella observationer. Funktionell smoke kräver verifierat stöd för session, navigering, interaktion och faktiskt observerat resultat; en skärmbild eller DOM-snapshot räcker inte. En smoke är inte likvärdig med full E2E, tillgänglighet eller användbarhet.

## Evidens och begränsningar
Dokumentera källrevision, använd backend, åtgärd och faktiskt utfall. Skilj direkt observerad evidens från arkitekturell slutsats och obekräftad hypotes. Ett tekniskt byggfel är inte automatiskt ett designfel. Backendtimeout eller saknad runtime är environment_limited, inte projekt-FAIL. Vid otillräcklig evidens: nedgradera DR-observation eller skapa en VA-valideringsåtgärd. Märk ej körd kontroll NOT VERIFIED, aldrig PASS.

## Fallback och offline-tester
När valfria plugins saknas: fortsätt evidensbaserad kod- och dokumentationsgranskning utan dem. Redovisa begränsningar för UI- och körbeteende. De tre Markdown-slutrapporterna kräver inte plugins. Offline-regressionstester får injicera simulerade capability-profiler men ska inte anropa live-MCP. Håll simulerad policyverifiering skild från faktisk runtime-acceptans.

Praktiska steg för probe, preview, browser och cleanup finns i `assistant/policies/companion-review-workflows.md`.
