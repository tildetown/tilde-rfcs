# RFC 1: Tilde-Wiki Project

| Metadata       |                  |
|-|-|
| Author         | Nathaniel Smith ([~vilmibm](https://tilde.town/~vilmibm)), Robert Miles ([~minerobber](http://tilde.town/~minerobber))         |
| Status         | accepted         |

## Preamble

This RFC was submitted by ~vilmibm in the [tildetown/tilde-wiki](https://github.com/tildetown/wiki) repo in Org-mode format. I, ~minerobber, have converted it into Markdown and submitted it as an RFC in this repo. You can read the original Org-mode document [here](https://github.com/tildetown/wiki/blob/master/rfc.org).

## Abstract

   Many moons ago, I thought it would be interesting to have a user that we all
   shared whose home directory was a git repo. In addition to being able to modify the shared
   user's home directory, it had a public_html that could be filled with pretty standard wiki style content.
   
   Users took to the html portion of the wiki user and generated a lot of useful
   content. the home directory / shared user aspect, however, was left untouched
   for years.

   Thus, this RFC outlines both a shift to a formalized wiki that retains the
   spirit of the origial idea (git based, shell oriented, low barrier to entry)
   while streamlining and improving it.

## Glossary

   - /the wiki/: the files in a git repo that constitute the town's wiki content. accessible by command line or web.
   - `wiki`: the `wiki` command, used locally to work on the wiki and publish changes
   - `tildetown/wiki`: a github repo for storing the content of our wiki
   - `tildetown/tilde-wiki`: a github repo for storing the ~wiki~ command

## Proposal

   - the system path /wiki , a git repository (structure to follow).
   - the url tilde.town/wiki, configured at nginx level to serve system path /wiki/compiled
   - Deleting the wiki user and setting a redirect in nginx from /~wiki to /wiki
   - a `wiki` command used for initializing, adding to, and publishing the wiki

## Wiki Layout

   The following is the proposed layout for the wiki with sample files

```
   /wiki
   |- .git/
   |- .gitignore
   |- wiki-githooks
   |- src/
   |-- toc.md
   |-- header.md
   |-- footer.md
   |-- articles/
   |---- index.md
   |---- new_user.md
   |---- ssh.html
   |---- editors/
   |------ vim.md
   |------ ed.txt
   |------ nano.html
```

After a `wiki publish`, the resulting site structure will look like this:

```
  /var/www/tilde.town/html/wiki/
  |- index.html
  |- new_user.html
  |- ssh.html
  |- editors/
  |-- ed.html
  |-- nano.html
  |-- vim.html
```

## wiki Command

   The `wiki` command has 4 principles:

   1. `wiki` should complement, not replace, ~git~
   2. `wiki` subcommands take actions that can be easily summarized in a step-by-step way
   3. `wiki` should be fully documented both at rest (manual page) and live (-h, usage info)
   4. as needed, `wiki` should print human readable and informative errors.

### Subcommands

#### init
   - Clones /wiki to ~/wiki, erroring if directory exists
   - Configures .git/config accordingly
   - prints next steps
#### preview
   - commits working tree
   - compiles wiki to `~/public_html/wiki`
   - prints link to https://tilde.town/~user/wiki/
#### publish
   - commits working tree
   - attempts to pull from origin
     - if this fails, reports on the failure and says to fall back to `git` or ask for help
     - if this succeeds, pushes to origin
   - compiles all source files and outputs to `~/var/www/tilde.town/wiki`
#### get <path>
   - given a valid wiki path, opens it in w3m
   - if no path, suggests creating it with `$EDITOR`
#### reset
   - prompts y/N
   - `git fetch origin && git reset --hard origin`

  NB: preview and publish both audit all links in changed files for absolute
  links to the wiki and error, explaining relative links.

## Web Presentation

   A guiding principle of this RFC is that the wiki should be comfortable to
   view locally via w3m or similar. A CSS oriented table of content sidebar is
   thus out of the question. Thus, I propose the following:

   - A standalone page, `toc.html`, that lists the directory structure / pages of the wiki (i.e., a site map)
   - A header with a site title (/The Tilde Town Wiki/, for example) and basic navigation 
     links (/home/, /table of contents/, /how to contribute/, /tilde.town home/)
   - a footer with metadata (/page compile time/, /most recent author/)
   - Source files in `.txt` format are turned into HTML naively; `\n\n` -> `</p><p>`.

   Compiled HTML pages are put together naively: ie, it is assumed that the
   content of a given page can be shoved into a `<body>` element.

#### Page titling

   After compiling to HTML but before combining with `head.md`, if the first
   line of a page's content is an h1 or h2 element its content will be used as
   the `<title>` of the page.

## Open Questions

   I'd appreciate feedback on these questions (in addition to general feedback).

  1. The `compiled/` directory is ignored by git, but compiled both locally and remotely. 
     Does this make sense? Should it not live in the folder at all?
    - After discussing with \~datagrok, I've decided to target directories outside the repo for compilation.
  3. is `/wiki/src/articles/` too deep of a path? is it cumbersome? i like that it is 
     explicit and i have a policy of erring on the side of explicitness.
  4. Should the `wiki` command be implemented using Python's `subprocess` modules to call
      out to `git` or use something like `PyGit2` or `GitPython`?

(note to ~vilmibm: you can edit this, just tell me so I can render the new version (be sure to include the date with the edit))

## Future Improvements

   - A macro system that can handle the following expansions:
     - prefixing a string with ~: expands to a user's page link. e.g. `~vilmibm`
     - prefixing a string with ~wiki: expands to a wiki page link, e.g. `~wiki:editors/ed.html/`
   - modify the `wiki get <path>` command to act as a local flavor replacement
     of `man`. This might look like a different compilation "target" distinct
     from compiling HTML for the web.
   - An `admin` subcommand with sub-subcommands that can start a tilde-style wiki
     at an arbitrary path. For now, the initial seeding of `/wiki` is all manual.
