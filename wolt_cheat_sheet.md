### Wolt programmatic access — cheat-sheet for your AI agent

Blunt, everything you need, nothing you don’t.

---

## 1  Official merchant APIs (need Wolt creds)

| Function                                                         | Endpoint (base `https://pos-integration-service.wolt.com`) | Field to watch                                    |
| ---------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------- |
| **Venue status**                                                 | `GET /venues/{venueId}/status`                             | `is_online`, `is_open` ([Wolt for Developers][1]) |
| Orders (webhook + pull), menus, opening-times, Drive courier API | See dev portal pages                                       |                                                   |

☑️ OAuth2 bearer token issued after you sign the *Marketplace Integrations* agreement.
If you run the restaurant, **this is the stable, SLA-backed route**.

---

## 2  Unofficial “consumer” API (no login, works for Israel)

```
GET https://consumer-api.wolt.com/order-catalog/api/v1/venues/<SLUG>/dynamic
Headers: User-Agent, Origin:https://wolt.com, x-platform:web
```

Response → `venue.online : true|false` (open for orders) ([Medium][2])

Bulk scan nearby venues:

```
GET https://consumer-api.wolt.com/order-catalog/api/v1/pages/restaurants?lat=<LAT>&lon=<LON>&radius=<M>
```

Same `online` flag for every item.

*404* = bad slug, *430* = you hit the retired `restaurant-api.wolt.com` host or forgot the headers.

---

## 3  Finding the correct **slug**

1. **Geo-browse** endpoint above → iterate `venue.name` until you match the restaurant name, then grab `venue.slug`.
2. Scrape it from the public site URL:
   `https://wolt.com/en/isr/tel-aviv/restaurant/<SLUG>`
3. Search endpoint (undocumented but live):
   `GET https://consumer-api.wolt.com/search/v2/venues?query=<text>&lat=<lat>&lon=<lon>`

Cache slugs; they rarely change.

---

## 4  Rate limits & etiquette

* Consumer API ≈ 60 req/min/IP; add jitter/back-off.
* Don’t call unofficial endpoints from browser JS (CORS blocked) — use your server or a Cloudflare Worker.
* For official APIs, quotas are in your contract.

---

## 5  Apify & other scrapers

The off-the-shelf **“Wolt Restaurants Scraper”** actor exports menu, rating, etc. **but not the `online` flag**, so it’s useless for availability tracking. Roll your own actor that hits the consumer API if you need SaaS hosting. ([Apify][3])

---

## 6  Minimal Python (sync)

```python
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://wolt.com",
    "x-platform": "web",
    "Accept-Language": "en"
}

def is_open(slug: str) -> bool:
    url = f"https://consumer-api.wolt.com/order-catalog/api/v1/venues/{slug}/dynamic"
    r = requests.get(url, headers=HEADERS, timeout=5)
    if r.status_code == 404:
        raise ValueError(f"Unknown slug: {slug}")
    r.raise_for_status()
    return r.json()["venue"]["online"]
```

---

## 7  Links for further digging

* Dev portal (Venue, Order, Menu, Drive APIs) – [https://developer.wolt.com/docs/api](https://developer.wolt.com/docs/api)
* Medium reverse-engineering walkthrough (old host but good field map) – [https://medium.com/analytics-vidhya/exploring-the-api-of-a-website-8579b04df28f](https://medium.com/analytics-vidhya/exploring-the-api-of-a-website-8579b04df28f)
* Backend-internship repo showing **`/venues/<slug>/dynamic`** example – [https://github.com/woltapp/backend-internship-2025](https://github.com/woltapp/backend-internship-2025) ([GitHub][4])
* Apify actor page – [https://apify.com/lucen\_data/wolt-restaurants-scraper](https://apify.com/lucen_data/wolt-restaurants-scraper)

---

### Bottom line

* **Restaurant owner?** Use the official Venue API (`is_online`/`is_open`).
* **Just monitoring availability?** Hit the consumer `/dynamic` endpoint with proper headers; discover slugs via the geo-browse call.
  Feed this into your agent and ship.

[1]: https://developer.wolt.com/docs/api/venue?utm_source=chatgpt.com "Venue API"
[2]: https://medium.com/analytics-vidhya/exploring-the-api-of-a-website-8579b04df28f "Exploring Wolt’s web API. Nowadays, due to the increasing… | by Tomer Chaim | Analytics Vidhya | Medium"
[3]: https://apify.com/lucen_data/wolt-restaurants-scraper/api?utm_source=chatgpt.com "Wolt Restaurants Scraper 🥡 API"
[4]: https://github.com/woltapp/backend-internship-2025 "GitHub - woltapp/backend-internship-2025: The pre-assignment for backend internship applicants"
