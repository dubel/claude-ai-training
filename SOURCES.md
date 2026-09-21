# Sources

Materials reviewed on September 21, 2026. Claude Code and the supporting tool ecosystem change quickly. Recheck experimental features, command names, installation instructions, and plan availability before the training.

## Source material

- `dubel/ai-level-up-training` - the adoption ladder, task contract, context, safety, and the mechanics of the offline presentation.
- `AI_Enablement_Cyber_Ark_MIS_Intro.pptx` - the five-level maturity model, visual identity, and the introductory Claude Code material.

## Spec-driven development frameworks

- [GitHub Spec Kit](https://github.github.com/spec-kit/) - a specification lifecycle covering specification, planning, tasks, implementation, and convergence.
- [GSD Core](https://github.com/open-gsd/gsd-core) - the current Git. Ship. Done. framework and its discuss, plan, execute, verify, and ship phase loop.
- [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) - adaptive AI-driven development workflows with durable context and specialized product, architecture, development, and testing perspectives.

## Claude Code

- [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices) - CLAUDE.md, permissions, explore-plan-code workflows, tests, and course correction.
- [Extend Claude Code](https://code.claude.com/docs/en/features-overview) - the roles of CLAUDE.md, rules, skills, hooks, subagents, agent teams, and MCP. The documentation recommends keeping CLAUDE.md below approximately 200 lines.
- [How Claude remembers your project](https://code.claude.com/docs/en/memory) - scope and loading behavior for CLAUDE.md, rules, and memory.
- [Configure permissions](https://code.claude.com/docs/en/permissions) - allow, ask, deny, evaluation order, and the distinction between model instructions and runtime enforcement.
- [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide) - deterministic lifecycle controls and hook use cases.
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents) - context isolation, custom tools, and permissions.
- [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams) - collaboration across several sessions. Agent teams are experimental and disabled by default. The documentation warns against multiple agents editing the same files.
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) - external services, configuration scope, and approval of project servers.
- [Manage costs effectively](https://code.claude.com/docs/en/costs) - `/usage`, context management, model choice, MCP overhead, and agent team cost. The slides omit price figures because contracts and pricing can change.

## Context and code optimization

- [RTK - Rust Token Killer](https://github.com/rtk-ai/rtk) - filters shell-command output before it reaches the model. Reported reductions concern command output, not the full model bill.
- [Caveman](https://github.com/JuliusBrussee/caveman) - a skill that shortens agent responses. Its own instructions and setup consume context, so it can add overhead to an answer that is already short.
- [Ponytail](https://github.com/DietrichGebert/ponytail) - a YAGNI and Occam-style approach that limits how much code gets built and looks for code that can be removed.

## Architecture, reliability, and evaluations

- [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) - augmented LLMs, prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, and the agent loop.
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - the finite attention budget and the principle of using the smallest set of strong signals.
- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) - task, trial, grader, transcript or trajectory, outcome, and evaluation harness.
- [A postmortem of three recent issues](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues) - canary rollout, continuous evaluations on production systems, and user feedback signals.
- [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) - defense layers across the model, environment, and external content, including sandboxing and blast-radius reduction.
- [MCP: Tool Annotations as Risk Vocabulary](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/) - tool annotations describe risk but do not enforce security or prevent prompt injection.

## Caveats

- The five adoption levels form a workshop model. They are not an Anthropic or industry standard.
- The deck treats “model degradation” as quality regression across the complete system. The model, context, tools, data, or process may cause it.
- Agent teams may change status, interface, and limitations. The slide explicitly labels them experimental.
- Specific prices and current model names are outside the deck. This keeps the material useful when the product offering changes.
