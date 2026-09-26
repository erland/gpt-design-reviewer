# GPT Byggaren 1.5.0 – migreringsplan

Projekt: **Design Reviewer**

Utgångsläge: utvecklingsplan **20/20 complete**, fyra implementerade peer runtimes, canonical kontrakt i `gpt-project.yaml` och releaseautomation via GitHub Actions.

## Mål

Migrera Design Reviewer till GPT Byggaren 1.5.0 utan att förändra produktbeteendet, analysmodellen, resume-semantiken eller de tre canonical slutartefakterna.

## Preserve-first

Följande ska bevaras:

- `assistant/instructions.md` som canonical produktinstruktion.
- `gpt-project.yaml` som centralt capability/artifact/workspace/tool-kontrakt.
- DR-*, RS-*, VA-*, UX-* och IP-* semantik.
- Focused/progressive analysworkflow.
- Explicit workspace/checkpoint-state.
- `Gör nästa steg` som canonical resume-semantik.
- Evidence gate och separation mellan severity, evidence, confidence, risk och priority.
- De tre slutartefakterna:
  - `design-review.md`
  - `recommended-solution-strategy.md`
  - `implementation-plan.md`
- Fyra runtime-distributioner: Chat, Custom GPT, Claude Projects och OpenCode.
- Befintlig 20/20-projektstatus och releasehistorik.

## Runtime-målbild

Aktiva runtimes:

1. ChatGPT Chat
2. ChatGPT Custom GPT
3. Claude Projects
4. OpenCode

GPT Byggaren 1.5.0 ska beskriva verklig parity mer exakt:

- Chat: equivalent_runtime_dependent
- Custom GPT: equivalent_with_platform_constraints
- Claude Projects: reduced
- OpenCode: equivalent

OpenAI Plugin ska bedömas explicit men inte automatiskt aktiveras som full peer runtime. Om nödvändig filåtkomst, persistent state, artifact writing, validation och project packaging inte kan verifieras ska målet vara `not_active / reduced / advisory_only`.

## Steg

### 1. Separat 1.5.0-migrationsstatus
Inför separat migrationsplan/status utan att röra den befintliga 20/20-statusen.

### 2. Normalisera canonical kontrakt
Mappa befintliga capability-, artifact-, workspace/state- och tool-kontrakt till GPT Byggaren 1.5.0.

### 3. Runtime/distribution registry
Gör runtime-set, artifactnamn och compatibility deklarativa och maskinvaliderbara.

### 4. Verifiera Chat
Verifiera canonical instruction, project package, workspace/resume-state och tool fallback semantics.

### 5. Verifiera Custom GPT
Verifiera compiled instruction, Knowledge, plattformsbegränsningar och no-false-PASS.

### 6. Verifiera Claude och OpenCode
Lås Claude som reduced och OpenCode som equivalent med korrekt tool/state-semantik.

### 7. OpenAI Plugin compatibility assessment
Dokumentera och regressionstesta not_active/reduced/advisory_only om full parity inte kan bevisas.

### 8. Generalisera CI/parity/release
Härled aktiva runtimes, validering och release-assets från registryt och verifiera exakt artifact-set.

### 9. Slutlig release-readiness
Synka README/STATUS, lägg final 9/9-gate och verifiera mergebar PR.
