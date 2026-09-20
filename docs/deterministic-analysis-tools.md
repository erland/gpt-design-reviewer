# Deterministiska analysverktyg

Design Reviewer använder små deterministiska verktyg som **evidensstöd**, inte som arkitekturdomare.

## Source tree inventory

Kör:

```bash
python scripts/analyze_source_tree.py /path/to/source -o evidence/source-inventory.json
```

Verktyget samlar bland annat fil-/katalogstatistik, radräkning, stora filer, stora funktioner för språk där en rimlig scanner finns, importindikatorer och möjliga duplicerade kodblock.

Trösklar kan ändras:

```bash
python scripts/analyze_source_tree.py /path/to/source \
  --large-file-lines 700 \
  --large-function-lines 100 \
  --duplicate-block-lines 10 \
  -o evidence/source-inventory.json
```

## Tolkningsregler

- Storlek är en hotspot, inte ett designfel.
- En importrelation är ett beroendeindicium, inte bevis på olämplig koppling.
- Dupliceringsfingeravtryck är kandidater som måste läsas semantiskt.
- Genererad kod, migrationsfiler, fixtures, vendored kod och konfiguration måste bedömas i sitt sammanhang.
- Ett verifierat `DR-*`-problem kräver fortsatt källkodsläsning och semantisk analys.

Verktyget är best-effort per fil: parse- och läsfel registreras i JSON-resultatet och övrig inventering fortsätter. Om kodexekvering saknas ska Design Reviewer fortsätta med filsystemets list/search/read-funktioner och tydligt ange att deterministiska indikatorer inte kunde samlas in.
