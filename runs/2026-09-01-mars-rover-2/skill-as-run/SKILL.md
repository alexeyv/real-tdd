---
name: real-tdd
description: Kent Beck's test-driven development as he wrote it, run as ping-pong pairing between two Claude Code sessions sharing one working tree. Use when the user says /real-tdd, "real TDD", or "ping-pong TDD". Requires a partner session; never simulate the partner.
---

# Real TDD

An experiment, not a recommendation. Beck's TDD depends on the test's
author not yet knowing the implementation. One model context cannot
provide that; two can. So the technique runs across two sessions that
share a working tree and nothing else, and the journal they keep is the
data. Sources are in `references/beck.md`.

```
/real-tdd ping <task statement>     # first session, starts the run
/real-tdd ping                      # first session, task already in .real-tdd/task.md
/real-tdd pong                      # second session, joins the run
```

Your role is the first word of `$ARGUMENTS`.

- `ping`: read `references/ping.md` and follow it.
- `pong`: read `references/pong.md` and follow it.
- Anything else, or nothing: ask the human which role you are and stop.

If there is no partner session, stop and say so. Do not play both roles
with a subagent, a fork, or your own reasoning.
