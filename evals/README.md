# Eval suite

`evals/cases/*.yaml` är canonical regressionsscenarier för Design Reviewer.

Varje fall beskriver:

- scenario och signaler,
- beteenden som ska observeras,
- beteenden som uttryckligen är förbjudna,
- coverage-tags som kopplar fallet till suite-kontraktet.

Kör den deterministiska nivån med:

```bash
python scripts/run_evals.py --project-root .
```

Den deterministiska nivån kör ingen LLM. Den validerar evalfilerna, täckningen och suite-invariants. När runtime-adaptrar finns kan samma scenarier återanvändas för modellbaserade beteende-evals.
