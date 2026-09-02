# Mars Rover, fourth ping-pong run: Fable 5.1 at medium effort

Same task and the same skill text as run 3 (`../2026-09-01-mars-rover-3/
skill-as-run/`), with both sessions on Claude Fable 5.1 at effort medium
instead of Opus 5 at high. Prompts: `/real-tdd ping` and `/real-tdd
pong`, task pre-written.

## Numbers

| | Run 3, Opus high | Run 4, Fable medium |
|---|---:|---:|
| Output tokens, both sessions | 134,301 | 66,254 |
| API calls | 198 | 98 |
| Wall time, scaffold to last commit | 29 min | 15 min |
| Turns | 24 | 27 |
| Commits | 25 | 29 |
| Tests | 27 | 35 |
| Tests that passed on arrival | 6 | 7 |
| Production lines | 62 | 55 |
| Green by Fake It / Obvious / Triangulate | 1 / 19 / 2 | 0 / 25 / 1 |
| Turns with "Refactored: nothing" | | 23 of 27 |
| Turns with "Surprise: none" | | 20 of 27 |
| Journal size | 54 KB | 28 KB |
| Human interventions | 1, asked for | 2, not asked for |
| Cache writes | 248,614 | 175,106 |
| Cache reads | 18,142,971 | 6,303,928 |

Half the output tokens, half the calls, half the wall time, half the
journal, for a result of the same shape and size. Per session: ping 38
calls and 35,440 output tokens, pong 60 calls and 30,814.

## The interventions

Both were the human's, neither was asked for, and both are on the record
because they changed the run.

1. **Turn 1.** Ping read the backward pole clause the opposite way from
   every earlier run: a rover backing over the north pole keeps its
   heading. It wrote in the journal that it had "fixed the reading in the
   list rather than asking" and named the list item as the place to
   correct it. That is the case the `human` baton exists for, seen and
   declined. The human appended a clarification to `task.md` giving the
   flip reading and the physics for it. Nobody asked; the baton never
   read `human`.
2. **After turn 3.** The clarification went unread, because the turn
   reads the journal, the list, git status, and the suite, and not the
   task file, even though git status showed the task file modified. The
   human prompted both sessions with one line saying the task file had
   a clarification. Ping rewrote the list item on its next turn; pong
   later noted that the clarified rule was the simpler code, one sentence
   for forward and backward alike where the other reading needed its own
   branch.

What the run therefore cannot show is what Fable would have done with
its own reading: asked, handed a test back, or shipped it. The
interventions were premature and the human said so at the time.

Two protocol gaps came out of it. A human answer only reaches the
session that asked, because only that session goes back to the task
file. And "ask when writing the test means choosing between readings"
did not fire on a session that had already chosen in the list at turn
one.

## What Fable did differently

- **Smaller greens.** Tables were filled one row per test. At turn 7 the
  step table had three headings and the turn tables one row each, and
  they stayed that way until a test asked. The Opus runs generalized
  earlier.
- **Refusal reports separately.** `refused_by` next to `blocked_by`, so
  a caller can tell a refusal from a bump. The only ping-pong run to
  make that distinction; the control made it with an enum.
- **The double-bump test holds under either rule.** Pong saw that
  refusal would make a second bump unreachable and wrote the assertion
  so it is true whether the second string bumps or is refused. Runs 2
  and 3 wrote a test that could be red only once and said so.
- **Refactoring almost never.** Twenty-three turns of "nothing". The two
  real ones: `RIGHT` derived as the inverse of `LEFT` at the end, and the
  refusal green at turn 23 that made movement a pure walk over a pure
  step, which ping described as the green itself rather than a refactor.
- **Seven regression tests at the end**, committed together as a test
  commit because no green was left to carry them. The rule says they go
  into the next green; there was none.
- **The list was shorter**, 23 items against 30 to 36, and split as it
  went rather than written in full at the start.

## Control: bmad-build on Fable 5.1 medium

Same TASK.md as the first control, bmad-build installed by its own
installer, one session on Fable 5.1 at medium effort. Setup answers as
before: uv, any Python, no rules beyond the spec, no outside standards.
Build prompt verbatim from the first control. Artifacts in `control/`.

| | Control 1, Opus high | Control 2, Fable medium | Run 4 ping-pong, Fable medium |
|---|---:|---:|---:|
| Output tokens | 93,266 | 36,577 | 66,254 |
| API calls | 137 | 35 | 98 |
| Wall time, build only | 25 min | 7 min | 15 min |
| Production lines | 267 | 205 | 55 |
| Classes | 6 | 3 | 1 |
| Tests (functions / cases) | 73 | 41 / 69 | 35 |
| Review layers run | 3 | 1 | |
| Human interventions | 5 | 1 | 2 |

Control 2 took bmad-build's in-session route: no implementer subagent,
the main session wrote the spec and the code itself, and only the Blind
Hunter layer ran. It never stopped for spec approval, which the prompt
had told it not to do. The one intervention was the same one the first
control needed: the reviewer's report came back truncated and the
session waited for a remainder that does not exist.

Asked afterwards why it took that route, the session said two things
beyond the gate's own criteria: that the dispatch route ends in a spec
approval stop and the prompt had said to stop only for what it could
not decide, so choosing dispatch "would have manufactured a stop"; and
that the one-shot route still runs a review, which "turned up 18
findings, 10 of which were patched", so coverage "was adequate for the
risk". The first applies an instruction about questions to a checkpoint
the workflow owns. The second justifies the route from the outcome of
having taken it. The gate's third criterion, no architectural
decisions, was false on a task that delegates interface and layout, and
the Opus control read it that way on the same prompt. One-shot was the right route for a greenfield kata with nothing to
break; the gate's own first criterion says so. The reasons the session
gave are not that. The route was chosen to fit the human's tone and the
criteria were fitted to it afterwards, and the same reasoning on a
codebase where the approval stop is the point would carry the model
past the one gate meant to put the interpretive calls in front of a
human. A good decision reached by a bad argument is the thing to record,
because the argument is what transfers.

The shape is the first control's shape at three quarters the size:
Planet, Rover, Report, seven validation sites, case-insensitive
commands, a review triage log with eighteen findings of which ten were
patched and six rejected with reasons. The known-obstacle pre-check uses
the rover's own map, recorded in the frozen Intent as the main
delegated decision. Same reading as every ping-pong run.

Against the ping-pong run on the same model: bmad-build produced four
times the code in half the tokens and half the time. The code it
produced is the code a spec author writes when told to make the calls
alone. The ping-pong code is the code the task's sentences demand and
nothing else. That is the same result as the Opus pair, at half scale
on both sides.

## Reading

The lean result is the same. On this kata a medium-effort model reaches
it in half the tokens by thinking less per turn and writing shorter
journal entries, and the journal shows what was lost: twenty turns with
nothing to report. The Opus journals were the interesting artifact;
this one is a log. Whether that matters depends on whether the journal
is the product or the code is.

## Files

Task with the human's clarification appended, final list, journal,
final code and tests, git log, and `repo.bundle` with full history. The
skill text is identical to run 3's `skill-as-run/`. `control/` holds
the bmad-build run: task, AGENTS.md, pyproject, the spec with its
triage log, deferred work, code, tests, git log, and bundle.
