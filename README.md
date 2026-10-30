# 5 Games to Learn Linux

Five interactive ways to build real command-line skill. Every link checked live (2026-10-30, all HTTP 200).

| # | Game | Shell | Level | What it teaches |
|---|------|-------|-------|-----------------|
| 1 | [OverTheWire: Bandit](https://overthewire.org/wargames/bandit/) | SSH into real hosts | beginner | 34 levels of `ls`/`cat`/`grep`/`find`/permissions — the canonical entry point |
| 2 | [SadServers](https://sadservers.com/) | live broken VMs | intermediate → engineer | Troubleshooting real infra: "LeetCode for Linux & DevOps", no signup |
| 3 | [Bashcrawl](https://github.com/bamr87/bashcrawl) | your own local bash | beginner | Dungeon crawl where directories are rooms and `scroll` files are the story. GPLv3 fork of [Seth Kenlon's original](https://gitlab.com/slackermedia/bashcrawl) |
| 4 | [Terminus](https://mprat.github.io/Terminus/) | in-browser JS emulator | beginner | MIT class project turned game; gentle pacing, dated 2011-era UI |
| 5 | [CMD Challenge](https://cmdchallenge.com/) | sandboxed runner | beginner → intermediate | One-command golf — many correct answers per puzzle, teaches muscle memory |

## Quick start

**Bandit** — `ssh bandit0@bandit.labs.overthewire.org -p 2220` (password `bandit0`), then follow the level pages.

**Bashcrawl** — no install for the browser version: <https://bamr87.github.io/bashcrawl/>. Or locally:

```bash
git clone https://github.com/bamr87/bashcrawl.git
cd bashcrawl && ./setup.sh
cd entrance && cat scroll
```

**SadServers** — open the site, pick a scenario, get a terminal in a broken container. Fix it, get scored.

**Terminus** — <https://mprat.github.io/Terminus/> — play in the browser.

**CMD Challenge** — <https://cmdchallenge.com/> — type a one-liner, it runs and diffs the output.

## Suggested order

Already comfortable with a shell: **SadServers** first, then **CMD Challenge** for drills.
New to the terminal: **Bandit** → **Bashcrawl** for the fun pass → **CMD Challenge**.

## License

List only — links belong to their respective projects (Bashcrawl is GPL-3.0-only; Bandit, SadServers, Terminus and CMD Challenge have their own terms).
