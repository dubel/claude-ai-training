# Systemy agentowe — notatka na kick-off

Notatka porządkuje najważniejsze tematy do omówienia podczas kick-offu:
architekturę systemów agentowych, autonomię, halucynacje, koszty, regresje
jakości, SDLC, analizę awarii i guardrails. Główny wniosek: agent nie jest
samym modelem. To cały system — model, kontekst, narzędzia, uprawnienia,
logika sterująca, walidacja i monitoring.

## 1. Architektura systemów agentowych

Najprostszy model architektury:

```text
Użytkownik
  → polityki i klasyfikacja ryzyka
  → orchestrator / workflow
  → model
  → narzędzia, dane i pamięć
  → walidacja wyniku
  → wykonanie albo akceptacja człowieka
  → tracing, metryki i evals
```

Warto odróżnić **workflow** od **agenta**. Workflow ma ścieżkę ustaloną
w kodzie; agent sam wybiera kolejne kroki i narzędzia. Najlepsza praktyka to
zaczynanie od pojedynczego wywołania modelu lub prostego workflow, a następnie
dodawanie retrieval, narzędzi, pamięci i autonomii tylko wtedy, gdy evals
pokazują realną potrzebę. Złożoność oznacza większy koszt, latency i trudniejsze
debugowanie.

Źródło: [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents).

## 2. Determinizm a autonomia

To skala, nie wybór zero-jedynkowy. Model może autonomicznie analizować,
planować i proponować rozwiązania, ale wykonanie krytycznej operacji powinno
przechodzić przez deterministyczny kod: walidację schematu, sprawdzenie
uprawnień, limitów i aktualnego stanu systemu.

Autonomia powinna zależeć od ryzyka. Wyszukiwanie informacji może mieć dużą
autonomię; przelew, usunięcie danych albo publikacja — małą i z human approval.
Każdy agent powinien mieć budżet kroków, czasu, kosztu i wywołań narzędzi oraz
jasne warunki zakończenia. Ponieważ systemy LLM są niedeterministyczne, należy
testować rozkład wyników i wskaźnik poprawnego zakończenia zadania, nie jeden
„idealny output”.

Źródło: [OpenAI — Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices).

## 3. Halucynacje — jak sobie radzić

Halucynacji nie da się rozwiązać samym lepszym promptem. Model powinien opierać
odpowiedzi na kontrolowanych źródłach, pokazywać dowody lub cytowania i móc
powiedzieć „nie wiem”. W evalach trzeba osobno mierzyć odpowiedzi poprawne,
błędne i abstentions; pewny, błędny wynik powinien być karany mocniej niż brak
odpowiedzi.

Praktyczne podejście:

- stosować RAG lub narzędzia pobierające aktualne dane;
- wymagać źródeł dla twierdzeń faktograficznych;
- programowo sprawdzać identyfikatory, daty, kwoty i istnienie cytowanych
  dokumentów;
- umożliwić prośbę o doprecyzowanie albo odmowę odpowiedzi;
- przy decyzjach wysokiego ryzyka używać źródła prawdy i human review;
- dodawać każdą wykrytą halucynację do zestawu regresyjnego.

NIST traktuje confabulation jako ryzyko całego systemu i całego lifecycle,
szczególnie groźne przy decyzjach o realnych konsekwencjach.

Źródła:

- [OpenAI — Why language models hallucinate](https://openai.com/index/why-language-models-hallucinate/)
- [NIST — Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)

## 4. FinOps — optymalizacja kosztów

Nie należy optymalizować wyłącznie `cost per token`. Ważniejszy jest koszt
poprawnie zakończonego zadania: `cost per successful task`,
`cost per resolved case` albo `cost per accepted output`. FinOps Foundation
rekomenduje przejście od metryk technicznych do metryk powiązanych z wynikiem
biznesowym.

Najskuteczniejsze mechanizmy:

- mniejszy model dla prostych zadań, eskalacja do większego tylko przy
  potrzebie;
- krótszy prompt i ograniczony output;
- filtrowany retrieval zamiast umieszczania całej bazy w kontekście;
- prompt caching i cache wyników narzędzi;
- batch processing dla pracy asynchronicznej;
- early exit, limit retry i limit pętli;
- blokada niekontrolowanego tworzenia subagentów;
- budżet kosztowy per run oraz alerty.

OpenAI wskazuje redukcję liczby requestów i tokenów, mniejsze modele oraz
batch/flex processing jako główne mechanizmy kosztowe. Multi-agent wymaga
osobnego business case. W systemie badawczym Anthropic agenci zużywali około
4× więcej tokenów niż chat, a wariant multi-agent około 15×. To wynik jednego
systemu, nie uniwersalna stała, ale dobrze pokazuje skalę ryzyka kosztowego.

Źródła:

- [FinOps Foundation — Unit Economics](https://www.finops.org/framework/capabilities/unit-economics/)
- [OpenAI — Cost optimization](https://developers.openai.com/api/docs/guides/cost-optimization)
- [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)

## 5. Zapobieganie degradacji modeli i systemu

Zwykle degraduje się nie sam model, ale cały produkt: zmienia się model
dostawcy, prompt, dane RAG, API narzędzia, ruch użytkowników albo polityki.
Dlatego trzeba wersjonować cały **agent manifest**: model, parametry,
instrukcje, schematy narzędzi, guardrails, źródła danych i konfigurację
retrieval.

Każda zmiana powinna uruchamiać ten sam zestaw evals. Zestaw powinien zawierać
przypadki typowe, brzegowe, adversarial oraz realne awarie produkcyjne.
Produkcyjnie warto używać shadow traffic lub canary, porównania z baseline,
alertów jakościowych i kosztowych oraz szybkiego rollbacku. Continuous
evaluation powinno działać przy każdej zmianie, a dataset rosnąć wraz z nowymi
przypadkami.

Źródło: [OpenAI — Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices).

## 6. SDLC dla agentów i praca kilku osób

Agentowy SDLC powinien przypominać zwykły SDLC, ale z dodatkową warstwą
eval-driven development:

1. Kryteria sukcesu, ryzyko i koszt przed implementacją.
2. Wersjonowane prompty, polityki, narzędzia i datasety.
3. Deterministyczne unit/integration tests.
4. Agent evals: wynik, tool calls, handoffs, koszt i bezpieczeństwo.
5. Review zmian promptów tak samo jak kodu.
6. Shadow/canary przed pełnym wdrożeniem.
7. Monitoring, feedback i rollback po wdrożeniu.

Praca kilku osób ma sens, jeśli zadanie da się podzielić na niezależne obszary
z jasnym kontraktem. Jeden właściciel powinien odpowiadać za integrację i wynik
end-to-end. Równoległa praca kilku osób lub agentów nad tym samym promptem albo
silnie zależnym fragmentem zwykle tworzy konflikty i utrudnia ustalenie
przyczyny regresji. Multi-agent dobrze działa przy szerokim, równoległym
researchu, ale wiele zadań programistycznych ma zbyt dużo zależności i za mało
prawdziwej równoległości.

Źródło: [Anthropic — Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system).

## 7. Analiza porażek AI — wynik i koszt

Każdy run powinien mieć trace zawierający: wersję konfiguracji, model, wejście,
pobrany kontekst, decyzje routingu, wywołania narzędzi, handoffs, wynik, koszt
i latency. Analizę należy zaczynać od pierwszego błędnego kroku, nie od
ostatniej złej odpowiedzi.

Przydatna taksonomia awarii:

- niejasne wymaganie;
- zły lub brakujący kontekst;
- błąd retrieval;
- zły plan;
- złe narzędzie albo argumenty;
- awaria narzędzia lub środowiska;
- błędny handoff;
- nieskuteczny guardrail;
- brak walidacji finalnego wyniku.

Koszt warto analizować jako waterfall: ile wydano przed wykryciem problemu oraz
ile kosztowały retry, zbędne narzędzia i praca wykonana po pierwszym błędzie.
Główna metryka porównawcza to koszt poprawnego wyniku, wsparty przez success
rate, severe-error rate, latency i liczbę interwencji człowieka. Trace grading
pomaga sprawdzać wybór narzędzi, handoffs, naruszenia instrukcji i regresje
całego workflow.

Źródło: [OpenAI — Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals).

## 8. Guardrails — granice, które nie giną z kontekstu

Najważniejsza zasada: krytyczne guardrails nie mogą istnieć wyłącznie jako
tekst w promptcie. Kontekst może zostać skrócony, zignorowany albo nadpisany
przez dane zewnętrzne. Granice trzeba egzekwować przy miejscu skutku: w kodzie
narzędzia, API gateway, systemie uprawnień, sandboxie i warstwie approval.

Warstwy ochrony:

- input guardrails — klasyfikacja zakresu, PII, prompt injection;
- structured output — ustalone schematy zamiast dowolnego tekstu;
- tool guardrails — allowlist operacji i walidacja argumentów;
- least privilege — minimalne dane, sieć i uprawnienia;
- human approval — operacje nieodwracalne, zewnętrzne lub kosztowne;
- output guardrails — walidacja, redakcja danych i zgodność z polityką;
- limity czasu, kosztu, kroków i retry;
- audyt i fail closed przy braku możliwości walidacji.

Polityka powinna być krótkim, wersjonowanym artefaktem z identyfikatorem
wersji. Trzeba przekazywać ją ponownie przy każdym handoffie, ale najważniejsze
ograniczenia egzekwować niezależnie od pamięci modelu. Walidacja powinna
znajdować się przy narzędziu tworzącym side effect, ponieważ guardrail na
wejściu lub wyjściu nie obejmuje automatycznie wszystkich kroków zagnieżdżonego
workflow.

Źródło: [OpenAI — Guardrails and human review](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals).

## Decyzje, które powinny zapaść na kick-offie

Spotkanie powinno zakończyć się ośmioma konkretnymi decyzjami:

- pierwszy, wąski use case;
- mierzalna definicja sukcesu;
- dopuszczalny poziom autonomii;
- operacje wymagające approval;
- budżet jednego runu;
- początkowy zestaw evals;
- właściciel jakości, kosztu i bezpieczeństwa;
- warunki zatrzymania oraz rollbacku.

Najważniejszy reality check: najpierw budujemy mierzalny system rozwiązujący
jedno zadanie. Dopiero wyniki pokażą, czy potrzebujemy agenta, większej
autonomii albo wielu agentów.
