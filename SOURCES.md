# Źródła

Materiały sprawdzone 21 września 2026 r. Funkcje Claude Code zmieniają się szybko. Przed szkoleniem warto ponownie sprawdzić oznaczone funkcje eksperymentalne, nazwy komend i dostępność opcji w planie organizacji.

## Materiały wejściowe

- Repozytorium `dubel/ai-level-up-training` - drabina adopcji, kontrakt zadania, kontekst, bezpieczeństwo oraz sposób działania prezentacji offline.
- `AI_Enablement_Cyber_Ark_MIS_Intro.pptx` - pięciopoziomowy model dojrzałości, identyfikacja wizualna spotkania i zakres podstaw Claude Code.

## Claude Code

- [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices) - CLAUDE.md, uprawnienia, praca explore-plan-code, testy i korekta kursu.
- [Extend Claude Code](https://code.claude.com/docs/en/features-overview) - role CLAUDE.md, rules, skills, hooks, subagents, agent teams i MCP. Dokumentacja zaleca utrzymywanie CLAUDE.md poniżej około 200 linii.
- [How Claude remembers your project](https://code.claude.com/docs/en/memory) - zakres oraz ładowanie CLAUDE.md, rules i pamięci.
- [Configure permissions](https://code.claude.com/docs/en/permissions) - allow, ask, deny, kolejność oceny reguł oraz różnica między instrukcją modelu a kontrolą runtime.
- [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide) - deterministyczne kontrole cyklu życia i przypadki użycia hooks.
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents) - izolacja kontekstu, własne narzędzia i uprawnienia.
- [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams) - współpraca wielu sesji. Agent teams są eksperymentalne i domyślnie wyłączone. Dokumentacja ostrzega przed konfliktami przy edycji tych samych plików.
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) - integracje z usługami zewnętrznymi, zakres konfiguracji i zgody na serwery projektu.
- [Manage costs effectively](https://code.claude.com/docs/en/costs) - `/usage`, zarządzanie kontekstem, dobór modelu, koszt MCP i agent teams. Liczby cenowe pominięto w slajdach, ponieważ zależą od umowy i mogą się zmienić.

## Architektura, niezawodność i evals

- [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) - augmented LLM, prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer i pętla agenta.
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - skończony budżet uwagi i zasada minimalnego zestawu silnych sygnałów.
- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) - task, trial, grader, transcript lub trajectory, outcome i evaluation harness.
- [A postmortem of three recent issues](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues) - canary, ciągłe evals na systemach produkcyjnych i sygnały od użytkowników.
- [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) - warstwy obrony modelu, środowiska oraz treści zewnętrznej, sandboxing i ograniczanie promienia rażenia.
- [MCP: Tool Annotations as Risk Vocabulary](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/) - adnotacje narzędzi opisują ryzyko, ale nie stanowią mechanizmu egzekwowania ani ochrony przed prompt injection.

## Zastrzeżenia

- Pięć poziomów adopcji to model warsztatowy. Nie jest standardem Anthropic ani standardem branżowym.
- „Degradacja modelu” została ujęta jako regresja jakości całego systemu. Przyczyną może być model, kontekst, narzędzie, dane lub proces.
- Agent teams mogą zmienić status, interfejs i ograniczenia. Slajd celowo nazywa je funkcją eksperymentalną.
- Konkretne ceny i nazwy aktualnych modeli nie są częścią decku. Prezentacja pozostaje użyteczna mimo zmian oferty.
