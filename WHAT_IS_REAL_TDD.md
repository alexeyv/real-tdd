# What Beck actually wrote

The skill's rules trace to these sources. Where the skill paraphrases,
this file says what is being paraphrased, so anyone can check whether the
skill has drifted from the technique it claims to run.

## Test-Driven Development: By Example (Addison-Wesley, 2002)

### Preface

The goal is "clean code that works" (Beck credits the phrase to Ron
Jeffries). Two rules:

- Write new code only if an automated test has failed.
- Eliminate duplication.

The rhythm those two rules imply:

- **Red.** Write a little test that does not work, and perhaps does not
  even compile at first.
- **Green.** Make the test work quickly, committing whatever sins are
  necessary in the process.
- **Refactor.** Eliminate all of the duplication created in merely getting
  the test to work.

"Test-driven development is a way of managing fear during programming."

### Part I, the Money example

The five-step loop stated at the start of the worked example:

1. Quickly add a test.
2. Run all tests and see the new one fail.
3. Make a little change.
4. Run all tests and see them all succeed.
5. Refactor to remove duplication.

The chapter opens with a **test list**: the behaviors to cover, written
before any test, in the language of the problem ("$5 + 10 CHF = $10 if
rate is 2:1", "$5 * 2 = $10"). Items get crossed off and added throughout.

The first green in the book returns a hard-coded value. The refactor step
then removes the duplication between that constant and the test's
expected value, and that is how the real implementation appears. This is
the mechanism the skill's Fake It rule relies on.

Beck's answer to whether he really works in steps this small is that he
does not always, but he is able to, and drops to that size when the going
gets hard. Step size is adjusted continuously, not fixed.

### Part III, patterns

**Test-Driven Development patterns (chapter 25):** Test, Isolated Test,
Test List, Test First, Assert First, Test Data, Evident Data.

- *Isolated Test*: tests do not affect one another; order must not matter.
- *Test List*: write down the tests you think you need before you start,
  and add to it as you go.
- *Assert First*: write the assertion first, then work backward to the
  setup.
- *Evident Data*: use literal values whose relationship to the expected
  result the reader can see.

**Red Bar patterns (chapter 26):** One Step Test, Starter Test,
Explanation Test, Learning Test, Another Test, Regression Test, Do Over,
Break.

- *One Step Test*: pick a test from the list that will teach you
  something and that you are confident you can implement.
- *Starter Test*: begin with something trivial, a test that establishes
  the shape of the call.
- *Another Test*: when a new idea comes up mid-step, add it to the list
  and stay on task.
- *Regression Test*: a test written for a defect that was found, which
  should have been written in the first place.
- *Do Over*: when you are lost, throw the code away and start again.

**Testing patterns (chapter 27):** Child Test, Mock Object, Self Shunt,
Log String, Crash Test Dummy, Broken Test, Clean Check-in.

- *Child Test*: when a test is too big to get green quickly, write a
  smaller test that represents the broken part, get that working, then
  reintroduce the larger one.
- *Clean Check-in*: before checking in, all tests pass. If integration
  turns something red, fix it or throw away the work.

**Green Bar patterns (chapter 28):** Fake It ('Til You Make It),
Triangulate, Obvious Implementation, One to Many.

- *Fake It*: return a constant; replace it with variables until you have
  real code. The constant is duplication with the test, and removing that
  duplication drives the implementation.
- *Triangulate*: abstract only when you have two or more examples. Beck
  says he uses it only when he really does not see the design.
- *Obvious Implementation*: if you know what to type, type it. If the bar
  goes red unexpectedly, drop back to smaller steps.

### Chapter 32, Mastering TDD

- "Write tests until fear is transformed into boredom." That is the
  answer to what you do not have to test.
- Delete a test when it adds no confidence and communicates nothing new.
- On pair programming: the tests you write are a good way to communicate
  with your partner. The skill's "the journal reports, it does not
  instruct" rule is a strict reading of this: the test is the message.

## Canon TDD (Kent Beck, *Software Design: Tidy First?* on Substack, December 2023)

Beck's restatement, written because so much of what is called TDD is not:

1. Write a list of the test scenarios you want to cover.
2. Turn exactly one item on the list into an actual, concrete, runnable
   test.
3. Change the code to make the test, and all previous tests, pass, adding
   items to the list as you discover them.
4. Optionally refactor to improve the implementation design.
5. Until the list is empty, go back to step 2.

He is explicit that writing all the tests up front and then all the code
is not TDD, and that the design work happens in two places: turning an
item into a test is interface design, and the refactor step is
implementation design. The skill's first turn is step 1; every later turn
is steps 2 through 4; the empty-list stop is step 5.

## Ping-pong pairing (not Beck)

The handoff pattern, where one partner writes a failing test and the other
makes it pass and writes the next one, comes from the XP community
(documented on Ward Cunningham's wiki and in Williams and Kessler's *Pair
Programming Illuminated*). Beck describes pair programming in *Extreme
Programming Explained* but does not prescribe this rhythm. The skill uses
it because it is the only pairing form in which the test author provably
does not know the implementation, which is the property the experiment
needs.

## Where TDD stops and asking begins

Nothing in *TDD by Example* tells you what to do when you do not know
what the behavior should be. The book assumes you do: the test list is
made of behaviors you already want, and every pattern in Part III is
about getting from a wanted behavior to working code in small steps. The
one place Beck addresses not knowing is the test list itself, and what he
puts there is a test you have not written yet, never a question.

The reason is that in Beck's setting the question has somewhere else to
go. *Extreme Programming Explained* (1999) makes it one of the twelve
practices: someone who can answer "what should this do" sits with the
programmers, full time, so that no programmer ever has to guess. *Planning
Extreme Programming* (Beck and Fowler, 2000) draws the line the skill
needs: what the software should do is a business decision and belongs to
the customer; how to build it is a technical decision and belongs to the
programmers. A programmer who picks between two readings of a requirement
has made a business decision, and in Beck's process that is a category
error, not initiative.

TDD is the programmer's side of that line. The tests are how programmers
make technical decisions one at a time. When a test would have to settle
what the software is for, it has crossed the line, and the right move is
not a cleverer test but a question.

Two runs of this skill showed why the rule has to be written down. In the
first, a session resolved an ambiguous clause in its test list, the
partner implemented it, and the choice was never surfaced. In the second,
both sessions noticed ambiguities, wrote them in the journal, and then
resolved them anyway, because the protocol gave them no other move. The
`human` baton is that move. It is not part of TDD; it is what TDD assumed
was in the room.

## What the skill invents

Beck's pairs share a keyboard and a room. Two sessions share a working
tree and nothing else, so the skill adds:

- a baton file, because there is no keyboard to hand over;
- a journal, because there is no conversation;
- a rule that the journal may not instruct, so that the journal cannot
  become the plan the technique is supposed to make unnecessary;
- a three-attempt limit before reverting, standing in for Beck's "get to
  green quickly", which for a human is measured in minutes;
- a `human` baton value, standing in for the person Beck's process keeps
  in the room to answer what the software should do.

None of these change the technique. They replace what a shared room
provided for free.
