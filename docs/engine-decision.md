# Beslut: ingen separat Engine ZIP

## Kontext
Design Reviewer har ett valfritt deterministiskt källkodsinventeringsskript, `scripts/analyze_source_tree.py`, som använder `lib/source_inventory.py`. Övriga skript är i första hand bygg-, test- och valideringsverktyg som hör till projektkällan, inte funktioner användaren behöver exekvera i ett installerat plugin.

## Beslut
**Ingen separat Engine-modul eller Engine ZIP i denna version.** Källkodsinventeringen ligger intill `source-analysis`-Skillen med sina Pythonberoenden. I miljöer utan kompatibel kodexekvering sker inventering med filsystemets läs-/sökfunktioner och evidensbegränsningen redovisas. Plugin och Chat ska inte behöva ladda ned en separat Engine för kärngranskning.

## Motiv
- Undviker dubblerat körlager, materialiseringskrav och en onödig versionsbunden artefakt.
- Det finns bara ett litet runtimeverktyg med tydlig Pythonimport och möjlighet att arbeta manuellt.
- Byggskript och kvalitetstester hör hemma i CI/projekt-ZIP, inte i varje runtime.
- En Engine är motiverad först om flera obligatoriska verktyg måste köras tillsammans, kräver stora externa beroenden eller har delat state som inte rimligen kan hanteras via portabla resurser.

## Framtida omprövningskriterier
Om runtime kräver reproducerbar AST-analys över flera språk, resurskrävande indexering, dedikerade beroenden eller exekvering som är blockerande för flödet: inför versionsmatchad Engine ZIP med självtest, dokumenterad fallback och hostbaserad acceptans.

## Verifiering
Testa separat att `source-analysis` har skript och `lib/source_inventory.py`, att de fyra övriga Skillsen inte oavsiktligt kräver exekveringsskript och att ingen Engine-länk används.
