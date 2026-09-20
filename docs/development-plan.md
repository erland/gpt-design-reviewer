# Design Reviewer – Development Plan

Version: 0.1  
Status: In implementation – steps 1–18 completed  
Profile: zip_first_advanced

## 1. Syfte

Design Reviewer ska hjälpa användaren att genomföra en strukturerad design review av ett eller flera källkodsträd tillsammans med eventuell dokumentation.

Assistenten ska agera som en erfaren senior utvecklare och mjukvaruarkitekt med fokus på förändringsbarhet, begriplighet, testbarhet, kopplingar, ansvarsfördelning och långsiktig underhållbarhet.

Den ska inte primärt vara en lint- eller kodstilsgranskare. Lokala kodproblem ska endast lyftas när de är symptom på, eller bidrar till, ett större designproblem.

## 2. Primär användarresa

1. Användaren tillhandahåller ett eller flera källkodsträd och eventuell dokumentation.
2. Design Reviewer inventerar materialet och skapar en bild av systemets struktur.
3. För små projekt kan analysen genomföras sammanhängande.
4. För större projekt delas analysen upp i flera steg.
5. Assistenten identifierar designproblem, styrkor och områden som behöver mer evidens.
6. Assistenten skapar en nedladdningsbar `design-review.md`.
7. Assistenten skapar en nedladdningsbar `recommended-solution-strategy.md`.
8. Assistenten skapar en nedladdningsbar `implementation-plan.md`.
9. Implementationsplanen ska vara uppdelad så att varje steg kan genomföras av en LLM i en prompt.
10. Vid flerstegsanalys ska användaren kunna fortsätta med exempelvis `Gör nästa steg`.

## 3. Analysområden

Design Reviewer ska kunna analysera bland annat:

- separation of concerns,
- cohesion inom moduler och komponenter,
- koppling mellan moduler,
- beroenderiktningar,
- cirkulära beroenden,
- stora filer, klasser, komponenter och funktioner,
- ansvar som samlats i controllers, services eller UI-komponenter,
- domänlogik i fel lager,
- duplicerad eller parallell logik,
- överdriven specialfallslogik,
- svårtestad design,
- implicit eller global state,
- API- och datamodeller som skapar onödig koppling,
- frontend-state och komponentstruktur,
- integrationsgränser,
- lagerindelning,
- inkonsekventa arkitekturmönster,
- död eller historiskt betingad struktur,
- design som gör sannolika framtida förändringar onödigt dyra,
- krav eller användarflöden som driver oproportionerligt mycket teknisk komplexitet.

Assistenten får föreslå mindre krav- eller UI-förändringar när de tydligt kan förbättra användarupplevelsen eller förenkla implementationen utan att försämra systemets avsedda nytta.

## 4. Evidensprincip

Varje viktig observation ska vara spårbar till konkret evidens, exempelvis:

- fil,
- modul,
- klass,
- funktion,
- beroende,
- dokumenterad arkitektur,
- återkommande struktur i flera delar av kodbasen.

Observationer ska klassificeras efter evidensnivå:

- verifierat designproblem,
- starkt indicium,
- möjlig förbättring,
- behöver mer information.

Assistenten ska undvika att dra slutsatsen att exempelvis en stor fil automatiskt är dålig design.

## 5. Positiva observationer

Design Reviewer ska även identifiera strukturer som fungerar bra och bör bevaras under refaktorering.

Dessa ska kunna uttryckas som exempelvis:

- design strengths,
- constraints to preserve,
- stable boundaries,
- successful abstractions.

Syftet är att undvika att senare förbättringsarbete förstör fungerande design.

## 6. Leveransartefakter

### 6.1 `design-review.md`

Rapporten ska beskriva vad som hittats och varför det spelar roll.

Varje betydande observation bör innehålla:

- ID,
- titel,
- berörda delar,
- observation,
- evidens,
- varför det är ett problem,
- konsekvens,
- allvarlighetsgrad,
- evidensnivå,
- sannolikt framtida förändringstryck,
- ungefärlig åtgärdsrisk,
- vad som bör ske innan vidareutveckling,
- relation till andra observationer.

Rapporten ska även innehålla:

- systemöversikt,
- viktigaste styrkor,
- viktigaste riskområden,
- områden som inte kunnat bedömas,
- sammanfattning.

### 6.2 `recommended-solution-strategy.md`

Strategin ska prioritera åtgärder efter en samlad bedömning av:

- förväntad nytta,
- framtida förändringsbehov,
- risk,
- kostnad/omfattning,
- möjliggörande effekt för senare steg,
- beroenden mellan åtgärder,
- sannolik påverkan på användare och systembeteende.

Principer:

- hög nytta + låg risk prioriteras normalt högt,
- låg nytta + hög risk prioriteras normalt lågt,
- möjliggörande åtgärder kan prioriteras före allvarligare problem,
- beroenden ska styra ordningen,
- stora riskfyllda omskrivningar ska inte rekommenderas när stegvis förbättring är rimligare.

Strategin ska även ange strukturer som bör bevaras.

### 6.3 `implementation-plan.md`

Planen ska härledas från den rekommenderade lösningsstrategin.

Varje steg ska vara möjligt att genomföra av en LLM i en prompt och innehålla:

- stegnummer,
- mål,
- motiv,
- berörda delar,
- konkreta förändringar,
- uttryckliga avgränsningar,
- beroenden,
- verifiering,
- klart-kriterier,
- risknotering vid behov.

Planen ska kunna användas av samma assistent eller en separat implementationsassistent med kommandot `Gör nästa steg`.

## 7. Analysflöde

För mindre projekt:

1. inventering,
2. systemförståelse,
3. hotspot-analys,
4. design review,
5. lösningsstrategi,
6. implementationsplan.

För större projekt kan följande interna steg användas:

1. inventera repositories, källkodsträd och dokumentation,
2. identifiera teknikstack och huvudkomponenter,
3. kartlägg ansvar och beroenden,
4. identifiera hotspots,
5. analysera backend,
6. analysera frontend,
7. analysera data, API och integrationer,
8. analysera tester och förändringsbarhet,
9. korsanalysera observationer,
10. färdigställ design review,
11. skapa lösningsstrategi,
12. skapa implementationsplan.

Assistenten ska själv avgöra när ett projekt behöver flerstegsanalys.

## 8. State och återupptagning

Eftersom större analyser kan behöva flera prompts kräver projektet ett explicit workspace/state-kontrakt.

State ska minst kunna hålla reda på:

- analyserade källkodsträd,
- analyserad dokumentation,
- identifierad systemstruktur,
- redan analyserade områden,
- kvarvarande analysområden,
- preliminära observationer,
- verifierade observationer,
- öppna frågor/evidensluckor,
- aktuellt analyssteg,
- genererade artefakter.

Chatthistorik ska inte vara enda sanningskälla när runtime tillåter persistent workspace.

## 9. Canonical capabilities

Projektets plattformsneutrala capability-kontrakt ska minst omfatta:

1. `source_tree_ingestion`
   - läsa ett eller flera källkodsträd.

2. `documentation_ingestion`
   - läsa tillhörande teknisk och funktionell dokumentation.

3. `codebase_inventory`
   - inventera teknik, struktur och huvudsakliga komponenter.

4. `architecture_inference`
   - härleda sannolik arkitektur och ansvarsfördelning.

5. `design_hotspot_detection`
   - identifiera delar som motiverar fördjupad analys.

6. `design_review_analysis`
   - analysera designproblem och styrkor.

7. `evidence_tracking`
   - knyta observationer till konkret evidens och confidence.

8. `cross_tree_analysis`
   - analysera kopplingar mellan flera repositories/källkodsträd.

9. `solution_prioritization`
   - skapa prioriterad lösningsstrategi utifrån nytta, risk och beroenden.

10. `implementation_planning`
    - bryta ned strategin till prompt-stora genomförandesteg.

11. `markdown_artifact_generation`
    - skapa de tre nedladdningsbara Markdown-artefakterna.

12. `incremental_analysis`
    - fortsätta större analyser stegvis.

13. `resume_analysis`
    - återuppta en påbörjad analys från explicit state när runtimen stödjer det.

## 10. Artifact contract

Obligatoriska slutartefakter:

- `design-review.md`
- `recommended-solution-strategy.md`
- `implementation-plan.md`

Mellanartefakter får användas internt, exempelvis:

- inventory,
- architecture map,
- hotspot list,
- analysis state,
- evidence ledger.

De ska inte belasta användaren om de inte tillför praktiskt värde.

## 11. Tool contract

Design Reviewer behöver huvudsakligen:

- fil- och ZIP-läsning,
- rekursiv inventering av källkod,
- textsökning,
- strukturerad analys,
- skapande av Markdown-filer.

Webbsökning är inte en central capability och ska normalt endast användas när användaren uttryckligen vill jämföra mot aktuell extern dokumentation, ramverksrekommendationer eller standarder.

Bildgenerering behövs inte.

Körbara scripts kan vara värdefulla för deterministisk inventering, exempelvis:

- filstorlekar,
- antal rader,
- katalogstruktur,
- beroendeindikatorer,
- importrelationer,
- enkla komplexitetsindikatorer.

Scripts ska användas som stöd för analysen och inte ersätta semantisk designbedömning.

## 12. Projektprofil

Vald referensprofil: `zip_first_advanced`.

Motivering:

- ett eller flera källkodsträd är central indata,
- ZIP-hantering är viktig,
- analysen kan bli långvarig och flerstegsbaserad,
- flera strukturerade artefakter ska produceras,
- evidens och återupptagning behöver hanteras,
- scripts och schemas är motiverade,
- runtime-adapters behöver hantera filer och state på olika sätt.

Avvikelse:

Projektet är mindre research-tungt än `workflow_research_heavy`; extern webbkunskap är sekundär till den faktiska källkoden.

## 13. Runtime-bedömning

### ChatGPT Chat

Suitability: full  
Activate by default: yes

Bra stöd för:

- bifogade ZIP-filer,
- längre interaktiv analys,
- skapande av nedladdningsbara artefakter,
- stegvis arbete.

### ChatGPT Custom

Suitability: full/reduced depending on file and workspace limits  
Activate by default: yes

Lämplig för den färdiga assistentupplevelsen. Adapter måste vara tydlig kring filgränser, analys i flera steg och hur artefakter levereras.

### Claude Projects

Suitability: full/reduced depending on runtime file/workspace semantics  
Activate by default: yes

Canonical beteende bör kunna portas väl. Adapter och dokumentation behöver beskriva hur större källkodsträd och persistent projektkontext hanteras.

### OpenCode

Suitability: full  
Activate by default: yes

Särskilt lämplig när Design Reviewer arbetar direkt mot lokala kodträd. OpenCode-adaptern bör bevara samma analys- och artefaktkontrakt, inte bli en separat produktvariant.

## 14. Development plan

### Steg 1 – Canonical projektskelett

Mål:
Skapa projektets canonical struktur, metadata och grundläggande README.

Leverans:
- `gpt-project.yaml`
- `README.md`
- `PROJECT.md`
- `STATUS.md`
- `project-status.yaml`
- `docs/development-plan.md`

Klart när:
- strukturen valideras,
- projektstatus kan läsas maskinellt,
- komplett projekt-ZIP kan byggas.

### Steg 2 – Canonical instruktion och beteendemodell

Mål:
Definiera Design Reviewers centrala beteende oberoende av runtime.

Omfattning:
- identitet,
- analysprinciper,
- scope,
- vad som ska ignoreras,
- evidensregler,
- positiva observationer,
- regler för flerstegsanalys,
- regler för krav/UI-förslag,
- prioriteringsprinciper.

Klart när:
- instruktionen täcker kärnflödet,
- kritiskt beteende inte kräver Knowledge-filer.

### Steg 3 – Capability-, artifact-, workspace- och tool-kontrakt

Mål:
Göra projektets viktigaste kontrakt explicita och maskinläsbara.

Omfattning:
- capability contract,
- artifact contract,
- workspace/state contract,
- tool contract.

Klart när:
- kontrakten valideras,
- de tre slutartefakterna finns representerade,
- incremental/resume-flödet finns definierat.

### Steg 4 – Design review-schema och observationmodell

Mål:
Definiera en konsekvent modell för designobservationer.

Omfattning:
- observation-ID,
- severity,
- evidence/confidence,
- impact,
- change pressure,
- remediation risk,
- dependencies,
- affected areas,
- preserve constraints.

Klart när:
- modellen kan användas för både små och stora kodbaser,
- observationerna kan prioriteras utan att reduceras till severity.

### Steg 5 – Analysworkflow för små och stora projekt

Mål:
Definiera hur assistenten inventerar, delar upp och genomför analysen.

Omfattning:
- snabb väg för små projekt,
- progressiv analys för stora projekt,
- hotspot-baserad fördjupning,
- korsanalys mellan kodträd,
- stop/continue-kriterier,
- återupptagning.

Klart när:
- assistenten kan avgöra om fler analyssteg behövs,
- `Gör nästa steg` kan driva analysen framåt deterministiskt.

### Steg 6 – Rapportmall för `design-review.md`

Mål:
Skapa canonical struktur för design review-rapporten.

Klart när:
- rapporten tydligt separerar fakta, evidens, konsekvens och rekommendation,
- styrkor och osäkerheter finns med,
- rapporten fungerar som input till strategin.

### Steg 7 – Prioriteringsmodell och lösningsstrategi

Mål:
Definiera hur observationer omvandlas till en prioriterad lösningsstrategi.

Omfattning:
- nytta,
- risk,
- förändringstryck,
- beroenden,
- möjliggörande effekt,
- stegvis refaktorering,
- krav/UI-alternativ.

Klart när:
- strategin inte bara sorterar på severity,
- beroenden kan ändra ordningen,
- låg-risk/high-value-förbättringar kan prioriteras korrekt.

### Steg 8 – Mall för `recommended-solution-strategy.md`

Mål:
Skapa canonical struktur för den rekommenderade lösningsstrategin.

Klart när:
- prioriteringen är spårbar till design review,
- bevarandekrav finns med,
- strategin kan användas som direkt input till implementationsplanen.

### Steg 9 – LLM-anpassad implementationsplanering

Mål:
Definiera regler för hur strategin bryts ned till ett steg per prompt.

Omfattning:
- maximal rimlig stegstorlek,
- beroenden,
- avgränsningar,
- verifiering,
- klart-kriterier,
- när ett steg ska delas.

Klart när:
- varje genererat steg går att utföra självständigt i en prompt,
- en genomförandeassistent kan följa planen utan att göra om analysen.

### Steg 10 – Mall för `implementation-plan.md`

Mål:
Skapa canonical struktur för den slutliga genomförandeplanen.

Klart när:
- varje steg innehåller mål, konkreta ändringar, avgränsning, beroenden och verifiering,
- `Gör nästa steg` kan användas som primärt fortsättningskommando.

### Steg 11 – Deterministiska analysverktyg

Mål:
Lägga till små scripts där deterministisk kodinventering förbättrar kvaliteten.

Möjliga funktioner:
- fil- och katalogstatistik,
- stora filer,
- stora funktioner där språkstöd är rimligt,
- import-/dependency-indikatorer,
- enkel dupliceringsindikering,
- repository inventory.

Klart när:
- verktygen endast producerar evidens,
- de inte gör arkitekturbedömningar själva,
- fel i ett verktyg inte gör kärnflödet obrukbart.

### Steg 12 – Eval- och testfall

Mål:
Skapa representativa tester för assistentens beteende.

Testfall bör täcka:

- liten välstrukturerad kodbas,
- stor monolitisk kodbas,
- flera repositories,
- stora filer utan verkligt designproblem,
- hög severity men riskfylld fix,
- enabling refactoring som bör komma först,
- UI/kravförenkling som alternativ till teknisk komplexitet,
- otillräcklig evidens,
- positiva designmönster som ska bevaras.

Klart när:
- kärnbeteendet kan regressionskontrolleras.

### Steg 13 – ChatGPT Chat-adapter

Mål:
Bygga Chat ZIP-runtime från canonical kontrakt.

Klart när:
- ZIP-inmatning fungerar enligt kontraktet,
- flerstegsanalys fungerar,
- Markdown-artefakter kan levereras,
- runtimevalidering passerar.

### Steg 14 – ChatGPT Custom-adapter

Mål:
Bygga Custom GPT-distribution från samma canonical kontrakt.

Klart när:
- kritiskt beteende ryms i instruktionen,
- Knowledge används endast där det är lämpligt,
- plattformsspecifika begränsningar dokumenteras,
- validering passerar.

### Steg 15 – Claude Projects-adapter

Mål:
Bygga Claude-portabel runtime från samma canonical kontrakt.

Klart när:
- analysbeteende och artefaktkontrakt bevaras,
- fil- och workspacebegränsningar dokumenteras,
- validering passerar.

### Steg 16 – OpenCode-adapter

Mål:
Bygga OpenCode-runtime för direkt arbete mot kodträd.

Klart när:
- samma canonical reviewmodell används,
- lokala filverktyg mappas utan att ändra produktbeteendet,
- validering passerar.

### Steg 17 – Runtime parity

Mål:
Verifiera att samtliga aktiverade runtimes implementerar samma kärnprodukt.

Klart när:
- capabilities jämförts,
- artefakter jämförts,
- state/resume-beteende jämförts,
- verkliga plattformsskillnader dokumenterats.

### Steg 18 – Project hygiene och slutrevision

Mål:
Rensa projektet och genomföra samlad kvalitetsgranskning.

Omfattning:
- överflödiga filer,
- dubblerat innehåll,
- stale instruktioner,
- inkonsekventa namn,
- dokumentationsgap,
- oanvända scripts/schemas.

Klart när:
- hygiene inte innehåller blockerare.

### Steg 19 – Release readiness

Mål:
Genomföra samlad releasekontroll.

Kontroller:
- lint,
- schemas,
- tests/evals,
- build,
- distributionsvalidering,
- runtime parity,
- hygiene,
- README och användarinstruktioner.

Klart när:
- inga blockerande resultat återstår.

### Steg 20 – Release-konfiguration

Mål:
Aktivera standardiserad GitHub CI och release-byggning.

Omfattning:
- CI,
- release workflow,
- versionsstyrning från release-tag,
- checksummor,
- distributionsartefakter.

Klart när:
- projektet kan skapa reproducerbara releaseartefakter.

## 15. Rekommenderat nästa steg

Steg 1–19 är genomförda. Canonical produkt, samtliga fyra peer runtimes, evals, parity, hygiene och release-readiness är validerade utan blockerande fynd.

Nästa genomförandesteg är **Steg 20 – Release-konfiguration**. Där aktiveras GitHub Actions för CI och release-byggning, versionsstyrning från release-tag samt publicering av checksummor och distributionsartefakter.

Efter steg 20 ska projektet kunna skapa reproducerbara releaseartefakter automatiskt på GitHub.


## Slutstatus

Alla 20 planerade steg är genomförda. Projektet har canonical produktmodell, fyra peer runtimes, evals, parity-kontroll, release-readiness och GitHub Actions för CI/release.
