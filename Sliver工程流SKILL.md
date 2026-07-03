---
name: sliver-engineering-workflow
description: "Use for Sliver-style repo-native engineering: 立项, empty-project bootstrap, mid-project adoption/接管, feature/change/refactor/debug/review/release work, and new-window handoff. Especially 架构优先, 设计优先, 不乱补丁, 真源/dev-docs, agent 宪法, 严格验收, 不漂移, debug 证据纪律. Enforces current-truth audit, owner/contract-first design, evidence-backed debugging with reproduction/git-history/upstream checks, one mainline architecture, docs write-back, git hygiene, drift lock, and dangerous-action confirmation."
---

# Sliver Engineering Workflow

## Core Stance

Default to Chinese unless the user explicitly asks for English.

Treat `dev-docs/` as the primary record of the user's real engineering habits when the repo has adopted it. Treat `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` as hard constraints after confirming they are current and technically valid. Treat Codex memories and `.codex/sessions` as supporting evidence only; never let old conversation history override current repo truth.

When used with generic workflow skills such as brainstorming, TDD, or verification-before-completion, use those skills for cadence and evidence discipline. This skill controls engineering boundary decisions: owner layer, source truth, product boundary, stop condition, doc split, and drift lock.

This skill is for execution, not slogans. It must reproduce the user's demonstrated method, not invent a new consulting framework. The agent must prove the current truth, name the boundary, design the change, implement through the right owner layer, verify against risk, and write docs back when behavior or architecture changes. If the user is not a developer, the project has not started, or a half-built project lacks reliable agent constitution/source truth, the agent must create or propose the minimum governance surface first instead of improvising.

Templates and scripts are part of the method, not optional decoration. Use references to decide, use assets to materialize repeatable project truth, and use scripts to catch missing guardrails before claiming the project can be handed to another agent.

When the user corrects the agent, treat the correction as source truth for this task. Remove rejected concepts completely instead of renaming them into softer variants. If a draft drifts into generic options, pull it back to one concrete architecture, one current truth index, and an explicit stop condition. For strict non-drift work, read `references/agent-drift-lock.md`.

## Source Order

When facts conflict, use this order:

1. Current code, tests, scripts, generated contracts, schema, logs, live-device evidence, and current git state.
2. Repo-local `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and equivalent agent constitution files.
3. `dev-docs/README.md` or `docs/README.md` entries that identify current source-of-truth documents.
4. Active project initiation, product charter, architecture, contract, implementation-plan, readiness, and verification documents.
5. Archive documents as history only.
6. Codex memories and `.codex/sessions` as pattern evidence only. In Cursor or non-Codex environments, use available `agent-transcripts/`, chat exports, current diff, commit history, review comments, and active docs as the substitute conversation evidence.

If source truth is missing or contradictory, stop and report the conflict before coding. If meaningless backward compatibility is being requested or implied, ask the user for a product/architecture decision instead of preserving both paths.

## Required Workflow

Use this sequence for project initiation, features, modifications, refactors, and bug fixes:

```text
current-truth audit
  -> reasoning gate
  -> owner and contract design
  -> test / fixture / gate plan
  -> core implementation
  -> thin adapter / UI / CLI wiring
  -> targeted verification
  -> doc write-back
  -> git boundary review
```

Do not start from UI, HTTP handlers, MCP/WSS/CLI adapters, prompts, temporary scripts, or compatibility branches and then reverse-engineer the core. If the concept crosses two entry points, it belongs in a shared owner layer first.

If there is no repo or no project truth yet, switch to bootstrap mode:

```text
bootstrap-stage agent constitution
  -> product definition
  -> idea shaping into one recommended mainline
  -> project truth scaffold
  -> technology-stack recommendation and user confirmation
  -> owner map and one mainline architecture
  -> first closed loop
  -> acceptance gates
  -> drift checklist
```

For empty projects, create or draft the lightweight root agent constitution before product shaping, technology choice, scaffolding, or code. It must bind the agent to read-only discovery until the user confirms execution, forbid option theater, forbid framework-private rewrites, require user confirmation for hard product/technology constraints, and require the agent to converge vague user ideas into one recommended product mainline with rejected alternatives recorded only to prevent drift.

For non-developer intake or vague product ideas, read `references/non-developer-intake.md`.

For empty or unstarted projects, read `references/project-bootstrap.md` and use `assets/project-bootstrap/` templates as the starting artifact set.

If the repo already has code or business behavior but lacks reliable Sliver truth, switch to mid-project adoption mode before feature work:

```text
read-only takeover audit
  -> project stage classification
  -> root constitution decision
  -> internal truth index
  -> current-state audit
  -> owner map / architecture boundary
  -> acceptance and stop condition
  -> first safe task proposal
```

Use adoption mode when the project is half-built, inherited, forked, renamed, missing `AGENTS.md`, missing `dev-docs/README.md`, has only scattered `docs/`, or when the user says 接管 / 半路项目 / 先立 agent 宪法 / 防止后续 agent 漂移. Read `references/mid-project-adoption.md` and use `assets/project-adoption/` templates. Do not treat this as an empty-project bootstrap.

When a project path exists, run `scripts/check_project_guardrails.py <project-root>` after creating or changing the bootstrap artifacts. For checking the bundled template itself, use `--allow-template`.

For adopted half-built projects, run `scripts/check_project_guardrails.py <project-root> --mode adoption` after creating or changing adoption artifacts. For checking the bundled adoption template itself, use `--mode adoption --allow-template`.

If a mature repo has `docs/` but no internal `dev-docs/`, prefer creating the `dev-docs` truth scaffold. If that is not appropriate yet, use `scripts/check_project_guardrails.py <project-root> --truth-dir docs` as a transitional light check and document the migration/relaxation decision.

## Dangerous Adoption Actions

During mid-project adoption, stop for user confirmation before changing project governance or source truth. Dangerous actions include:

- creating or rewriting `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor rules, or equivalent agent constitution
- declaring `dev-docs/` the internal or only source truth when the repo used README, `docs/`, wiki, issues, or review comments before
- migrating, archiving, deleting, or mass-renaming old docs
- reframing product name, public README, external docs, UI copy, or marketing language
- deleting legacy API, fields, routes, config, caches, compatibility branches, generated contracts, or deployment scripts
- creating a nested `dev-docs` git repo or changing commit/release workflow
- marking the project as impossible to continue because truth is missing

Allowed without confirmation: read-only audit, listing conflicts, drafting a proposed adoption plan, and running non-destructive validation.

## Current-Truth Audit

Before editing, inspect the relevant current files. Usually start with:

- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
- `dev-docs/README.md`, `docs/README.md`
- active `project-initiation`, `product-charter`, `architecture`, `contract`, `implementation-plan`, `readiness`, `verification`, or `audit` docs
- current source files and call chain
- scripts/tests/generators that define the acceptance surface
- `git status --short`, repo root, ignored files, and nested repo boundaries when committing or publishing

For Codex session history, use targeted searches only. Search for stable phrases such as `架构优先`, `设计优先`, `不乱打补丁`, `严格遵守agent宪法`, `先审计`, `dev-docs`, `真源`, `无意义兼容`, `立项`, `重构`, `验收`. Ignore system prompts and repeated copied context. Extract recurring user preference and failure patterns, not stale implementation facts.

For creating or updating this methodology itself, sample one or two real conversations and check how the user pulled the agent back to boundary, evidence, documentation, or verification. Do not fill gaps with the agent's own taste.

## Reasoning Gate

Before implementation, answer these points briefly in the working notes or user update:

1. What problem is actually being solved?
2. Who creates it, who calls it, who consumes it?
3. What is the current source of truth?
4. Is there already a module, trait, SPI, manifest, registry, schema, state machine, validator, DAO, repository, or document with the same responsibility?
5. What is the single owner layer/module?
6. Which layers are forbidden owners for this concept?
7. What simpler or more conservative design exists, and why is it not enough?
8. What is the biggest regression risk, and what verification blocks it?

No closed reasoning gate, no implementation.

## Design Rules

- Lead with one recommended architecture. Mention alternatives only to explain why they were rejected.
- Answer the user's actual boundary question first: which layer, plane, contract, product boundary, or repo boundary owns the issue.
- Define product boundary and non-goals before module details.
- Put shared semantics in one owner: kernel, SDK, core service, SPI, trait, registry, schema, repository, policy, or design token source.
- Keep adapters thin. HTTP, MCP, WSS, MQTT, CLI, UI, controller, and runtime app should map protocol/display concerns onto shared contracts.
- Do not keep old product remnants, mock contracts, legacy fields, old routes, or old docs unless they have real migration value.
- Add abstractions only when they remove real complexity, define a needed boundary, or match an existing local pattern.
- Avoid option theater. If the user asks for an architecture, converge on the architecture that should be built.
- Every major design or plan needs a termination condition: when this topic is done, and what evidence proves it.

For project initiation and from-zero-to-one work, read `references/project-initiation-template.md`.

For feature, modification, refactor, and bug-fix work, read `references/feature-change-workflow.md`. For bugs, flaky tests, performance regressions, dependency/framework issues, production/live behavior, or any problem that has already resisted a simple fix, also read `references/debugging-workflow.md`.

For repeated failure modes and what to reject, read `references/anti-patterns.md`.

For acceptance, documentation, and git hygiene, read `references/verification-and-doc-governance.md`.

For final drift control, read `references/drift-control-checklist.md` and run `scripts/check_project_guardrails.py` when a local project path is available.

When the user asks for stronger non-drift guarantees, the task spans architecture/code/docs/git, or the agent is about to hand work to another agent, read `references/agent-drift-lock.md` and apply its hard stop triggers.

When the current context is too large, the user asks for a new-window handoff, or another agent will continue the project, read `references/context-handoff.md`. The handoff must be copy-paste-ready and include current git state, nested repo state, recent commits, changed files, validation evidence, runtime/service state, drift warnings, and next safe commands.

For a compact end-to-end example, read `examples/one-feature-lifecycle.md`.

## Implementation Rules

- Start with contract/schema/profile/report/manifest/trait/SPI where applicable.
- Add tests, fixtures, or gate scripts at the level that owns the risk.
- Implement core logic before adapter/UI exposure.
- Prefer existing local helper APIs, validators, repository patterns, design tokens, generated contracts, and framework conventions.
- Never hand-edit generated files when the project has a generator. Run the project generator and then inspect generated output.
- Do not use hard-coded cue lists, string contains matches, magic fallback paths, fake metrics, or duplicated status mappings as system authority.
- Do not remove reconciliation, identity, permission, or verification fields to improve speed or simplify UI.
- If the repo has an established UI style, reuse existing components, skeletons, i18n, spacing, and interaction patterns instead of creating a new visual direction.
- If a fix would silently sacrifice UX, visibility, data integrity, hardware stability, or product boundary, stop and discuss the architecture tradeoff.

## Verification Rules

Verification must match the touched risk surface:

- Docs only: read back files, check indexes, run targeted `rg` drift checks.
- Rust: format/check/test/clippy/profile gates and project scripts as relevant.
- Go/GoFrame: generated contract checks, package tests, vendor sync if module boundaries require it.
- Frontend: build, relevant tests, design-token scan, browser verification when UI behavior changed.
- Hardware/live path: target profile build plus live-device/log/user-visible evidence when claiming live readiness.
- Protocol/API: contract tests, structured errors, idempotency, auth/scope/rate/size limits where relevant.
- Performance/live behavior: real timing/log evidence from the affected path, not theoretical estimates.
- Review feedback: framework/source inspection when a finding is disputed before patching.

Never claim "passed", "ready", "fixed", or "release-ready" without current evidence. Split conclusions into code gate, integration chain, live-device/user acceptance, and remaining risk.

## Documentation Rules

Code behavior, architecture boundary, API contract, schema, profile, feature matrix, device behavior, UI truth, or acceptance criteria changes require doc write-back.

Use the repo's doc split:

- `dev-docs/`: internal architecture, plans, acceptance gates, audit records, agent constitution, rollout/readiness truth.
- `docs/`: external user, deploy, integration, API, hardware wiring, operations, and troubleshooting docs.

New active docs must be indexed from the relevant README. Completed, absorbed, one-off, or historical plans should move to archive or be marked non-current according to repo convention.

## Multi-Agent Rules

Use multiple agents only when tasks are independent and the user/environment allows it. Each agent must have:

- exact source truth to read
- read-only or disjoint write scope
- concrete output expectations
- verification responsibilities

The main agent remains responsible for architecture judgment, integration, diff review, and final acceptance. Never treat a subagent's "done" as verified.
