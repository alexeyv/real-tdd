- source_spec: `spec-mars-rover.md`
  summary: AGENTS.md "Running and verifying" still says "TODO, no pyproject.toml exists yet" — now stale, since pyproject.toml exists and `uv run pytest` is a verified command.
  evidence: Raised by the blind-hunter review layer as an undocumented run command; the command IS documented, but under a TODO framing that is no longer true. The fix edits an agent-context file inside the bmad:context managed block, so it belongs to a bmad-project-context refresh rather than this build.
