# JobScout — Design Decisions

## 1. Why this ingestion strategy?

JobScout uses the public Himalayas Jobs API as its primary job source instead of scraping a protected job platform directly.

The API provides structured job data that can be consumed with a simple HTTP request. This reduces unnecessary browser automation and avoids depending on fragile page selectors. It also keeps the demo within the assignment's low-risk source requirement.

The ingestion process is implemented in `fetch_jobs.py`. It requests job data, extracts the required fields, and stores them in a local SQLite database (`jobs.db`). Duplicate records are prevented using a unique `source_id`.

For detection and responsible ingestion, the design avoids attempting to bypass authentication, CAPTCHA systems, or access controls. The application uses a public source and does not use a real user's account.

## 2. Trade-off and future improvement

Because of the available development time, JobScout currently uses a single public API source and stores the fetched listings in SQLite.

The main trade-off is that the system has limited source redundancy. If the primary API becomes unavailable or changes its response structure, new listings may not be ingested.

With a full development week, I would add a second compatible public source, stronger schema validation, scheduled ingestion, retry/backoff handling, source health monitoring, and a fallback strategy when the primary source becomes unavailable.

## 3. AI-assisted development

AI tools were used during development for brainstorming, debugging, code explanations, UI improvement ideas, and reviewing implementation approaches.

I personally verified the generated suggestions by running the application locally, testing the API ingestion, checking the SQLite database, reviewing the displayed job information, and making changes where necessary.

The final implementation was tested against the actual project environment rather than being accepted solely because an AI tool suggested it.