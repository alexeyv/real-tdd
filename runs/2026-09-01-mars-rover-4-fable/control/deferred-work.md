- source_spec: `_bmad-output/implementation-artifacts/spec-mars-rover.md`
  summary: Decide whether to commit uv.lock (currently gitignored) so `uv run pytest` is reproducible.
  evidence: Reviewer noted uv recommends committing the lock for non-package projects; the ignore line predates this spec (baseline commit) and is a policy choice.
- source_spec: `_bmad-output/implementation-artifacts/spec-mars-rover.md`
  summary: Remove the "TODO: verify once pyproject.toml exists" from the `uv run pytest` line in AGENTS.md.
  evidence: `uv run pytest` was run repeatedly this build and passes; the fix edits an agent-context file, so it is left for bmad-project-context refresh.
