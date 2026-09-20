# {{GPT_NAME}} – OpenCode

Version: {{VERSION}}

Detta paket är OpenCode-distributionen av **{{GPT_NAME}}**. Den bygger på samma canonical design-review-kontrakt som ChatGPT Chat, Custom GPT och Claude Projects.

## Installation

1. Packa upp ZIP-filen i ett eget workspace eller kopiera innehållet till roten av det workspace där reviewn ska köras.
2. Starta OpenCode i workspace-roten.
3. `AGENTS.md` innehåller Design Reviewers runtime-instruktioner.
4. `.opencode/skills/design-review-workflow/SKILL.md` beskriver det återanvändbara reviewflödet.
5. `.opencode/tools/` innehåller genererade wrappers för canonical scripts.

## Användning

Lägg ett eller flera källkodsträd och eventuell dokumentation i eller under workspace. Be sedan om en design review. För större projekt arbetar Design Reviewer progressivt; fortsätt då med **`Gör nästa steg`**.

De tre obligatoriska slutartefakterna är:

- `design-review.md`
- `recommended-solution-strategy.md`
- `implementation-plan.md`

## OpenCode-specifikt

OpenCode kan arbeta direkt mot lokala filer och köra det deklarerade deterministiska analysverktyget via en genererad custom tool. Verktygets mätvärden är endast evidensstöd och får aldrig ensamma bli designobservationer.

Skrivande och generell shell-användning kräver enligt den genererade OpenCode-konfigurationen användargodkännande, medan det icke-muterande analysverktyget får köras direkt.
