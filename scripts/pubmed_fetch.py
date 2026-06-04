"""
Thin wrapper around NCBI E-utilities for the AI curation agent.

The agent is restricted to `eutils.ncbi.nlm.nih.gov` for evidence lookups
(PRD §5.1.1). This wrapper:

  - Throttles requests (3 req/s without API key, 10 req/s with).
  - Caches abstracts in references_cache/PMID_xxxxxxxx.md in the same
    markdown-with-YAML-frontmatter format that linkml-reference-validator
    reads, so a successful fetch primes Layer 4 caching too.
  - Honors a 90-day TTL on cached entries (PRD §5.1.2). Use --force to
    re-fetch; use --offline to skip the network entirely.
  - Surfaces NCBI-flagged retractions in the cached metadata (eutils
    populates a `corrections_in` field when the article has been retracted
    or has a published erratum).

NCBI_API_KEY (env var, optional) raises the rate ceiling to 10 req/s and
counts against your registered account quota. Without it the wrapper uses
the public 3 req/s limit, which is enough for typical /curate workflows
(≤20 fetches per path).

Usage:
    python scripts/pubmed_fetch.py search "aspirin platelet aggregation"  # PMIDs only
    python scripts/pubmed_fetch.py fetch  PMID:35569550                   # one abstract
    python scripts/pubmed_fetch.py fetch  PMID:35569550 PMID:36129273     # batch
    python scripts/pubmed_fetch.py fetch  PMID:35569550 --force           # bypass cache
    python scripts/pubmed_fetch.py fetch  PMID:35569550 --offline         # cache-only
    python scripts/pubmed_fetch.py info   PMID:35569550                   # show cached state without fetching
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from xml.etree import ElementTree as ET

REPO = Path(__file__).resolve().parent.parent
CACHE_DIR = REPO / "references_cache"

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CACHE_TTL_DAYS = 90

API_KEY = os.environ.get("NCBI_API_KEY", "").strip()
TOOL = "drugmechdb-ai-curation"
EMAIL = os.environ.get("NCBI_CONTACT_EMAIL", "drugmechdb-curation@example.org")

# Throttle: 10 req/s with key, 3 req/s without.
_RATE_INTERVAL = 0.11 if API_KEY else 0.34
_last_call = 0.0


PMID_RE = re.compile(r"^PMID:(\d+)$")
PLAIN_PMID_RE = re.compile(r"^\d+$")


def _throttle() -> None:
    global _last_call
    delta = time.monotonic() - _last_call
    if delta < _RATE_INTERVAL:
        time.sleep(_RATE_INTERVAL - delta)
    _last_call = time.monotonic()


def _http_get(url: str) -> bytes:
    _throttle()
    req = urllib.request.Request(url, headers={"User-Agent": f"{TOOL} ({EMAIL})"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def _eutils_url(endpoint: str, params: dict) -> str:
    p = dict(params)
    p["tool"] = TOOL
    p["email"] = EMAIL
    if API_KEY:
        p["api_key"] = API_KEY
    return f"{EUTILS_BASE}/{endpoint}?{urllib.parse.urlencode(p)}"


def _normalize_pmid(s: str) -> str:
    """Return the bare numeric PMID for either 'PMID:1234' or '1234'."""
    s = s.strip()
    m = PMID_RE.match(s)
    if m:
        return m.group(1)
    if PLAIN_PMID_RE.match(s):
        return s
    raise ValueError(f"not a PMID: {s!r}")


def _curie(pmid_bare: str) -> str:
    return f"PMID:{pmid_bare}"


def cache_path(pmid_bare: str) -> Path:
    return CACHE_DIR / f"PMID_{pmid_bare}.md"


def cache_is_fresh(path: Path, ttl_days: int = CACHE_TTL_DAYS) -> bool:
    if not path.exists():
        return False
    # Parse fetched_at from frontmatter if present; fall back to mtime.
    try:
        text = path.read_text(encoding="utf-8")
        if text.startswith("---"):
            head = text.split("---", 2)[1]
            for line in head.splitlines():
                if line.startswith("fetched_at:"):
                    ts = line.split(":", 1)[1].strip().strip("'\"")
                    parsed = dt.datetime.fromisoformat(ts.rstrip("Z"))
                    age = dt.datetime.now(dt.timezone.utc) - parsed.replace(
                        tzinfo=dt.timezone.utc
                    )
                    return age.days < ttl_days
    except Exception:
        pass
    age = dt.datetime.now() - dt.datetime.fromtimestamp(path.stat().st_mtime)
    return age.days < ttl_days


def _yaml_quote(value: str) -> str:
    """Quote per linkml-reference-validator's frontmatter convention."""
    if any(ch in value for ch in "[]{}:,#&*?|<>=!%@`\"'\\") or value != value.strip():
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    if value.lower() in ("true", "false", "yes", "no", "on", "off", "null", "~"):
        return f'"{value}"'
    return value


def _write_cache(pmid_bare: str, record: dict) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = cache_path(pmid_bare)
    fetched_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

    lines = ["---"]
    lines.append(f"reference_id: PMID:{pmid_bare}")
    if record.get("title"):
        lines.append(f"title: {_yaml_quote(record['title'])}")
    if record.get("authors"):
        lines.append("authors:")
        for a in record["authors"]:
            lines.append(f"- {_yaml_quote(a)}")
    if record.get("journal"):
        lines.append(f"journal: {_yaml_quote(record['journal'])}")
    if record.get("year"):
        lines.append(f"year: '{record['year']}'")
    if record.get("doi"):
        lines.append(f"doi: {record['doi']}")
    if record.get("retracted"):
        lines.append("retracted: true")
    if record.get("corrections_in"):
        lines.append("corrections_in:")
        for c in record["corrections_in"]:
            lines.append(f"- {_yaml_quote(c)}")
    lines.append("content_type: abstract")
    lines.append(f"fetched_at: '{fetched_at}'")
    lines.append("---")
    lines.append("")
    if record.get("title"):
        lines.append(f"# {record['title']}")
        if record.get("authors"):
            lines.append(f"**Authors:** {', '.join(record['authors'])}")
        if record.get("journal"):
            jr = record["journal"] + (f" ({record['year']})" if record.get("year") else "")
            lines.append(f"**Journal:** {jr}")
        if record.get("doi"):
            lines.append(f"**DOI:** [{record['doi']}](https://doi.org/{record['doi']})")
        lines.append("")
        lines.append("## Content")
        lines.append("")
    if record.get("abstract"):
        lines.append(record["abstract"])
    elif record.get("title"):
        lines.append("(No abstract available — title only.)")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _parse_pubmed_xml(xml_bytes: bytes) -> list[dict]:
    """Parse an esummary/efetch response into per-article records."""
    out: list[dict] = []
    root = ET.fromstring(xml_bytes)
    # efetch with rettype=xml returns PubmedArticleSet/PubmedArticle.
    for article in root.findall(".//PubmedArticle"):
        med = article.find(".//MedlineCitation")
        pmid = (med.findtext("PMID") or "").strip() if med is not None else ""
        rec: dict = {"pmid": pmid}

        # Title
        title_el = article.find(".//Article/ArticleTitle")
        rec["title"] = "".join(title_el.itertext()).strip() if title_el is not None else None

        # Abstract — may be split across multiple AbstractText elements with Label attrs
        abs_parts = []
        for at in article.findall(".//Article/Abstract/AbstractText"):
            label = at.get("Label")
            text = "".join(at.itertext()).strip()
            if label:
                abs_parts.append(f"**{label}:** {text}")
            else:
                abs_parts.append(text)
        rec["abstract"] = "\n\n".join(abs_parts) if abs_parts else None

        # Authors
        authors = []
        for au in article.findall(".//Article/AuthorList/Author"):
            ln = au.findtext("LastName") or ""
            init = au.findtext("Initials") or ""
            coll = au.findtext("CollectiveName")
            if coll:
                authors.append(coll.strip())
            elif ln:
                authors.append((ln + " " + init).strip())
        rec["authors"] = authors

        # Journal + Year
        rec["journal"] = article.findtext(".//Article/Journal/Title")
        rec["year"] = article.findtext(".//Article/Journal/JournalIssue/PubDate/Year") or \
                      article.findtext(".//Article/Journal/JournalIssue/PubDate/MedlineDate")
        if rec["year"]:
            # MedlineDate may be like "2019 Jun-Jul" — keep first 4 digits.
            m = re.match(r"(\d{4})", rec["year"])
            if m:
                rec["year"] = m.group(1)

        # DOI
        for aid in article.findall(".//Article/ELocationID"):
            if aid.get("EIdType") == "doi":
                rec["doi"] = aid.text.strip() if aid.text else None
                break

        # Retraction / errata signal
        history = article.findall(".//CommentsCorrectionsList/CommentsCorrections")
        rec["retracted"] = any(c.get("RefType") == "RetractionIn" for c in history)
        rec["corrections_in"] = [
            (c.findtext("PMID") or c.findtext("RefSource") or "").strip()
            for c in history
            if c.get("RefType") in ("RetractionIn", "CorrectedAndRepublishedIn", "ErratumIn")
        ]
        rec["corrections_in"] = [c for c in rec["corrections_in"] if c]
        out.append(rec)
    return out


def fetch_one(pmid: str, force: bool = False, offline: bool = False) -> dict:
    """Fetch one PMID. Returns a record dict; writes cache on success."""
    bare = _normalize_pmid(pmid)
    cache_file = cache_path(bare)

    if not force and cache_is_fresh(cache_file):
        return {"pmid": bare, "cached": True, "path": str(cache_file)}

    if offline:
        if cache_file.exists():
            return {"pmid": bare, "cached": True, "stale": True, "path": str(cache_file)}
        return {"pmid": bare, "error": "offline and not cached"}

    url = _eutils_url("efetch.fcgi", {
        "db": "pubmed", "id": bare, "rettype": "xml", "retmode": "xml",
    })
    try:
        xml = _http_get(url)
    except Exception as e:
        return {"pmid": bare, "error": f"fetch failed: {e}"}

    records = _parse_pubmed_xml(xml)
    if not records:
        return {"pmid": bare, "error": "no record returned by PubMed"}
    record = records[0]
    if not record.get("abstract"):
        # PRD §5.1.2: paywalled / no-abstract — surface but don't write cache
        # (so future runs retry; downstream agent records evidence_source OTHER).
        return {"pmid": bare, "error": "no abstract available", "title": record.get("title")}
    written = _write_cache(bare, record)
    return {"pmid": bare, "cached": False, "path": str(written), "retracted": record.get("retracted", False)}


def search(query: str, retmax: int = 20) -> list[str]:
    """Return a list of bare PMIDs matching the query, max retmax."""
    url = _eutils_url("esearch.fcgi", {
        "db": "pubmed", "term": query, "retmax": retmax, "retmode": "json",
    })
    try:
        data = json.loads(_http_get(url))
    except Exception as e:
        print(f"search failed: {e}", file=sys.stderr)
        return []
    return data.get("esearchresult", {}).get("idlist", [])


def info(pmid: str) -> dict:
    bare = _normalize_pmid(pmid)
    cache_file = cache_path(bare)
    if not cache_file.exists():
        return {"pmid": bare, "cached": False}
    return {
        "pmid": bare, "cached": True,
        "path": str(cache_file),
        "fresh": cache_is_fresh(cache_file),
        "size_bytes": cache_file.stat().st_size,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_search = sub.add_parser("search", help="esearch — return PMIDs matching a query")
    p_search.add_argument("query", help="PubMed search expression")
    p_search.add_argument("--max", type=int, default=20, dest="retmax")

    p_fetch = sub.add_parser("fetch", help="efetch — pull abstract(s) and cache")
    p_fetch.add_argument("pmids", nargs="+", help="One or more PMIDs (PMID:nnn or nnn)")
    p_fetch.add_argument("--force", action="store_true", help="Bypass cache freshness check")
    p_fetch.add_argument("--offline", action="store_true", help="Use cache only; never hit PubMed")
    p_fetch.add_argument("--json", action="store_true", help="Emit machine-readable JSON")

    p_info = sub.add_parser("info", help="Show cache state for a PMID (no network)")
    p_info.add_argument("pmid")
    p_info.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.cmd == "search":
        ids = search(args.query, retmax=args.retmax)
        for pid in ids:
            print(_curie(pid))
        return 0 if ids else 1

    if args.cmd == "fetch":
        results = [fetch_one(p, force=args.force, offline=args.offline) for p in args.pmids]
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for r in results:
                tag = "ERROR" if r.get("error") else ("CACHED" if r.get("cached") else "FETCHED")
                bits = [f"{tag} PMID:{r['pmid']}"]
                if r.get("error"):
                    bits.append(r["error"])
                if r.get("retracted"):
                    bits.append("[RETRACTED]")
                if r.get("path"):
                    bits.append(r["path"])
                print("  ".join(bits))
        return 0 if all(not r.get("error") for r in results) else 1

    if args.cmd == "info":
        out = info(args.pmid)
        if args.json:
            print(json.dumps(out, indent=2))
        else:
            print(out)
        return 0

    parser.error("unknown cmd")


if __name__ == "__main__":
    sys.exit(main())
