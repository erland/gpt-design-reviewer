# Runtime parity – Design Reviewer

Status: PASS  
Scope: ChatGPT Chat, ChatGPT Custom GPT, Claude Projects, OpenCode och OpenAI Plugin.

## Canonical parity

Alla fem runtimes använder samma canonical kontrakt för:

- capabilities,
- de tre slutartefakterna,
- workspace-/analysis-state,
- checkpoint och resume semantics,
- evidens- och observationsmodell,
- prioriterings- och implementationsprinciper.

Automatisk parity-kontroll verifierar att runtime-kontrakten innehåller identiska `capabilities`, `artifacts` och `workspace_state`.

## Gemensamma slutartefakter

Alla runtimes ska producera:

1. `design-review.md`
2. `recommended-solution-strategy.md`
3. `implementation-plan.md`

Samma `DR-*`, `RS-*`, `VA-*`, `UX-*` och `IP-*`-semantik gäller i samtliga runtimes.

## Resume-beteende

`Gör nästa steg` ska i samtliga runtimes fortsätta från explicit analysstate/checkpoint och inte göra om redan verifierad analys utan en konkret invalidation-trigger.

Skillnaden mellan runtimes ligger i hur state faktiskt lagras eller representeras, inte i vilket state som krävs av Design Reviewer.

## Verkliga adapter-skillnader

| Område | ChatGPT Chat | Custom GPT | Claude Projects | OpenCode | OpenAI Plugin |
| --- | --- | --- | --- | --- | --- |
| Canonical reviewbeteende | Fullt | Fullt via kompilerad kärninstruktion | Fullt | Fullt | Fullt när required host-capabilities finns |
| Direkt arbete mot bifogade filer | Runtime-stöd | Runtime-/Builder-beroende | Projektkontext | Direkt workspace | Host filesystem |
| Inbäddat deterministiskt analysscript | Ja | Reducerat/ej inbäddat som körbart script | Nej | Ja, som custom tool | Ja, som script-resurs |
| Fallback utan script | Filläsning/sökning | Filläsning/sökning | Filläsning/sökning | Filläsning/sökning | Filläsning/sökning |
| Full canonical instruktion distribuerad | Ja | Nej, komprimerad till plattformsgräns | Ja | Ja | Ja, i skill |
| Stöd-Knowledge/references | Ja | Ja | Ja | Ja | Ja, som references/assets |

## Custom GPT

Custom GPT är den enda runtimen där canonical instruktion behöver kompileras ned för instruktionsgränsen. Kritiska beteenden ligger fortfarande i `builder/instructions.md`; Knowledge används endast som stödreferens. Detta är en representationsskillnad, inte en produktvariant.

## Claude Projects

Claude Projects-paketet bäddar inte in lokalt command execution för `analyze_source_tree.py`. Det deterministiska verktyget är därför reducerat och reviewn använder den canonical fallbacken: inventering, sökning och semantisk filläsning.

## OpenCode

OpenCode är workspace-first och kan exponera source-tree-inventeringen som ett custom tool. Det ger starkare lokal verktygsintegration men ändrar inte slutsatsreglerna: verktygsresultat är evidens/hotspot-signaler, aldrig automatiska designproblem.

## OpenAI Plugin

OpenAI Plugin är skills-first och har `equivalent_runtime_dependent` parity. Filesystem read/write, archive extraction och persistent workspace/state måste tillhandahållas av hosten. `analyze_source_tree.py` och dess `scripts/lib/`-beroenden följer med som script-resurser. Code execution är rekommenderad evidensförstärkning; om den saknas används den canonical fallbacken med semantisk filläsning/sökning och scriptresultat simuleras aldrig.

## ChatGPT Chat

Chat-paketet innehåller canonical instruktion, schemas, mallar och source-tree-script. Runtime-contractet är samma canonical kontrakt som de andra adaptrarna.

## Parity gate

Följande är blockerande parity-avvikelser:

- olika canonical capabilities,
- olika slutartefakter eller artifact semantics,
- olika workspace/checkpoint-state,
- runtime-specifika severity/prioriteringsregler,
- runtime-specifika observationstyper som förändrar produktens betydelse,
- `Gör nästa steg` med annan semantik än canonical resume-flödet.

Skillnader i verktygsåtkomst, packaging, instruktionens representation och filsystemintegration är tillåtna när canonical fallback-beteendet bevaras och skillnaden dokumenteras.

## Automatisk kontroll

Kör efter att alla runtime-distributioner byggts:

```bash
python3 scripts/check_runtime_parity.py --project-root .
```

Förväntat resultat: `RUNTIME PARITY: PASS`.
