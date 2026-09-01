# Ping

1. Read `glossary.md` in this directory.
2. Read `turn.md` in this directory. Your role is `ping`; your partner is
   `pong`.
3. Start the run.
   1. If `$ARGUMENTS` carries a task statement after the word `ping`,
      write it verbatim to `.real-tdd/task.md`. Otherwise read the one
      there. If there is none, ask the human and stop.
   2. Write `.real-tdd/test-list.md`: the behaviors the finished code
      should have, as checkboxes, in the problem's words. Not steps, not
      functions.
   3. Read the task again, line by line, against the list. Every sentence
      that states a behavior has an item, and no item contradicts a
      sentence. Both sessions will treat this list as binding. If a
      sentence can be read two ways, ask the human now (turn step 7)
      rather than picking one.
   4. If no test can run yet, add the minimum that lets one test file
      execute, and commit it on its own. No production code.
   5. Write `ping` to `.real-tdd/baton`.
4. Do the turn from step 5, Red. Then continue the turn as written.
