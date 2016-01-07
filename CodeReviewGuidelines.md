# Keep "code reviewing" and "code rewriting" separate! #

We review existing code by having the reviewer directly edit the code in a separate git branch.  When the reviewer edits existing code in this way s(he) needs to keep two different impacts separate, by keeping them in two separate git branches:

  * "innocuous" revisions: e.g. adding or editing comments or docstrings.  We will refer to this as "code reviewing" because it leaves the original behavior unchanged.

  * significant revisions: anything that might alter how the code behaves.  We will refer to this as "code rewriting" because it could change the code's correctness and must be analyzed much more carefully.

Once the reviewer is done, the original author(s) of the existing code should review these recommended changes and decide what should be merged to master.  To make this job of "reviewing the code review" as straightforward as possible, it is very important that the innocuous changes (code reviewing) be separate from the potentially significant changes (code rewriting).  Knowing which changes require "paranoid" analysis (code rewriting) vs. which don't will make it easier and faster to review all these changes.

Git makes this separation really easy, and makes the potential disadvantages / overhead fairly minor.

# Process #
Say you were performing a code review of the **seqdb** module.  You would first

  * create a branch named something like **seqdb\_review**, and add docstrings and comments, reformat whitespace, add new test cases, move classes and functions around, delete unused classes or functions, change internal variable names etc.

  * If you see code that you think would benefit from revision, create a branch **seqdb\_rewrite**, and make your changes there.

  * Always commit each individual change separately (rather than combining several distinct changes into one commit), so that it will later be possible to easily pick and choose which changes to keep.  If many changes are combined in one commit, the only way to separate them is by hand, and much of the value of git for managing the revision process is lost.  This applies equally both to "code reviewing" and "code rewriting".

  * If code is rewritten, then in effect we have to begin a new cycle of code review, to review the new code.  The above rules would apply again; i.e. we'd create a review branch in which the existing code's author(s) can add comments, tests, etc.  If the author thinks significant changes to the rewritten code are desirable, s(he) can either just communicate them to the reviewer, or create a new "rewrite" branch in which to make these changes and expose that branch for review...