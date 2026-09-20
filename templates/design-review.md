# Design Review

> Canonical rapportstruktur. Ta bort instruktionstext och tomma delar i en faktisk leverans. Hitta inte på observationer för att fylla mallen.

## Sammanfattning

Beskriv den övergripande designbilden, de mest materiella riskerna, de viktigaste styrkorna, eventuella utvecklingsgrindar och de största begränsningarna i evidensen.

## Omfattning och underlag

Redovisa vilka källkodsträd och dokument som granskats, vad som saknats eller undantagits, analysläge (focused/progressive) och viktiga avgränsningar.

## Systemöversikt

Beskriv teknikstack, huvudkomponenter, ansvar, viktiga beroenden samt centrala data- eller exekveringsflöden. Markera antaganden som antaganden.

## Styrkor och strukturer som bör bevaras

Beskriv designstyrkor, stabila gränser, lyckade abstraktioner, användbara testseams och relevanta användaregenskaper som framtida ändringar bör bevara.

## Översikt över observationer

Ge ett kompakt index över observationerna med ID, titel, typ, severity, evidensnivå, förändringstryck och eventuell utvecklingsgrind. Detta är inte den slutliga åtgärdsordningen.

## Detaljerade observationer

Använd följande struktur för varje betydande observation.

### DR-NNN – Observationens titel

**Berörda delar:** Ange källkodsträd, sökvägar, symboler och roller.

**Observation:** Beskriv vad som faktiskt observerats.

**Evidens:** Redovisa konkreta kod-, beroende-, dokumentations- eller flödesevidens.

**Varför detta spelar roll:** Förklara designresonemanget utan att blanda ihop det med observerade fakta.

**Konsekvens:** Beskriv konkret framtida eller nuvarande påverkan.

**Allvarlighetsgrad:** Critical / High / Medium / Low / Informational enligt observationskontraktet.

**Evidensnivå och säkerhet:** Ange evidensnivå och confidence separat.

**Påverkan:** Beskriv relevanta dimensioner såsom maintainability, changeability, testability, reliability, user experience och delivery risk.

**Förändringstryck:** High / Medium / Low / Unknown med kort motivering.

**Åtgärdsrisk och omfattning:** Redovisa remediation risk och remediation effort utan att bestämma den slutliga prioriteringen.

**Möjliggörande effekt:** Beskriv om en åtgärd kan förenkla eller avriska senare arbete.

**Före vidareutveckling:** Ange must fix before / should fix before / can fix in parallel / can defer / not applicable och vilken typ av vidareutveckling som avses.

**Relationer:** Referera andra `DR-*`-observationer och förklara relationen.

**Bevara:** Ange beteenden, gränser, abstraheringar eller UX-egenskaper som en åtgärd inte bör förstöra.

**Föreslagen riktning:** Beskriv endast en övergripande lösningsriktning. Den prioriterade åtgärdssekvensen hör hemma i lösningsstrategin.

**Ytterligare verifiering:** Ta med detta endast när mer information skulle kunna stärka, försvaga eller falsifiera observationen.

## Tvärgående mönster

Syntetisera återkommande orsaker och relationer som inte blir tydliga om observationerna läses var för sig. Undvik att duplicera detaljobservationerna.

## Vad bör åtgärdas före vidareutveckling

Lista endast verkliga utvecklingsgrindar med observation-ID och vilken typ av arbete de blockerar eller bör föregå. Definiera inte den fullständiga refaktoreringsordningen här.

## Osäkerheter och evidensluckor

Beskriv observationer som behöver mer information, viktiga antaganden, saknad runtime-/driftkontext samt relevanta verifieringsåtgärder.

## Avgränsningar

Beskriv vad som inte bedömts, vilka lågnyttiga lokala frågor som medvetet utelämnats och andra kända begränsningar.

## Underlag för lösningsstrategin

Sammanfatta kandidatteman för åtgärder, viktiga beroenden mellan observationer, preserve constraints och potentiella enabling changes. Presentera inte den slutliga rangordnade lösningssekvensen eller prompt-stora implementationssteg.
