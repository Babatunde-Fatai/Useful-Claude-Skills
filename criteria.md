## Skill review task (paste to your coding agent)

You are a repository reviewer. Your job is to evaluate every Skill folder (each must contain `SKILL.md` with YAML frontmatter) and produce: (1) per-skill scores, (2) actionable improvement PR suggestions, (3) cross-skill dedupe/standardization recommendations. The goal is effectiveness and efficiency first; include safety checks only where they affect reliability, maintainability, or avoid obvious misuse.

### Inputs you may assume
- A “Skill” is a directory with `SKILL.md` and optional extra markdown/resources/scripts; metadata (`name`, `description`) is always loaded, instructions are loaded only when triggered, and scripts can run without their code entering context (only outputs do), enabling token efficiency and deterministic operations. [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- Skills should be designed for progressive disclosure: metadata small, SKILL.md concise, deeper references/scripts loaded only when needed. [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

### Output format (strict)
1) `SKILLS_REPORT.md` (human readable)
2) `skills_report.json` (machine readable)
3) For each skill: a patch plan (file paths + exact edits), and if possible, a ready-to-apply diff.

### What to scan
- Parse every `SKILL.md` YAML frontmatter (`name`, `description`) and validate constraints (lowercase letters/numbers/hyphens; <=64 chars; description non-empty <=1024 chars). [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- Inspect SKILL.md structure: quick start, steps, examples, references to other files/scripts, and any tool assumptions (network/no-network, package availability). [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- Inspect scripts/resources for: determinism, I/O contracts, and whether they reduce token use by doing heavy work outside the prompt. [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

## Scoring rubric (100 points)

Score each category 0–5, multiply by weight, sum to 100. Include short justification and 1–3 evidence quotes/paths per category.

### 1) Trigger precision (weight 12)
How well metadata causes correct activation with minimal false positives.
- High score: description includes “use when…” conditions and clear boundaries. [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- Flags: vague descriptions (“handles documents”), overlapping descriptions with other skills, missing trigger cues.

### 2) Instruction economy (weight 12)
How concise SKILL.md is while still executable by a model.
- High score: “just enough” steps; avoids long prose; uses checklists and templates.
- Flags: walls of text, repeated boilerplate across many skills (suggest extraction into shared reference). Progressive disclosure is intended to keep nonessential content out of context. [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

### 3) Progressive disclosure design (weight 14)
Whether the skill cleanly separates L1 metadata vs L2 core steps vs L3 deep refs/scripts/resources.
- High score: SKILL.md links to deeper docs only when needed; scripts used for deterministic work and emit compact outputs; large references kept out of SKILL.md. [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- Flags: embedding huge reference tables directly in SKILL.md; instructions that require loading many files every time.

### 4) Determinism & automation leverage (weight 12)
Whether repeatable work is implemented as scripts instead of “do it in the model’s head”.
- High score: scripts validate inputs, normalize formats, and produce structured outputs; SKILL.md tells the agent when to run scripts; scripts keep code out of context for token efficiency. [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- Flags: instructions that repeatedly ask the model to generate long code rather than run provided utilities.

### 5) I/O contracts & schemas (weight 10)
Whether inputs/outputs are explicit and machine-checkable.
- High score: JSON/YAML schemas, “required fields”, examples, and error handling conventions; consistent output format across skills.

### 6) Tool-use workflow fit (weight 10)
How well the skill supports the common tool-use stages (select tool → call tool → interpret output → respond).
- High score: clear decision points (“If X, run script Y; else do Z”), validation steps, and how to interpret tool output.
- Tie to research: tool-learning evaluations and benchmarks are often stage-based (selection/calling/interpretation), so skills should be structured to reduce mistakes in each stage. [arxiv](https://arxiv.org/html/2405.17935v3)

### 7) Performance & cost awareness (weight 10)
Whether the skill is designed to reduce latency/tokens and avoid unnecessary work.
- High score: batching guidance, caching suggestions, minimal file reads, avoids repeated expensive operations; makes constraints explicit (e.g., no network in some surfaces). Runtime constraints vary by surface and matter for efficiency. [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- Tie to research: tool-use introduces practical challenges like latency and reliability tradeoffs, so skills should explicitly optimize the workflow. [arxiv](https://arxiv.org/html/2405.17935v3)

### 8) Maintainability & composability (weight 10)
How easy it is to evolve and combine skills.
- High score: consistent naming conventions, shared templates, minimal coupling, version notes, and cross-skill references that don’t create circular loads.
- Flags: duplicated logic across multiple skills; hard-coded paths; inconsistent outputs.

### 9) Reliability guardrails (weight 10)
Only reliability-focused checks (not “policy safety”): input validation, clear failure modes, and fallback behavior.
- High score: “If script fails, do X”; retry rules; sanity checks; non-goals; TEVV-style tests or fixtures where applicable (NIST emphasizes integrating testing/evaluation/verification/validation across lifecycle). [nvlpubs.nist](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf)

## Required per-skill deliverables
For each skill folder produce:

### A) Score block (markdown)
- Name, path
- Total score /100
- Category breakdown table (9 rows)
- 3 biggest strengths
- 3 highest-impact fixes (ordered by ROI)

### B) “Patch plan” block
- Exact edits (file + line-range or section)
- Suggested new/edited metadata description (optimized trigger phrase)
- Suggested refactor plan for progressive disclosure (what to move out of SKILL.md into `REFERENCE.md` / scripts). [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

### C) Minimal test plan
- 3–5 test cases (inputs + expected outputs/behaviors)
- Include at least one “error path” test (bad input) and one “efficiency” test (should avoid reading large files / avoid unnecessary steps). [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

## Cross-repo recommendations (required)
After per-skill reviews:
- Detect overlapping skills (similar descriptions) and propose merges or trigger narrowing. [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- Identify boilerplate duplicated across skills; propose a shared template or reference file to reduce SKILL.md tokens and improve maintainability. [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- Propose a standardized output contract for skills (e.g., “always return: Summary, Artifacts, Next actions, and Machine-readable JSON”). Keep it short.

## Rating guidance (how to score 0–5)
- 5: Best-in-class; minimal changes.
- 3: Works but has inefficiency/ambiguity; moderate refactor recommended.
- 1: Hard to trigger correctly or produces inconsistent results; needs redesign.
- 0: Missing required pieces (e.g., invalid YAML frontmatter, no executable steps). [platform.claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

***
