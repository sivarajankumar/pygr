# Why Git? #

Git is the front-runner of a new generation of "distributed source code management" tools that make it much easier for a dispersed group of developers to collaborate on a complex open source project like the Linux kernel.  The first thing to understand is that git dumps the previously universal assumption of a centralized repository, which developers check out files (from) and check in changes (to).  Instead, with git, **every** developer has the complete repository, storing the complete revision history.  That makes it much easier for each developer to work independently -- s/he doesn't even need a net connection to make commits.  Developers can clone a repository from each other, pull changes from each other, email patches to each other, push changes to a public site etc.  Second, git makes it spectacularly easy to work with branches: at any moment, you can create a new branch off your current code, make experimental changes as a series of commits on that branch -- without in any way affecting your "master" branch or any other branch -- and switch instantly between different branches.  Merging in changes from one branch to another is amazingly easy and powerful in git, so if you decide you like your experimental changes, you can apply them to your "master" branch easily -- typically with just a single command "git merge".  Git has great momentum now, and it has already been a terrific boost to Pygr development.

# Overview of How We're Using Git #
The Pygr project is tiny in comparison with Linux kernel, so we can get away with a pretty simple development model:
  * We are using [github.com](http://github.com) as our public repository server.  Github.com offers a lot of [great tools](http://github.com/guides/home) for developers to collaborate.
  * I own the ["official" public git repository for pygr](http://github.com/cjlee112/pygr); i.e. all proposed changes pass through me.
  * Anyone else can [create their own fork of the project on github.com](http://github.com/guides/fork-a-project-and-submit-your-modifications), which will allow you to easily create your own experimental branches, tell me when you want me to incorporate your changes into the official master branch, and stay in synch with my "upstream" repository etc.
  * If you want to immediately get your hands on the code without creating a github.com account, just using "git clone" from [the public repository](http://github.com/cjlee112/pygr).  Note however that without a publicly hosted git repository, you will only be able to share your changes with others by sending email patches, without any of github's great tools.  If you have any interest in modifying the Pygr source, I highly recommend getting a github.com account.  It only takes a minute.
  * In general, I suggest making changes in a new branch rather than **master**.  Making changes in the master branch will complicate your ability to pull from the public repository, because you will not be able to keep your changes separate from the changes in the public master.  We suggest that you always create a separate branch in which to make your changes.  In doing so, you just commit your changes as usual, but in your branch, not in the master branch.
  * When the time comes that you want to share your changes with others (e.g. get them incorporated in the public master), all you have to do is tell us the name of your new branch.  We will then examine them, and merge them into the public master branch if there are no issues that need discussion first.
  * We can create separate branches for a specific release cycle.  E.g. I created a branch v0\_7 for bug fixes to version 0.7.  It's trivial to pull bug fixes from the master branch into the v0\_7 branch, and vice versa.


# Using git with your github.com account #
The following examples assume you have a github.com account and your own fork of the pygr repository in your account.  This allows you both to pull future changes from the official repository, and to push your changes to your own public repository for others to access.

First, take a look at the [very helpful guides](http://github.com/guides/home) on github.com.

Next, you may want to use the [github gem interface](http://github.com/defunkt/github-gem), which provides an interface on top of git that customizes it nicely to work with github.  It looks pretty nice.

### Get a copy of your Pygr fork repository ###
```
git clone git@github.com:yourname/pygr.git
```
Whenever you clone a repository, git automatically adds a remote called "origin" that points to the repository you cloned.  That means you can use "origin" in all sorts of git commands, e.g. {{{git push origin master}} will push your master branch to your github repository.

See github's [helpful instructions](http://github.com/guides/fork-a-project-and-submit-your-modifications) here.

### Add the official repository as a remote named "upstream" ###
```
git remote add -f upstream git://github.com/cjlee112/pygr.git
```
Note that **upstream** is how github refers to the repository you forked from (in this case, the official Pygr repository).

### Update your master branch from the official master branch ###
```
git checkout master
git pull upstream master
```
**upstream master** refers to the master branch in the official repository (which we named "upstream" in the previous section).  The `git pull` command will both fetch and merge changes from that branch into your current branch (in this case, your master branch).

### Push your master branch to your github repository ###
```
git push origin master
```
Note that **origin** is how github refers to your public repository in your github account.

### Push your current branch to your github repository ###
```
git push origin HEAD
```
**HEAD** just refers to the head of your current branch.  If your current branch doesn't exist in your github repository, it will be created.

### Push a tag to your github repository ###
```
git push origin tag v0.8.0.alpha1
```
In this case I pushed my tag "v0.8.0.alpha1" to github.

### Add someone else's fork to your list of remote repositories ###
```
git remote add -f ctb git://github.com/ctb/pygr.git
```
In the future we will be able to access Titus' Pygr repository via the name **ctb**.  The **-f** option makes git fetch Titus' branches as tracking branches in your local repository, e.g. his master branch would be tracked in your repository as **ctb/master**.

### Pull an experimental branch from someone else's fork ###
Assuming you've already added that person's fork to your list of remote repositories as shown in the previous step, all you have to do is get the latest remote updates
```
git remote update
```
E.g. if Titus has a branch named "seqdb\_review", any updates he made in that branch will show up in **remotes/ctb/seqdb\_review** (which simply tracks that branch in his repository).

### Fetch from a specific remote ###
```
git fetch mkszuba
```
This fetches the latest commits from all branches of the remote repository "mkszuba".  This will update a set of branches in your local repository named "mkszuba/_branchname_", but it won't merge into any of your personal branches like **git pull** would.


### Graphical view of remote branches vs. your branches ###
The `gitk` viewer shows you the branch structure, history, and any commit that you select.  To view all branches:

`gitk --all`
Remote branches will be labeled "remotes/**remotename**/**branchname**"

To view a specific branch:

`gitk remotes/ctb/seqdb_review`


### View someone else's experimental branch ###
Using the above procedure, the other person's branches will be mirrored in your repository simply prefixed by the name you assigned their remote repository (in this case **ctb**).  Knowing that, you can view everything they've done in that branch simply by using that branch name, e.g.
```
git branch -r # list the remote branches your repository is tracking
git checkout remotes/ctb/seqdb_review # look at the current state of his branch
git log # show the list of commits leading up to his current state
git diff a17f52 # show diff of his current state vs. a specific commit
gitk --all # show dependency graph of all commits, including local and remote branches
```

### Add your own changes to someone else's experimental branch ###
If you wanted to modify that branch, you'd create your own seqdb\_review branch based on his branch, and start making commits...
```
git branch seqdb_review remotes/ctb/seqdb_review
git checkout seqdb_review
```
Now you can start editing and making your own commits in this branch, and push it back to your own repository.

In general, this is the best way for two or more people to collaborate on an experimental feature: one person creates the experimental branch; other people copy it, make their own changes, push the branch to their own github repository.  Then everybody can pull from each other's version of this experimental branch, make more changes, etc.

# Using git without your own github.com account #
### Get a copy of the public repository ###
```
git clone git://github.com/cjlee112/pygr.git
```
In this case, you will be able to pull future changes from the official repository, but you won't be able to push your changes back to it.

### Get the latest changes from the public repository ###
```
git checkout master
git pull --rebase
```
The first command is only necessary if you were previously working on a different branch than "master".

# General git usage #
### Make an experimental branch and commit changes there ###
```
git checkout -b trythis
# edit one or more files, test your changes...
git add pygr/sqlgraph.py tests/nosebase.py # whatever files you changed
git add tests/new_test.py # you can also add new files to the repository
git rm tests/old_test.py # and even delete a file (from this branch)
git commit -m 'put a meaningful explanation of your changes here'
# edit some more files...
git add some_more_files.py
git commit -m 'explain your new changes here'
# and so on...
```
The basic process for making changes in git is:
  * first, just edit whatever files you want.  You don't have to do anything to "check out" those files!
  * use **git add** on your changed files, to "stage" these changes for committing.
  * use **git commit** to commit all those changes as a single atomic revision.  Note that every commit has a unique ID (long hexadecimal code).  You can generally use this ID (or just its first few digits as long as it's unique) to specify a specific commit in any git command.

### See a list of branches in your repository ###
```
git branch
```
The current branch is marked with an asterisk.

### Switch to a different branch ###
```
git checkout master
```
Substitute the name of the branch you want for "master".

### Go back to an old version ###
```
git checkout 1a413b3
```
You can use the first few digits of a commit ID, or a tag name.  This jumps
you back to that specific commit, which can be very useful for testing purposes.
Note that this puts you in effect on an "unnamed branch" whose HEAD is at the
commit you specified.  To go back to the current HEAD of your master branch just
```
git checkout master
```

### See the current state of any edits you may have made, but not yet committed ###
```
git status
```

### See the history and branch structure of the repository with a graphical tool ###
```
gitk --all
```
May require X windows and Tk on some platforms.

### See a list of your remotes ###
```
git remote -v
```

### See repository history as text ###
```
git log
```

### Merge new changes from one branch to another ###
```
git checkout trythis
git merge master
```
This example automatically applies any changes from the master branch that have been made after you created your **trythis** branch.  Git is able to do most merges completely automatically; only if the changes overlap the same lines of code will it ask you to sort out the conflict (it puts diff markers in the relevant file; your job is to edit that file to be the way you want it).

### Merge selected changes from one branch to another ###
What if you only want to take a subset of commits from another branch, or you
want to modify some of those commits?  To take a subset of commits from `remotes/lhc/master` to your master branch:

```
git checkout -b temp master
git rebase -i --onto temp master remotes/lhc/master
```

The -i specifies interactive mode: git will show you a list of the commits on the remotes/lhc/master branch.  If you delete a given commit line, that commit will be skipped by the rebase operation.  If you edit the keyword "pick" to "edit", it will stop the rebase operation at that point, and let you edit / add whatever changes you want, before continuing the rebase process.  To add another change at that point, just edit / commit as usual, then type
```
git rebase --continue
```

Equally well, you can modify this commit by resetting that commit.  For example
```
git reset HEAD^
```
will move back to the previous commit, while leaving your working files alone, so you can modify them as you wish.  Commit them as you wish, then restart the rebase operation with
```
git rebase --continue
```

When the rebase operation is all done, all of its results will be in the "temp" branch.  If you like what it has produced, you can now merge it to master:
```
git checkout master
git merge temp
git branch -d temp
```

### Move your last commit to a different branch ###
Say you've realized you should have made your last commit on a different branch.  You can easily move it.  Assuming your current branch is `thisbranch` and you want to move the last commit to `otherbranch`:
```
git checkout -b tmp
git checkout thisbranch
git reset --hard HEAD^
git rebase --onto otherbranch thisbranch tmp
git checkout otherbranch
git merge tmp
git branch -d tmp
```
To move more than one commit, just alter the `HEAD^` reference to point to the commit that you want to become the new HEAD of `thisbranch`.

### Mark your branch as the correct resolution of other branches ###
Say you put some work into revising someone else's branch to produce what you consider to be the "corrected" version of their branch.  At this point, you'd like to inform git that your branch should be considered the "correct resolution" of their work.  That way, if they add new commits to their branch, you'd have the option of simply merging those commits from their branch without any fear that this would pull in some of their older commits that conflict with your resolution.

This is easy to do in git:
```
git merge -s ours remotes/lhc/master
```
leaves the current HEAD completely unchanged, but tells git to consider all previous commits on remotes/lhc/master to be "merged into it".  That means that any future merge from remotes/lhc/master will **only** apply commits that occurred after this point.  This is an example of specifying a "merge strategy", in this case the trivial strategy "ours", which just leaves your branch unchanged.


### Apply a single commit from one branch to another ###
```
git checkout trythis
git cherry-pick 37d1f89
```
Here we switch to the branch we want to change (in case we're not already on that branch).
Then you specify the commit you want to apply via its SHA1 hash code, or in this case just its first few digits.

### Revert changes in one file, back to the last commit ###
Say you edited myfoo.py, but now want to revert back the version in your last commit:
```
git checkout myfoo.py
```
Note that git checkout treats any name that isn't a branch name as a file name to revert in this way...

### Abandon any uncommitted changes, returning to last commit ###
```
git reset --hard HEAD
```
If you want to get rid of the last two **commits** as well:
```
git reset --hard HEAD-2
```
Don't do the latter if you have already exposed those commits to other people!!!  Instead, use...

### Revert a previous commit ###
To revert a single commit, just specify its ID
```
git revert 1d5916
```
You can also revert a series of commits (see the git-revert man page).

### Push updates from one machine to another ###
Say you have a test machine that currently has just the master branch cloned from the public repository.  Now suppose you have made a bunch of new changes on a new branch called "seqdb\_refactor" on your main development machine, and want to test these changes on the test machine.  Instead of having to push the new changes to the public repository, and then pull them to the test machine, you can push them directly to the test machine over ssh.  From your development machine, in your development repository:
```
git push 'ssh://my.test.machine.address/~/projects/pygr/.git' seqdb_refactor
```
If the test machine repository doesn't have the seqdb\_refactor branch, it will be created automatically.

When I push to a repository that is already on that specific branch, it seems that the destination repository (i.e. on my.test.machine.address in the example above) does not automatically update the working files to the head of what I pushed to that branch.  I have had trouble getting it to update the working files.  In at least one instance, it claimed that there were unsaved changes in the one file I wanted to update, and thus would not let me use `git checkout HEAD` to update it (maybe it was confused by the fact that the new HEAD specifically included a change to that file?).  In that case I was able to force it to update the working files via
```
git reset --hard HEAD
```


### Push to github repository ###
Same as above but with github: you need to have uploaded your ssh public key, and you need to be included as a collaborator on the project to which you want to push.  In this example I am pushing to Titus' psu-tests-branch:
```
git push ssh://git@github.com/ctb/pygr.git psu-tests-branch
```

### Tag a release ###
```
git tag v0.7.1
```
to tag the current HEAD of the current branch.  You can also tag a specific previous commit:
```
git tag v0.7.5 78ac23bb
```

### Push a tag to the repository ###
```
git push origin tag v0.8.0.alpha2
```
In this case, "origin" means my github repository.


# Deprecated Usages #

These are no longer our recommended ways of working, but retained just in case they're historically useful.

### Generate patch output for emailing me your changes ###
```
git format-patch master >my_patches.txt
```
This outputs patches for all commits in the current branch not in the master branch.

### Apply someone else's patch file to your repository ###
```
git checkout -b titus_temp # create & switch to temporary branch
git am titus_patches.txt # apply the patch file
# inspect changes to see if you like them
# alter as you see fit, make additional commits until you're happy
git checkout master # switch back to master
git merge titus_temp # apply all our approved changes to master
git branch -d titus_temp # don't need this temporary branch any more
```
Note that here the net effect was I applied the patches to my master branch.  But of course I could have applied to any branch I wanted.  Note also that I adopt the cautious approach of first testing out all the patches in a temporary branch, rather than directly applying them to master.  This way, if I don't manage to finish this job in one sitting, it is kept separate from my master branch.  Indeed, I could switch back to the master branch and do urgent bug fixes, before switch back to titus\_temp to finish my evaluation of the patch(es).

### Pull from someone else's staging branch to your repository ###
```
git checkout -b titus_temp # create & switch to temporary branch
git pull git://iorich.caltech.edu/git/public/pygr-ctb staging # get his changes
# inspect changes to see if you like them
# alter as you see fit, make additional commits until you're happy
git checkout master # switch back to master
git merge titus_temp # apply all our approved changes to master
git branch -d titus_temp # don't need this temporary branch any more
```
The only difference from the previous method is that this pulls in all the commits from a particular branch of someone else's git repository, in this case the branch called "staging".

### Pull from a github branch to your repository (simple case) ###
Everything the same as above, but with github instead: this example pulls from Titus' branch called "psu-tests-branch", assuming that branch started from the same commit that your current branch is at (in which case git can apply the commits from psu-tests-branch as a simple fast-forward)
```
git checkout -b psu-tests-branch
git pull git://github.com/ctb/pygr.git psu-tests-branch
```

### Pull from a github branch to your repository (more complex case) ###
What if you or others have committed more changes after Titus began his branch that you want to begin working with?  In that case, the simplest thing to do is to go back to the commit he started from, before creating the branch that will then pull from his branch.  To see the commit-graph online, go to Titus github account and click the [network](http://github.com/ctb/pygr/network) tab.  You can click and drag to explore the commit-graph, and mouse-over a specific commit to see its ID etc.  Once you identify the commit-ID that his branch began from, you can "rewind" to that commit-ID, start a branch from that same point, and then pull from his github branch (which will be a simple fast-forward):
```
git checkout e17e4 # rewind to the last commit shared by his branch and yours
git checkout -b seqdb-review # start a branch from that point
git pull git://github.com/ctb/pygr.git seqdb-review # pull all his changes from that point
```

### Push master branch to the public git repository ###
```
git push ssh://cjlee112@repo.or.cz/srv/git/pygr.git master
```
Replace the username with your own repo.or.cz username... It will ask for your ssh passphrase.


# Additional Tutorials #
There are a **lot** of tutorials on how to use git.  Here are some I've found useful:
  * the [standard git tutorial](http://www.kernel.org/pub/software/scm/git/docs/gittutorial.html)
  * [Stanford student git tutorial](http://www-cs-students.stanford.edu/~blynn/gitmagic/)
  * [Git - SVN Crash Course](http://git.or.cz/course/svn.html) for developers used to Subversion.
  * [Rails project git tutorial](http://rails.lighthouseapp.com/projects/8994/sending-patches): very similar to the usage pattern I'm recommending for Pygr development.
  * [Getting Git](http://random-state.net/log/3410431842.html): a condensed view of git internals
  * [Git is the next Unix](http://www.advogato.org/person/apenwarr/diary/371.html)
  * [Git Cheat Sheet](http://cheat.errtheblog.com/s/git)