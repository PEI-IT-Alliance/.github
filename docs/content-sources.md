# Content sources for the profile README

`scripts/update_readme.py` fills two blocks in `profile/README.md`, each from its own
site API endpoint:

| Block | Source | Override |
|---|---|---|
| `EVENTS` | `https://www.peiitalliance.com/api/events` | `EVENTS_URL` |
| `NEWS` | `https://www.peiitalliance.com/api/news` | `NEWS_URL` |

The two endpoints do not share an envelope or field names, so each has its own reader.
Either can fail on its own. A source that is unreachable, malformed, or empty falls back
to a friendly link rather than failing the run, so the README never shows an error or a
blank section and the daily workflow stays green.

Both endpoints return their results already sorted, but the script sorts anyway.

## Events

Upcoming events only, wrapped in an envelope:

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
- `start.utc`, required. A real timestamp, so it is converted to America/Halifax for
  display: `Tue, Sep 22 · 6 PM`.
- `location`, optional. The API does not return it today. If it is added, it shows after
  the time: `Tue, Sep 22 · 6 PM · The Foundry`.

Events whose `start.utc` has passed are skipped, and the three soonest are shown. Event
URLs point at the ticketing host, so they are left alone. UTM tags are added only to
links on `peiitalliance.com`.

## News

Newest first, with a flat envelope and pagination fields:

```json
{
  "articles": [
    {
      "slug": "meet-vivian-beer",
      "title": "Meet Vivian Beer, on a multi-faceted AI journey",
      "subTitle": "An interview that is part of a series of profiles showcasing PEI's IT professionals",
      "url": "https://peiitalliance.com/news/meet-vivian-beer",
      "imageUrl": "https://peiitalliance.com/assets/news/2026/09/vivian-beer.jpg",
      "publishedDate": "September 21, 2026",
      "publishedAt": "2026-09-21T00:00:00.000Z"
    }
  ],
  "count": 5,
  "total": 14,
  "limit": 5,
  "offset": 0,
  "generatedAt": "2026-09-21T21:01:28.990Z"
}
```

What the script reads:

- `title` and `url`, both required. An article missing either is skipped.
- `publishedAt`, required. Unlike an event start, this is a date stamped at midnight UTC,
  not a real timestamp. Converting it to Halifax time would roll every date back a day,
  so it is read as given. `publishedDate` is the site's own display string and is not
  used, since its format varies between entries.

The three newest are shown. A piece from an earlier year shows its year, so
`Feb 20, 2025` does not read as this February. `?limit=` is supported if the default
page ever grows too large to be worth fetching.
