# AI Enablement - Claude Code kickoff

Statyczna prezentacja HTML na kickoff hackathonu CyberArk MIS 2026. Materiał obejmuje poziomy adopcji AI, architekturę systemów agentowych, Claude Code, halucynacje, guardrails, SDLC, współpracę wieloosobową, FinOps, regresje jakości oraz analizę porażek.

## Uruchomienie

Serwer WWW nie jest potrzebny. Otwórz plik `index.html` bezpośrednio w przeglądarce.

Sterowanie:

- `→`, `Space`, `PageDown` - następny slajd
- `←`, `PageUp` - poprzedni slajd
- `Home`, `End` - początek lub koniec
- `O` - overview wszystkich slajdów
- `F` - pełny ekran
- `?` - pomoc

Adres może zawierać numer slajdu, na przykład `index.html#/18`.

## Druk i PDF

Użyj funkcji drukowania w przeglądarce i wybierz układ poziomy. Arkusz stylów drukuje każdy slajd na osobnej stronie w proporcji 16:9.

## Zakres

Prezentacja jest materiałem typu intro i nie zawiera ćwiczeń. Slajdy mają układ modułowy, więc prowadzący może pominąć cały blok bez utraty ciągłości. Aktualne źródła i zastrzeżenia znajdują się w `SOURCES.md`.

## Weryfikacja

```bash
npm test
```

Skrypt sprawdza strukturę prezentacji, metadane slajdów i odwołania do lokalnych plików.
