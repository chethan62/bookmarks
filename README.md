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

## Handy sites

Pulled from a real browser bookmark set — the ones worth keeping, **full site URLs**, nothing local (`localhost` dashboards, chat-thread links, tokenised player URLs and the streaming/anime/piracy bookmarks are deliberately left out).

**Linux & desktop**

- [DistroFinder](https://distro-finder.com/) — pick a distro by answers, not vibes
- [HelloGitHub](https://hellogithub.com/en) — monthly open-source project digest
- [Trendshift](https://trendshift.io/) — what's climbing on GitHub
- [Vicinae](https://github.com/vicinaehq/vicinae) — native, fast, extensible desktop launcher
- [GeeksforGeeks: make your terminal look awesome](https://www.geeksforgeeks.org/linux-unix/how-to-make-linux-terminal-look-awesome/)

**Learning & dev reference**

- [roadmap.sh](https://roadmap.sh/) — developer roadmaps
- [OverAPI](https://overapi.com/) — every cheat sheet in one place
- [Learn Anything](https://learn-anything.xyz/) — topic→resource maps
- [Mind Luster](https://www.mindluster.com/) — 300k MOOC courses, free certificates
- [Coddy](https://coddy.tech/) — interactive C++/fundamentals track
- [Gitingest](https://gitingest.com/) — turn any repo into one LLM-friendly text blob
- [GitDiagram](https://gitdiagram.com/) — visualise any GitHub repo
- [GitReverse](https://www.gitreverse.com/) — repo anatomy/insight
- [Bellingcat toolkit](https://bellingcat.gitbook.io/toolkit) — online investigation tools
- [NoSignups](https://nosignups.net/) — open-source tools, no account
- [SAP FICO tutorials](https://www.saponlinetutorials.com/sap-fico-module-training-tutorials-sap-fi-materials/)

**AI chat / models**

- [ChatGPT](https://chatgpt.com/) · [Claude](https://claude.ai/new) · [Gemini](https://gemini.google.com/app)
- [DeepSeek](https://chat.deepseek.com/) · [Z.ai (GLM)](https://chat.z.ai/) · [Kimi](https://www.kimi.com/en)
- [Perplexity](https://www.perplexity.ai/) · [Meta AI](https://www.meta.ai/) · [Tusk Central](https://tuskcentral.ai/chat) — many models, free
- [DeepInfra](https://deepinfra.com/) — hosted open models (incl. text-to-image)

**GPU rental**

- [Vast.ai](https://vast.ai/) · [Jarvislabs](https://jarvislabs.ai/) · [Yotta](https://console.yottalabs.ai/) · [E2E Networks](https://myaccount.e2enetworks.com/)

Link check (2026-10-30): every URL above answered 200 except the handful behind Cloudflare bot walls — `chatgpt.com`, `claude.ai`, `chat.deepseek.com`, `meta.ai`, `coddy.tech` — which return 403 to `curl` but load normally in a browser. `hyprstylish.com` was dropped: its DNS no longer resolves.

## License

List only — links belong to their respective projects (Bashcrawl is GPL-3.0-only; Bandit, SadServers, Terminus and CMD Challenge have their own terms).
