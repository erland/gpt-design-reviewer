# Implementation planning

## När den aktiveras
Använd när användaren efterfrågar en konkret, stegvis och verifierbar genomförandeplan.

## Arbetssteg
Utgå från strategiteman RS-ID:n och deras DR-referenser. Dela upp arbetet i IP-001 och följande med ett avgränsat LLM-genomförbart steg per prompt. Ange mål, berörd kod, specifika ändringar, avgränsningar, beroenden, testkommando eller annan verifiering, färdigkriterier och risk. Säkra regressionstester och stabila gränssnitt innan riskfyllda beteendeförändringar.

## Utdata och överlämning
Leverera `implementation-plan.md` med spårning IP → RS → DR, checkpoint efter varje materiellt steg och explicit nästa körbara steg i `project-status.yaml`.
