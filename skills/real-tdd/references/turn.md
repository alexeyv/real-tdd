# The turn

Shared by both roles. "You" is whichever role is reading; "your partner"
is the other. The baton names roles as `ping` and `pong`.

## Steps

1. **Wait.** Run this until it returns, with your own role in place of
   `ROLE`; if the tool times out, run it again.

   ```bash
   until [ "$(cat .real-tdd/baton 2>/dev/null)" = "ROLE" ] || [ "$(cat .real-tdd/baton 2>/dev/null)" = "done" ]; do sleep 5; done
   ```

   If the baton reads `done`, read the last journal entry and stop.

2. **Receive.** Read the last entry of `.real-tdd/journal.md`,
   `.real-tdd/test-list.md`, and `git status`. Run the whole suite.
   Expect one failing test, uncommitted; the diff is your assignment. If
   the diff is a whole new test file, your partner forgot to commit it
   earlier and it goes into your commit.
   - If the test fails because of a mistake in the test rather than a
     missing behavior, fix it only enough to fail for the right reason,
     say so in the journal, and do not change what it asserts.
   - If the test asserts something that contradicts `.real-tdd/task.md`,
     name the task line in the journal, hand the baton back without a
     green, and go to step 1.
   - If the failing test is one you wrote and your partner handed it
     back, skip to step 5 and split it (Child Test), rewrite it, or
     withdraw it and pick another item.

3. **Green.** Make the failing test pass and keep every other test
   passing, by Fake It, Obvious Implementation, or Triangulate. Choose by
   how sure you are. Write no code that no current test demands; put the
   need on the list instead. If your green also satisfies other list
   items, name them in the journal and check them off as "satisfied by
   <commit>, not driven". After three failed attempts, revert to the last
   green commit, write in the journal that the step was too big, hand the
   baton back with the test still red, and go to step 1.

4. **Refactor.** Remove duplication, including between the test's
   expected value and the code. Improve names. Add no behavior. Run the
   whole suite after each change. Commit when green and clean, test file
   included, with a conventional-commit subject.

5. **Red.** Write the next failing test. You are deciding the interface
   it calls; record any signature, type, or name you fix in the journal.
   1. Pick one item from the list (One Step Test; Starter Test if nothing
      exists yet). If it is too big, split it on the list and take the
      smallest part.
   2. Assert First, with Evident Data. One behavior per test; the name
      says what it demonstrates.
   3. Isolated Test.
   4. Run the whole suite. The new test must fail and you must be able to
      say why. Not compiling is a valid failure. If it passes, either it
      records existing behavior, so keep it as a Regression Test and pick
      another item, or the code does more than its tests say. Check which;
      a passing new test has found a bug this way.
   5. Touch no production code. Not a stub, not a signature.
   6. Assert observable behavior in the problem's words, not an
      implementation you have in mind.
   7. Check off the item. Add anything you discovered.

   If the list is empty, write `done` to the baton, make the final journal
   entry, and stop. The human decides whether the list was finished.

6. **Hand off.** Append the journal entry in the format below, then write
   your partner's role to `.real-tdd/baton`. In that order. Go to step 1.

## Rules that hold throughout

- No plan. Write nowhere how the code will be structured.
- The journal reports. It does not tell your partner what to write or how
  to pass what you wrote. The only instruction between sessions is a test.
- One test at a time. Never two reds. Never a test and its implementation
  in the same turn.
- Whole suite, every run.
- One commit per green, only on green.
- Never read the other session's transcript.
- Never simulate your partner.

## Journal entry format

Take the timestamp from `date -u`; do not write it from memory.

```markdown
## Turn N — <your role> — <output of date -u>

**Received:** <test name> failing because <reason as observed>
**Green by:** Fake It | Obvious Implementation | Triangulate — <one line on why>
**Refactored:** <what duplication was removed, or "nothing">
**Commit:** <hash>
**Also satisfied:** <list items this green covered without a test, or "none">
**Wrote:** <new test name> — fails because <observed reason>
**Interface decided:** <any signature, type, or name this test fixed, or "none">
**List:** <items checked, items added>
**Surprise:** <what the test or the code taught you, or "none">
```

The Surprise line is the point. Write "none" when there was none.
