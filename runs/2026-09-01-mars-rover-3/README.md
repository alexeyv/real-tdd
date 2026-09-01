# Mars Rover, third ping-pong run

Same task as the first two runs, on the skill at 0af8e9e: the `human`
baton, Receive and Hand off collapsed to one command each, no journal
timestamps, regression tests folded into the next green commit. The
skill text as installed is in `skill-as-run/`.

Both sessions Opus 5, effort high. Prompts: `/real-tdd ping` and
`/real-tdd pong`, task pre-written. One human answer during the run,
recorded at the bottom of `task.md`.

## Numbers

| | Run 1 | Run 2 | Run 3 |
|---|---:|---:|---:|
| Output tokens, both sessions | 92,639 | 136,199 | 134,301 |
| API calls | 165 | 223 | 198 |
| Wall time, first to last commit | ~100 min | 34 min | 32 min |
| Turns | 25 | 27 | 24 |
| Commits | 28 | 32 | 25 |
| Tests | 44 | 39 | 27 |
| Tests that passed on arrival | 20 | 12 | 6 |
| Production lines | 71 | 51 | 62 |
| Green by Fake It / Obvious / Triangulate | | 2 / 21 / 3 | 1 / 19 / 2 |
| Human interventions | 1 | 0 | 1, asked for |
| Cache writes | 311,695 | 271,421 | 248,614 |
| Cache reads | 11,542,804 | 19,732,682 | 18,142,971 |

Per session in run 3: ping 87 calls and 60,072 output tokens, pong 111
calls and 74,229. Pong wrote the closing question.

The collapsed protocol cut calls by a tenth against run 2 and left output
tokens unchanged. Output is mostly thinking, and thinking did not get
cheaper.

## The human baton

It fired once, at turn 22, and not on either ambiguity run 2 had found.

- The backward pole crossing was written as a regression test at turn 12,
  passed on arrival with the mechanism reading, and was checked off. The
  two readings never came up, because the code already did one of them
  and the test recorded it. The rule "ask when writing the test means
  choosing between readings" does not trigger when there is no choice
  left to make.
- The double bump was seen at turn 19, exactly as in run 2, and judged
  not ambiguous: the two task sentences do not contradict, the second
  makes the first unobservable. Pong wrote the test early so it could be
  red once, and said so.
- The question that did go to the human was one the sessions raised
  themselves: whether a rover that has never run a command string reports
  no obstacle or raises. The task says "after any command string" and is
  silent on before. Pong put the item on the list at turn 16 marked "not
  asked for by the task", carried it for six turns, and at the end handed
  the baton to the human with three options and a preference. The human
  chose (a), appended one paragraph to `task.md`, and the run finished
  two turns later.

So the mechanism works and the sessions use it for what it is for: a
scope decision, not an interpretation they can defend. Whether it should
also have fired on the pole reading is the open question.

## What the list did

Ping's closing entry counts it. Three defects were found by an item on
the list rather than by a test written for them: the heading flipping
during a blocked pole crossing, the stale report after a clean run, and
step-table rows missing for south and west. Each was flagged in the
journal by the session that saw it and left for a test, because fixing
it out of turn would have been production code no test demanded. Five
items were already true when their turn came, each paid for by a
refactoring done for another reason, and each unverified until the list
made someone look.

Twenty-seven tests against forty-four in run 1. Fewer regression tests,
and the ones that exist are there because an item was reached, not
because a block was written at the end.

## Files

Task with the human's answer appended, final list, journal, final code
and tests, git log, `repo.bundle` with full history, and `skill-as-run/`.
