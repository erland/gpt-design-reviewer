# OpenAI Plugin compatibility assessment – Design Reviewer / GPT Byggaren 1.5.0

## Beslut

OpenAI Plugin är en **aktiv peer runtime** för Design Reviewer.

Målbilden är:

- status: `active`
- compatibility: `equivalent_runtime_dependent`
- advisory_only: `false`

Bedömningen bygger på att Design Reviewers semantiska kärnflöde inte kräver code execution. Kärnflödet kräver däremot faktisk host-capability för filesystem, ZIP/archive input och persistent workspace/state.

## Runtimekrav

För full faktisk körning behöver hosten:

1. filesystem read/write för ett eller flera källkodsträd,
2. ZIP/archive extraction för ZIP-baserad input,
3. persistent workspace/state utanför chat memory,
4. läsning och uppdatering av `project-status.yaml` som auktoritativ state,
5. stöd för `Gör nästa steg` från explicit checkpoint,
6. faktisk skrivning av `design-review.md`, `recommended-solution-strategy.md` och `implementation-plan.md`,
7. structured data för observations- och evidensstate.

## Code execution

Code execution är **recommended**, inte required för den semantiska Design Review-kärnan.

Pluginen paketerar `scripts/analyze_source_tree.py` samt dess `scripts/lib/`-beroenden som script-resurs. När kompatibel code execution finns ska scriptet användas som reproducerbart evidensstöd.

Om code execution saknas ska pluginen **degrade** ärligt: fortsätt semantisk analys med faktisk filåtkomst, men markera script-härledd evidens som unavailable. Scriptresultat får aldrig simuleras.

## Parity

`equivalent_runtime_dependent` betyder att canonical beteende, artifacts och state-semantik kan bevaras när hosten erbjuder de required capabilities som uppgiften behöver.

Det gäller särskilt:

- källkodsträd och dokumentation analyseras från faktisk input,
- persistent workspace/state används,
- `project-status.yaml` förblir auktoritativ,
- `Gör nästa steg` återupptar från explicit state,
- de tre slutartefakterna skapas som faktiska filer,
- evidence gate och DR/RS/VA/UX/IP-semantik bevaras.

## No-false-PASS

Unrun verification får aldrig redovisas som PASS.

Om en host-capability som behövs för en viss operation saknas ska begränsningen redovisas explicit. Design Reviewer får inte påstå att ett helt repository analyserats, att persistent state muterats eller att ett script körts om det inte faktiskt skett.

## Release

OpenAI Plugin ingår i build och release som:

`design-reviewer-plugin-<version>.zip`

Distributionen innehåller skill, references, assets, runtime contract och den deklarerade runtime script-resursen.
