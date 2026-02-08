Hey, thanks for wanting to help out with development! 🙂
Here's a few guidelines (and one hard rule regarding AI) so that we can work together well:

# PRs
It's fine to open a PR directly, but please explain the problem you're solving in the comment. I don't want to guess what it does from the code.

If you're unsure whether I will accept a new feature, open an issue first and let's discuss it there.

Expect that I won't merge your PR directly; the more complex it is, the more comments I will usually leave. These are not meant to discourage or blame you!
I simply expect that I'll keep maintaining this tool for quite some more time, so I'd like to make sure its code is up to that.

# AI Usage
In general, it is okay to use AI for development. *HOWEVER*, it should only be an assistant to a human being.
I expect you to understand all changes and to be able to convince me that they are necessary and sensible.

Do not let it rewrite methods for something that is a one-line change. Keep the PR focussed on the necessary change and don't let AI run wild.

Keep to the usual style of the files. For example, I use comments very sparingly, so I expect to see almost none in your PR (only very unintuitive code deserves comments, in my opinion).

If your PR feels like AI slop because it ignored these rules, I will close it without review or comment, to keep my sanity.
Please respect me and my time.

# Git
I much prefer a rewritten, linear, clean history.

Each commit should contain one "unit" of connected changes that form a cohesive whole.

Do *NOT* merge any other branch into yours. If `main` has diverged, please rebase onto it.

During a review, it's okay to just add a comment `Review fixes`, but please squash it before I'm merging it.
With [git absorb](https://github.com/tummychow/git-absorb) and fixup commits, it's easy, too.

Feel free to add a good commit message with explanations, if fitting.
