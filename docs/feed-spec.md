# Content sources for the profile README

`scripts/update_readme.py` fills two blocks in `profile/README.md`:

| Block | Source | Status |
|---|---|---|
| `EVENTS` | `https://www.peiitalliance.com/api/events` | Live |
| `NEWS` | `https://www.peiitalliance.com/feed.json` | Not built yet |

Either source can be missing. The script falls back to a friendly link rather than
failing, so the README never shows an error or a blank section.

## Events API

The site already serves this. It returns upcoming events only, wrapped in an envelope:

```json
{
  "message": "Success",
  "version": "1.0",
  "body": {
    "result": [
      {
        "name": "The Night Shift (Tuesday Edition)",
        "url": "https://locarius.io/events/4832/the-night-shift-tuesday-edition",
        "start": {
          "timezone": "America/Halifax",
          "local": "Tuesday, September 22, 2026 at 06:00 PM",
          "utc": "2026-09-22T21:00:51.672Z"
        },
        "summary": "Build your dream after hours!",
        "logo": "https://img.locarius.io/18335/7686ec04.../original.png",
        "capacity": 75,
        "is_free": true,
        "doorsOpenAt": "",
        "source": "locarius"
      }
    ]
  }
}
```

What the script reads:

- `name` and `url`, both required. An event missing either is skipped.
- `start.utc`, required, and converted to America/Halifax for display.
- `location`, optional. The API does not return it today. If it is added, it shows
  after the time, as `Tue, Sep 22 · 6 PM · The Foundry`.

Events whose `start.utc` has passed are skipped, and the three soonest are shown.
Event URLs point at the ticketing host, so they are left alone. UTM tags are added
only to links on `peiitalliance.com`.

## News feed

Not built yet. Format: [JSON Feed 1.1](https://www.jsonfeed.org/version/1.1/).

```json
{
  "version": "https://jsonfeed.org/version/1.1",
  "title": "PEI IT Alliance",
  "home_page_url": "https://www.peiitalliance.com",
  "feed_url": "https://www.peiitalliance.com/feed.json",
  "items": [
    {
      "id": "news-residency-cohort-4",
      "url": "https://www.peiitalliance.com/news/residency-cohort-4",
      "title": "Meet Residency cohort 4",
      "tags": ["news"],
      "date_published": "2026-09-15T09:00:00-03:00"
    }
  ]
}
```

Rules:

- `tags` must include `news`. Items without it are ignored.
- `date_published` needs a timezone offset. The three newest are shown.
- `url` goes without UTM tags. The script adds them.
- Serve with `Content-Type: application/feed+json` and cache for about an hour.

### Next.js route (App Router)

`app/feed.json/route.ts`:

```ts
import { getNews } from "@/lib/content"; // swap in your data source

export const revalidate = 3600;

export async function GET() {
  const news = await getNews();
  const base = "https://www.peiitalliance.com";

  return Response.json(
    {
      version: "https://jsonfeed.org/version/1.1",
      title: "PEI IT Alliance",
      home_page_url: base,
      feed_url: `${base}/feed.json`,
      items: news.map((n) => ({
        id: `news-${n.slug}`,
        url: `${base}/news/${n.slug}`,
        title: n.title,
        tags: ["news"],
        date_published: n.publishedAt,
      })),
    },
    { headers: { "Content-Type": "application/feed+json" } }
  );
}
```
