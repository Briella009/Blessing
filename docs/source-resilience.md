# Source resilience and link-health monitoring

AAIO depends on public evidence. Court judgments move, news sites redesign, fact-check pages disappear, rate limits change and bot-protection systems can block automated research tools. A source-traceable incident dataset therefore needs to monitor its evidence links without confusing **web availability** with **evidence validity**.

## Principle

A failed automated request does **not** mean an incident is false, unsupported or ready for removal.

The source-health audit is an operational maintenance signal. It answers a narrow question: *could an automated GitHub runner reach this public URL at the time of the check?*

It does not determine whether:

- the source remains trustworthy;
- the incident remains correctly classified;
- a human browser can reach the page;
- a bot challenge or geoblock is temporary;
- an archived or replacement source exists; or
- the evidence should be downgraded.

## Sources included

`scripts/check_source_health.py` builds a deduplicated URL inventory from:

- core incident primary/secondary sources and existing AIID cross-references;
- multilingual evidence source URLs;
- operational evidence primary/secondary sources and any AIID cross-references; and
- watchlist source URLs.

The resulting report records every URL together with the AAIO evidence layer and record IDs that depend on it.

## Status vocabulary

| Status | Meaning | Default maintenance response |
|---|---|---|
| `reachable` | HTTP 2xx/3xx after request handling | No action required. |
| `access_blocked` | 401, 403, 407, 429 or 451 | Review manually; do not treat as a dead source. |
| `not_found` | 404 or 410 | Search for an official replacement or lawful archive; inspect whether the evidence chain needs an update. |
| `client_error` | Other HTTP 4xx | Review request/URL and source behaviour manually. |
| `server_error` | HTTP 5xx | Re-check later before taking any data action. |
| `network_error` | Timeout, DNS, TLS or runner-network failure | Re-check later and compare from another network if needed. |
| `unexpected_status` | Status outside expected HTTP ranges | Manual review. |

## Request strategy

The audit first tries `HEAD` to minimize data transfer. If the site rejects or blocks `HEAD`, or the network request fails, the script can fall back to a small `GET` request. This reduces false dead-link signals from sites that do not implement `HEAD` normally.

The tool identifies itself with an AAIO user agent and does not attempt to bypass authentication, paywalls, anti-bot systems or access controls.

## Scheduled workflow

`.github/workflows/source-health.yml` runs a non-blocking source-health audit every week and can also be launched manually.

The workflow:

1. checks out the current repository;
2. runs the public URL audit;
3. places a concise status table in the GitHub Actions job summary; and
4. uploads the JSON and Markdown reports as temporary workflow artifacts.

The scheduled audit is deliberately **not a release gate**. External websites can fail independently of AAIO, so making transient network behaviour block data validation would reduce reproducibility rather than improve it.

## Local use

Build the source inventory without making any network requests:

```bash
python scripts/check_source_health.py --inventory-only
```

Run a live audit:

```bash
python scripts/check_source_health.py \
  --output /tmp/aaio-source-health.json \
  --markdown-output /tmp/aaio-source-health.md
```

For a small diagnostic sample:

```bash
python scripts/check_source_health.py --limit 10
```

## Responding to a flagged source

For a `not_found` or persistent error:

1. verify the URL manually;
2. search for the same primary document or report at the publisher's current canonical location;
3. prefer a replacement from the same authoritative source where possible;
4. if a lawful archive exists, record it as supporting resilience rather than pretending it is the original publisher;
5. if the evidence basis materially changes, update `last_verified`, append a record-history entry and explain the change in the changelog; and
6. never silently replace a source with a weaker article merely to make the link green.

## Copyright and archival discipline

AAIO links to evidence; it does not mirror full copyrighted articles or private material. Source resilience should rely on publisher URLs, public institutional archives, persistent identifiers and lawful web archives where appropriate.

## Research value

Monitoring source persistence adds a second dimension of provenance: not only *what source supported the record*, but also *whether that source remains practically reviewable over time*. This is especially important for multilingual fact-checks, court records and fast-changing public web content.
