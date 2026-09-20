# Rekommenderad lösningsstrategi

> Canonical rapportstruktur. Ta bort instruktionstext och tomma underpunkter i en faktisk leverans. Strategin ska vara spårbar till `design-review.md` men inte duplicera hela design review-rapporten.

## Rekommenderad strategi

Sammanfatta den övergripande riktningen, vilka resultat strategin ska uppnå och den viktigaste logiken bakom ordningen. Lyft större constraints som påverkar sekvensen.

## Underlag och spårbarhet

Ange vilken design review strategin bygger på, vilka `DR-*`-observationer som varit styrande, relevanta utvecklingsgrindar och eventuella evidensbegränsningar som fortfarande påverkar beslutet.

## Ordnings- och beroendekrav

Beskriv hårda prerequisites, evidence gates, preserve constraints samt migrerings- eller leveransbegränsningar som styr vad som kan göras när.

## Prioriterade åtgärdsteman

Använd följande struktur för varje `RS-*`-tema.

### RS-NN – Åtgärdstemats titel

**Prioritet:** P0 / P1 / P2 / P3 / PX.

**Adresserar:** Referera relevanta `DR-*`-observationer.

**Mål:** Beskriv vilket designresultat temat ska åstadkomma.

**Varför nu:** Förklara varför temat ligger på denna plats i strategin, inklusive change pressure eller development gates.

**Nytta:** Beskriv vilken återkommande designkostnad, leveransrisk eller användarfriktion som reduceras.

**Evidens och säkerhet:** Beskriv hur starkt beslutsunderlaget är och om osäkerhet påverkar åtgärden.

**Kostnad:** Beskriv ungefärlig omfattning utan att likställa stor arbetsmängd med hög risk.

**Risk:** Beskriv beteende-, migrerings-, data-, API-, rollback- och testbarhetsrisker som är relevanta.

**Möjliggörande effekt:** Beskriv vilka senare teman som blir enklare, säkrare eller billigare efter detta tema.

**Beroenden:** Ange prerequisites, teman som detta blockerar/låser upp samt eventuell säker parallellisering.

**Bevara:** Ange beteenden, gränser, abstraheringar och UX-egenskaper som inte bör försämras.

**Rekommenderad ansats:** Beskriv den tekniska strategin på en övergripande nivå. Bryt inte ned den till prompt-stora implementationsteg här.

**Verifiering:** Beskriv vilken typ av verifiering som behövs för att bedöma att temat lyckats.

**Ordningsmotivering:** Förklara explicit varför temat kommer före eller efter närliggande teman.

## Valideringsåtgärder före beslut

Använd `VA-*` när evidensen ännu inte räcker för att motivera en riskfylld åtgärd.

### VA-NN – Valideringsåtgärd

**Osäkerhet:** Vad vet vi inte tillräckligt säkert?

**Relaterade observationer:** Referera `DR-*`.

**Varför verifiering behövs:** Förklara vilket felbeslut som annars riskeras.

**Valideringsmetod:** Beskriv vilken analys, mätning, kodspårning eller verksamhetsfråga som kan avgöra saken.

**Beslut som möjliggörs:** Ange vilket strategibeslut som kan tas efter verifieringen.

Om inga materiella valideringsåtgärder krävs, säg det kort i stället för att skapa konstgjorda poster.

## Krav- eller UX-alternativ

Använd `UX-*` endast när en ändring av krav eller användarinteraktion realistiskt kan reducera komplexitet eller förbättra användarupplevelsen.

### UX-NN – Krav/UX-alternativ

**Nuvarande komplexitetsdrivare:** Beskriv vilket krav eller flöde som driver teknisk komplexitet.

**Föreslaget alternativ:** Beskriv användar- eller kravförändringen.

**Relaterade observationer:** Referera `DR-*`.

**Vinst för användaren:** Beskriv förbättringar.

**Förlust/tradeoff för användaren:** Beskriv vad som blir sämre eller annorlunda.

**Teknisk effekt:** Beskriv vilken komplexitet som försvinner eller minskar.

**Beslut krävs av:** Ange att detta är ett produkt-/verksamhetsbeslut när så är fallet.

**Teknisk fallback:** Ange rimlig teknisk strategi om alternativet inte accepteras.

## Uppskjutna eller avrådda åtgärder

Redovisa verkliga förbättringar som medvetet skjuts upp eller avråds, varför de inte prioriteras nu och vad som skulle motivera att de tas upp igen.

## Strukturer och egenskaper som ska bevaras

Samla de viktigaste preserve constraints som hela strategin måste respektera: beteenden, stabila gränser, lyckade abstraktioner, användarupplevelse och kontraktuella/operativa egenskaper.

## Rekommenderad ordning

Presentera den strategiska sekvensen med `RS-*`-ID:n. Gruppera gärna i faser om det ökar begripligheten. Förklara varför ordningen är vald och vad som säkert kan göras parallellt.

Detta är fortfarande en strategisk sekvens, inte den prompt-stora genomförandeplanen.

## Underlag för implementationsplanen

Sammanfatta de teman som ska brytas ned i nästa artefakt, hårda beroenden, valideringsprerequisites, preserve constraints, förväntad verifiering och explicita non-goals. Lägg inte in de färdiga implementationstegen här.
