# Agent Operating Rules

These rules apply before and during any task that uses project skills.

## Core Rules

1. Think before coding. State assumptions first. If a requirement is ambiguous and the wrong choice would matter, ask instead of guessing.
2. Prefer simplicity. Use the smallest code or document change that solves the stated problem. Do not add speculative features.
3. Make surgical changes. Touch only files and sections required for the task. Do not optimize neighboring code opportunistically.
4. Execute against goals. Define success criteria and let the agent iterate toward them. Avoid over-prescribing implementation steps when outcomes are clearer than process.
5. Use the model for judgment only. Let the model classify, summarize, extract, and interpret. Put routing, retries, status-code handling, pagination, and state transitions in deterministic code.
6. Treat token budget as a hard constraint. Target no more than 4000 tokens per single task and 30000 tokens per session. If the work is about to exceed the budget, summarize the current state, unresolved decisions, evidence, and next step before restarting or asking for direction. Do not silently keep running in circles.
7. Surface conflicts. When the codebase contains competing patterns, choose one pattern, explain why it is newer, better tested, or more consistent with the target surface, and mark the other as follow-up cleanup. Do not average incompatible patterns.
8. Read before writing. Before editing a file, inspect its exports, callers, shared helpers, and local conventions. Treat "this looks orthogonal" as unproven until checked.
9. Test intent, not only behavior. A test must explain why the behavior matters. If business logic can change while the test still passes, the test is too weak.
10. Checkpoint every multi-step task. After each step, record what changed, what was verified, and what remains. Do not continue from a state the agent cannot explain.
11. Follow local conventions even when they are not the agent's preferred style. Consistency inside the codebase is more important than taste. If a convention is harmful, say so explicitly instead of creating a parallel style.
12. Make failure visible. Do not claim completion after silently skipping records, checks, tests, or edge cases. Report skipped work, uncertainty, partial coverage, and verification gaps.

## Practical Gate

Before editing, answer internally or in the user-facing checkpoint:

- Assumptions: What am I assuming?
- Ambiguity: What would be risky to guess?
- Scope: Which files must change, and which should stay untouched?
- Success: What concrete evidence proves the task is handled?
- Budget: Is this still within the current task/session budget?

Before finishing, report:

- What changed.
- What was verified.
- What was skipped or remains uncertain.
