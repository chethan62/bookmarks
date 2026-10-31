#!/usr/bin/env python3
"""Dedupe a Netscape bookmarks export: merge same-name sibling folders, drop
duplicate URLs. Dry-run by default; nothing is written without --write.

    python3 dedupe.py ~/bookmarks_work.html              # report only
    python3 dedupe.py ~/bookmarks_work.html --write ~/bookmarks_clean.html
    python3 dedupe.py --selftest

Only stdlib. Parse -> merge -> dedupe -> report -> (optionally) emit.
"""
import argparse, html, sys
from html.parser import HTMLParser
from urllib.parse import urlsplit, parse_qsl, urlencode

TRACKING = ("utm_", "fbclid", "gclid", "mc_cid", "mc_eid", "ref_src", "si")


def norm(url):
    """Comparison key: ignore scheme, fragment, trailing slash, tracking params,
    host case. Returns None for non-http(s) links (kept as-is, never deduped)."""
    try:
        u = urlsplit(url.strip())
    except ValueError:
        return None
    if u.scheme.lower() not in ("http", "https") or not u.netloc:
        return None
    q = [(k, v) for k, v in parse_qsl(u.query, keep_blank_values=True)
         if not k.lower().startswith(TRACKING)]
    q.sort()
    host = u.netloc.lower()
    for dflt in (":80", ":443"):          # keep the port — localhost:8090 != :9117
        if host.endswith(dflt):
            host = host[: -len(dflt)]
            break
    path = u.path.rstrip("/")
    return f"{host}{path}" + (f"?{urlencode(q)}" if q else "")


class Node:
    __slots__ = ("kind", "title", "url", "children")

    def __init__(self, kind, title, url=None):
        self.kind, self.title, self.url = kind, title, url
        self.children = [] if kind == "folder" else None


class Parse(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = []
        self.stack = [self.root]
        self.depth = 0           # number of folder <DL>s we pushed
        self.pending = None      # folder created by <H3>, waiting for its <DL>
        self.closed = None       # folder whose </H3> just closed
        self.in_h3 = False
        self._last_link = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag != "a":
            self._last_link = None
        if tag == "h3":
            self.in_h3 = True
            self.pending = Node("folder", "")
        elif tag == "dl":
            if self.closed is not None:
                kids = self.closed.children
                self.stack.append(kids if kids is not None else [])
                self.depth += 1
                self.closed = None
        elif tag == "a" and a.get("href"):
            n = Node("link", "", a["href"])
            self.stack[-1].append(n)
            self._last_link = n

    def handle_endtag(self, tag):
        if tag == "h3":
            self.in_h3 = False
            if self.pending is not None:
                self.pending.title = self.pending.title.strip()
                self.stack[-1].append(self.pending)
                self.closed = self.pending
                self.pending = None
        elif tag == "dl" and self.depth:
            self.stack.pop()
            self.depth -= 1
        elif tag == "a" and self._last_link is not None:
            self._last_link.title = self._last_link.title.strip()
            self._last_link = None

    def handle_data(self, data):
        if self.in_h3 and self.pending:
            self.pending.title += data
        elif self._last_link is not None:
            self._last_link.title += data


def merge(nodes, merges):
    """Merge sibling folders sharing a name; recurse. Keeps first position."""
    out, seen = [], {}
    for n in nodes:
        if n.kind == "folder":
            key = n.title.strip().lower()
            if key in seen:
                tgt = seen[key]
                tgt.children.extend(n.children)
                merges.append((tgt.title, len(n.children)))
                continue
            seen[key] = n
        out.append(n)
    for n in out:
        if n.kind == "folder":
            n.children = merge(n.children, merges)
    return out


def dedupe(nodes, removed, seen, path=""):
    out = []
    for n in nodes:
        if n.kind == "folder":
            n.children = dedupe(n.children, removed, seen, f"{path}/{n.title}")
            out.append(n)
            continue
        k = norm(n.url)
        if k is None:
            out.append(n)
            continue
        if k in seen:
            removed.append((path or "(bar)", n.title, n.url))
            continue
        seen.add(k)
        out.append(n)
    return out


def emit(nodes, out, indent=1):
    p = "    " * indent
    for n in nodes:
        if n.kind == "folder":
            out.append(f'{p}<DT><H3>{html.escape(n.title)}</H3>')
            out.append(f"{p}<DL><p>")
            emit(n.children, out, indent + 1)
            out.append(f"{p}</DL><p>")
        else:
            out.append(f'{p}<DT><A HREF="{html.escape(n.url, quote=True)}">'
                       f"{html.escape(n.title)}</A>")


def to_html(nodes, title="Bookmarks"):
    body = []
    emit(nodes, body)
    return ("<!DOCTYPE NETSCAPE-Bookmark-file-1>\n"
            '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n'
            f"<TITLE>{html.escape(title)}</TITLE>\n<H1>{html.escape(title)}</H1>\n"
            "<DL><p>\n" + "\n".join(body) + "\n</DL><p>\n")


def count(nodes):
    return sum(count(n.children) if n.kind == "folder" else 1 for n in nodes)


def run(text):
    p = Parse()
    p.feed(text)
    merges, removed = [], []
    tree = dedupe(merge(p.root, merges), removed, set())
    return tree, merges, removed


def selftest():
    src = """<!DOCTYPE NETSCAPE-Bookmark-file-1><DL><p>
<DT><H3>Daily</H3><DL><p>
  <DT><A HREF="https://Example.com/a/?utm_source=x">A</A>
  <DT><A HREF="http://example.com/a#frag">A again</A>
</DL><p>
<DT><H3>Daily</H3><DL><p>
  <DT><A HREF="https://example.com/a/">A third</A>
  <DT><A HREF="https://example.com/b">B</A>
</DL><p>
<DT><H3>Other</H3><DL><p><DT><A HREF="https://example.com/b/">B again</A></DL><p>
</DL><p>"""
    tree, merges, removed = run(src)
    assert len(tree) == 2, [n.title for n in tree]                 # Daily merged into one
    assert tree[0].title == "Daily" and len(tree[0].children) == 2  # A once, B once
    assert tree[1].title == "Other" and len(tree[1].children) == 0  # B deduped across folders
    assert merges and merges[0][0] == "Daily"
    assert len(removed) == 3, removed                              # A x2 + B (cross-folder) dropped
    out = to_html(tree)
    tree2, m2, r2 = run(out)                                       # idempotent
    assert count(tree2) == count(tree) and not m2 and not r2
    assert norm("https://EXAMPLE.com/x/?utm_medium=1#f") == norm("http://example.com/x")
    assert norm("http://localhost:8090/") != norm("http://localhost:9117/")   # port is significant
    assert norm("https://example.com:443/a") == norm("https://example.com/a")  # default port is not
    print("selftest ok:", count(tree), "links,", len(merges), "merge(s),", len(removed), "removed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="?")
    ap.add_argument("--write", metavar="OUT")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.src:
        ap.error("need an input file (or --selftest)")
    text = open(a.src, encoding="utf-8", errors="replace").read()
    tree, merges, removed = run(text)
    before = count(ParseRoot(text))
    print(f"parsed {before} links")
    print(f"\nfolders merged: {len(merges)}")
    for name, n in merges:
        print(f"  + {name}: absorbed {n} child(ren)")
    print(f"\nbookmarks removed: {len(removed)}")
    for path, title, url in removed:
        print(f"  - [{path}] {title}  {url}")
    print(f"\nresult: {count(tree)} links  ({before - count(tree)} dropped)")
    if a.write:
        open(a.write, "w", encoding="utf-8").write(to_html(tree))
        print(f"wrote {a.write}")
    else:
        print("dry run — nothing written (pass --write OUT to save)")


def ParseRoot(text):
    p = Parse()
    p.feed(text)
    return p.root


if __name__ == "__main__":
    main()
