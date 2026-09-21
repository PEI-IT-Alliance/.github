# Feed spec for peiitalliance.com

The profile README reads `https://www.peiitalliance.com/feed.json`. Format: [JSON Feed 1.1](https://www.jsonfeed.org/version/1.1/) with one custom `_event` extension.

## Shape

```json
{
  "version": "https://jsonfeed.org/version/1.1",
  "title": "PEI IT Alliance",
  "home_page_url": "https://www.peiitalliance.com",
  "feed_url": "https://www.peiitalliance.com/feed.json",
  "items": [
    {
      "id": "event-night-shift-2026-09-24",
      "url": "https://www.peiitalliance.com/the-night-shift",
      "title": "The Night Shift",
      "tags": ["event"],
      "date_published": "2026-09-01T12:00:00-03:00",
      "_event": {
        "start": "2026-09-24T18:00:00-03:00",
        "end": "2026-09-24T21:00:00-03:00",
        "location": "The Foundry, Charlottetown"
      }
    },
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

## Rules

- `tags` holds `event` or `news`.
- Events need `_event.start` with a timezone offset. Past events get skipped.
- `url` goes without UTM tags. The script adds them.
- Serve with `Content-Type: application/feed+json` and cache for about an hour.

## Next.js route (App Router)

`app/feed.json/route.ts`:

```ts
import { getEvents, getNews } from "@/lib/content"; // swap in your data source

export const revalidate = 3600;

export async function GET() {
  const [events, news] = await Promise.all([getEvents(), getNews()]);
  const base = "https://www.peiitalliance.com";

  const items = [
    ...events.map((e) => ({
      id: `event-${e.slug}`,
      url: `${base}${e.path}`,
      title: e.title,
      tags: ["event"],
      date_published: e.publishedAt,
      _event: { start: e.startsAt, end: e.endsAt, location: e.location },
    })),
    ...news.map((n) => ({
      id: `news-${n.slug}`,
      url: `${base}/news/${n.slug}`,
      title: n.title,
      tags: ["news"],
      date_published: n.publishedAt,
    })),
  ];

  return Response.json(
    {
      version: "https://jsonfeed.org/version/1.1",
      title: "PEI IT Alliance",
      home_page_url: base,
      feed_url: `${base}/feed.json`,
      items,
    },
    { headers: { "Content-Type": "application/feed+json" } }
  );
}
```
