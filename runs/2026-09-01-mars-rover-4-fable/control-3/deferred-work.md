- source_spec: `_bmad-output/implementation-artifacts/spec-mars-rover.md`
  summary: Decide whether `_bmad-output/` is tracked or gitignored; today it is neither.
  evidence: Reviewer noted `AGENTS.md` names it as the artifact location while the diff neither commits nor ignores it; user asked only for `.claude/` and `_bmad/` to be ignored, so this is a policy question.
- source_spec: `_bmad-output/implementation-artifacts/spec-mars-rover.md`
  summary: Refresh the `AGENTS.md` managed block so its provenance line names the commit with code in it.
  evidence: The block was hand-edited to drop the test-invocation TODO; the "Verified ... against the baseline commit" line predates the code. Fix belongs to `bmad-project-context refresh`, an agent-context file edit.
