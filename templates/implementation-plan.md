# Implementationsplan

> Canonical rapportstruktur. Ta bort instruktionstext och tomma underpunkter i en faktisk leverans. Planen ska kunna användas direkt av samma eller en separat LLM ett steg per prompt utan att design review eller lösningsstrategi behöver göras om.

## Genomförandeplan

Beskriv planens syfte, vilken `recommended-solution-strategy.md` den bygger på, att arbetsmodellen är **en prompt = ett sammanhängande checkpoint**, samt vilka övergripande constraints som gäller.

Ange också vad som krävs för att hela planen ska betraktas som genomförd.

## Regler för genomförande

- Följ `IP-*`-ordningen och hårda beroenden om inte ny evidens kräver en dokumenterad planändring.
- Utför inte senare steg opportunistiskt om de inte krävs för att hålla aktuellt steg giltigt.
- Bevara angivna preserve constraints och användarsynliga beteenden.
- Utför `VA-*` före implementation som bygger på valideringens resultat.
- Implementera inte `UX-*` innan det uttryckligen accepterats.
- Om ett steg visar sig vara väsentligt större än planerat: stanna vid ett koherent checkpoint, dela återstående arbete och uppdatera planen.

## Gemensam verifieringsbas

Dokumentera kända bygg-, test-, lint- och andra verifieringskommandon som flera steg kan återanvända.

Beskriv även övergripande regressionsförväntningar, arkitekturkontroller och eventuella migrations-/recoverykrav.

## Översiktlig genomförandeordning

Lista `IP-*`-stegen i rekommenderad ordning. Gruppera dem i faser om det förbättrar begripligheten, men behåll den exakta exekveringsordningen synlig.

Markera:

- hårda beroenden,
- steg som säkert kan köras parallellt,
- blockerade steg,
- beslut eller valideringar som måste ske innan vissa steg.

## Genomförandesteg

Använd följande struktur för varje steg.

### IP-NNN – Stegets titel

**Status:** `planned` / `in_progress` / `blocked` / `completed` / `skipped` / `superseded`.

**Härledd från:** Referera relevanta `RS-*`, `VA-*` eller uttryckligen accepterade `UX-*`.

**Relaterade observationer:** Referera relevanta `DR-*` när det tillför spårbarhet.

**Mål:** Beskriv vilket konkret resultat detta checkpoint ska uppnå.

**Motiv:** Förklara varför steget finns och varför det ligger här i ordningen. Återge inte hela strategianalysen.

**Scope:** Beskriv subsystem, ansvar, gränssnitt och sannolika filer/symboler som ingår när de är kända.

**Förändringar:** Lista de konkreta ändringar som ska genomföras. Skilj obligatoriska ändringar från eventuella valfria förbättringar.

**Gör inte:** Ange explicita non-goals, senare steg och närliggande cleanup som inte ska tas med nu.

**Förutsättningar:** Ange tidigare `IP-*`, `VA-*`, beslut, miljökrav eller annan prerequisite som måste vara uppfylld.

**Bevara:** Ange beteende, API-kontrakt, datakompatibilitet, UX, arkitekturgränser eller andra egenskaper som inte får försämras.

**Beteendeeffekt:** Ange om steget ska vara beteendebevarande eller avsiktligt ändra beteende. Beskriv den avsedda synliga effekten när beteende ändras.

**Verifiering:** Ange riktade kontroller, regressionskontroller och strukturella/arkitekturmässiga kontroller. Använd kända projektkommandon när de finns.

**Klart när:** Ange observerbara eller binära kriterier för att checkpointen ska få status `completed`.

**Risknotering:** Beskriv särskilda risker, rollback-/recoverybehov, migrationsfrågor eller tecken på att steget bör delas ytterligare.

**Fortsättning:** Ange vilket nästa steg som normalt blir exekverbart när detta steg är klart och vad som ska sparas i checkpointen.

## Besluts- och valideringsgrindar

Sammanställ olösta `VA-*`, produkt-/UX-beslut och andra grindar som kan blockera senare `IP-*`-steg.

För varje grind, ange vilka steg som påverkas och vilken fallback eller alternativ väg som gäller om beslutet inte tas eller valideringen ger ett annat resultat än väntat.

## Checkpoint-logg

Uppdatera denna del efter genomförda steg. Spara sammanfattad verifiering och beslut, inte dold intern tankegång.

| Steg | Resultat | Verifiering | Avvikelse/ny evidens | Planpåverkan |
|---|---|---|---|---|
| IP-NNN | completed / blocked / ... | Kort evidens | Kort beskrivning | Ingen / uppdaterade beroenden / nytt steg / etc. |

Dokumentera även nya prerequisites och planändringar som upptäcks under implementationen.

## Återupptagning

**Nästa ofullständiga exekverbara steg:** `IP-NNN`.

**Förutsättningsstatus:** Sammanfatta relevanta prerequisites.

**Aktuella blockerare:** Ange blockerare eller `Inga`.

**Relevanta checkpoint-noteringar:** Ta endast med information som nästa genomförandesteg faktiskt behöver.

**Standardkommando:** `Gör nästa steg`.

När användaren ger standardkommandot ska nästa exekverbara steg genomföras från denna checkpoint utan att design review och lösningsstrategi görs om.
