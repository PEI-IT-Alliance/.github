#!/usr/bin/env python3
"""Refresh the Next up and From the Alliance blocks in profile/README.md.

Events and news both come from the PEI IT Alliance site API. Standard
library only.

Falls back to a friendly link if either source is missing or empty, so the
README never shows an error or a blank section.
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl
from zoneinfo import ZoneInfo

EVENTS_URL = os.environ.get("EVENTS_URL", "https://www.peiitalliance.com/api/events")
NEWS_URL = os.environ.get("NEWS_URL", "https://www.peiitalliance.com/api/news")
README = os.environ.get("README_PATH", "profile/README.md")
TZ = ZoneInfo("America/Halifax")
UTM = {"utm_source": "github", "utm_medium": "org_profile", "utm_campaign": "readme"}
SITE_HOSTS = {"peiitalliance.com", "www.peiitalliance.com"}
SITE_HOST = "www.peiitalliance.com"
MAX_EVENTS = 3
MAX_NEWS = 3

EVENTS_FALLBACK = (
    "We're lining up the next few events. See the full calendar at "
    "[peiitalliance.com/events](https://www.peiitalliance.com/events?utm_source=github"
    "&utm_medium=org_profile&utm_campaign=readme)."
)
NEWS_FALLBACK = (
    "Catch up on community news at "
    "[peiitalliance.com/news](https://www.peiitalliance.com/news?utm_source=github"
    "&utm_medium=org_profile&utm_campaign=readme)."
)


def with_utm(url):
    """Tag our own links so the site can attribute them. Leave other hosts alone.

    The APIs return bare peiitalliance.com links. The profile uses the www
    subdomain throughout, so normalise them and skip a redirect.
    """
    parts = urlparse(url)
    if parts.netloc.lower() not in SITE_HOSTS:
        return url
    query = dict(parse_qsl(parts.query))
    query.update(UTM)
    return urlunparse(parts._replace(netloc=SITE_HOST, query=urlencode(query)))


def parse_dt(value):
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ)
    return dt


def md_escape(text):
    return re.sub(r"([\[\]|])", r"\\\1", text.strip())


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "pei-it-alliance-profile-bot"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def fetch_events():
    """The API wraps its payload: {"body": {"result": [...]}}."""
    payload = fetch_json(EVENTS_URL)
    if isinstance(payload, list):
        return payload
    body = payload.get("body") or {}
    result = body.get("result")
    if result is None:
        result = payload.get("result", [])
    return result if isinstance(result, list) else []


def fetch_news():
    """The news API returns {"articles": [...]}, newest first."""
    payload = fetch_json(NEWS_URL)
    if isinstance(payload, list):
        return payload
    articles = payload.get("articles")
    return articles if isinstance(articles, list) else []


def render_events(items, now):
    events = []
    for item in items:
        start = parse_dt((item.get("start") or {}).get("utc"))
        title = (item.get("name") or "").strip()
        url = item.get("url")
        if not (start and title and url) or start < now:
            continue
        events.append((start, title, url, item.get("location")))
    events.sort(key=lambda e: e[0])
    if not events:
        return EVENTS_FALLBACK
    lines = []
    for start, title, url, where in events[:MAX_EVENTS]:
        local = start.astimezone(TZ)
        when = local.strftime("%a, %b %-d · %-I:%M %p").replace(":00 ", " ")
        detail = f"{when} · {md_escape(where)}" if where else when
        lines.append(f"- **[{md_escape(title)}]({with_utm(url)})**  \n  {detail}")
    lines.append("")
    lines.append(
        "[See all events →](https://www.peiitalliance.com/events?utm_source=github"
        "&utm_medium=org_profile&utm_campaign=readme)"
    )
    return "\n".join(lines)


def render_news(items, now):
    news = []
    for item in items:
        published = parse_dt(item.get("publishedAt"))
        title = (item.get("title") or "").strip()
        url = item.get("url")
        if not (published and title and url):
            continue
        news.append((published, title, url))
    news.sort(key=lambda n: n[0], reverse=True)
    if not news:
        return NEWS_FALLBACK
    lines = []
    for published, title, url in news[:MAX_NEWS]:
        # Published dates are stamped at midnight UTC. Converting them to
        # Halifax time would roll each one back a day, so read them as given.
        # Older pieces need the year, or February 2023 reads as this February.
        when = (
            published.strftime("%b %-d")
            if published.year == now.year
            else published.strftime("%b %-d, %Y")
        )
        lines.append(f"- [{md_escape(title)}]({with_utm(url)}) · {when}")
    return "\n".join(lines)


def replace_block(text, name, body):
    pattern = re.compile(rf"(<!-- {name}:START -->\n).*?(\n<!-- {name}:END -->)", re.S)
    if not pattern.search(text):
        sys.exit(f"Marker {name} missing from {README}")
    return pattern.sub(lambda m: m.group(1) + body + m.group(2), text)


def main():
    now = datetime.now(timezone.utc)

    try:
        events = fetch_events()
    except Exception as err:  # network blip, bad JSON, API down
        print(f"Events unavailable ({err}). Using fallback text.")
        events = []

    try:
        news = fetch_news()
    except Exception as err:  # network blip, bad JSON, API down
        print(f"News unavailable ({err}). Using fallback text.")
        news = []

    with open(README, encoding="utf-8") as f:
        original = f.read()

    updated = replace_block(original, "EVENTS", render_events(events, now))
    updated = replace_block(updated, "NEWS", render_news(news, now))

    if updated == original:
        print("No changes.")
        return
    with open(README, "w", encoding="utf-8") as f:
        f.write(updated)
    print("README updated.")


if __name__ == "__main__":
    main()
