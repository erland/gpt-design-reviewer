# Operativa arbetsflöden för valfri designgransknings-evidens

Detta är fördjupning av `assistant/policies/optional-companion-evidence.md`. Använd bara när ett konkret designpåstående behöver kompletterande teknisk eller UI-evidens. Inga plugins är obligatoriska.

## 1. Välj minsta relevanta verifiering
1. Läs källkod och dokumentation, definiera den specifika DR-hypotesen och vilket observerbart resultat som skulle stärka eller försvaga den.
2. Upptäck aktuell värdmiljös tillgängliga verktyg. Gör inte antaganden utifrån installerade plugins.
3. Föredra tillgänglig icke-exekverande evidens. Om test/build behövs: använd redan fungerande lokal miljö eller GitHub CI före ny extern exekvering.
4. Stäm av säkerhetsrisk och tillåtelse inför körning av obetrodd kod och överföring av privat källmaterial; avstå från exekvering vid osäkerhet.

## 2. Agent Workspace – avgränsad teknisk probe
Kontrollera live-status och stödda språk/buildsystem, inklusive eventuell multi-modul- och projektrotskonfiguration. Välj exempelvis en bestämd npm/Maven-build eller ett fokuserat test som kan belägga en svårtestad designyta; kör inte hela projektet slentrianmässigt.

När exekvering är berättigad: skapa kortlivad workspace, överför endast godkänd projektkälla, kör avgränsad verifiering med `project_verify`; använd `project_build` endast när en byggd artefakt behövs för ett senare preview-steg. Läs relevanta loggutdrag med `file_read`. För artefakt-handoff, föredra tillfällig signerad `artifact_download_link` i stället för stor Base64 eller filmaterialisering i chatten. Rensa workspace även vid fel. Rapportera backendfel som `environment_limited`, inte som design-FAIL.

## 3. PWA Preview – enbart säker statisk webb
Kräv faktiskt producerad statisk build och kontrollera att innehållet är säkert att publicera på temporär HTTPS-adress. Gör aldrig privat kod, tokens, interna dokument eller data offentliga utan uttryckligt tillstånd. Skicka signerad build-URL direkt till preview-tjänsten om den stöds. Spara preview-ID, källrevision och tidsbegränsning. Status READY bevisar inte användbarhet, tillgänglighet eller funktionalitet. Radera preview best effort efter observation.

## 4. Browser Screenshot – observerad UI-evidens
Om en säker befintlig URL finns behövs ingen ny preview. Kontrollera aktuella session- och interaktionsverktyg. För endast visuellt stöd: ta skärmbild, ange viewport, URL och observerade detaljer och avgränsa slutsatsen till layouten.

För faktisk interaktion: skapa session, navigera, läs snapshot, välj stabila selectors, utför endast ofarlig fill/click och kontrollera DOM/visuellt utfall. Lägg inte in muterande verksamhetsdata, lösenord eller autentiserade flöden utan särskilt tillstånd. Ett enskilt observerat smoke-flöde är inte fullständigt E2E- eller tillgänglighetstest. Stäng session även om kontrollen misslyckas.

## 5. Evidensspår och fallback
För varje observation: ange projekt/source SHA, artefakt-hash när relevant, backend, kommando eller UI-handling, faktiskt resultat, vilken DR-hypotes som testats, evidensklass och begränsningar. Behåll `DR-*` och använd `VA-*` för material som kräver ytterligare verifiering. Misslyckade/skippade anrop rapporteras `NOT VERIFIED`; de är inte produktfel utan separat evidens.

Om Agent Workspace saknas: återgå till lokal analys/CI eller manuell källkodsläsning. Om PWA Preview saknas: observera bara redan säkert tillgänglig URL eller begränsa UI-slutsatserna. Om Browser Screenshot saknas: analysera källkoden och märk beteende-/UX-påståenden som inferens eller hypotes. Slutrapporterna är möjliga utan några plugins.
