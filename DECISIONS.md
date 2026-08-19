# JobScout — Design Decisions

## 1. Detection Surface & Source Choice

JobScout uses the public Himalayas Jobs API as its primary job source rather than scraping a protected platform such as LinkedIn.

The main reason for this choice was to demonstrate the complete ingestion pipeline safely and reliably without attempting to bypass authentication, CAPTCHA, anti-bot controls, or a real user's account. This also follows the assignment's low-risk-source requirement.

For an automated client, common detection signals on a protected website can include headless-browser fingerprints, unusual request timing, missing or inconsistent browser headers, repeated requests from the same identity/IP, abnormal navigation patterns, and other behavioral signals. JobScout does not attempt to defeat these protections. Instead, it uses a documented/public API surface where structured job data can be requested directly.

If a protected source were considered in the future, my technical boundary would be to use only officially permitted/public interfaces and respect the source's robots.txt, terms, authentication requirements, and rate limits. I would stop rather than implement CAPTCHA bypass, credential reuse, stealth browser techniques, or other mechanisms intended to defeat access controls.

## 2. Ingestion Strategy

The ingestion flow is:

Himalayas Jobs API → Python requests → JSON response → field extraction → SQLite → Streamlit JobScout

The `fetch_jobs.py` script requests job listings from the API and extracts the fields required by the application, including job title, company, employment type, salary, description, and application URL.

Each listing is given a `source_id`. SQLite stores this value as a unique identifier, allowing duplicate API records to be ignored instead of creating repeated jobs.

The database layer is implemented in `database.py`, while `check_database.py` is used to verify that records were actually stored. During development, the pipeline was tested successfully and the database reached 60 stored listings.

The current implementation intentionally uses one low-risk public API instead of using a real LinkedIn account or attempting to scrape a protected site.

### Future fallback strategy

If the primary API becomes unavailable, changes its response structure, or starts rate-limiting requests, I would add:

- request timeouts and retry/backoff handling;
- response/schema validation before writing to SQLite;
- ingestion logging and source-health checks;
- scheduled ingestion instead of uncontrolled repeated requests;
- a second permitted public job source as a fallback;
- preservation of the last known-good SQLite data so the UI can continue serving previously ingested listings.

I would not respond to blocking by increasing request aggressiveness or bypassing anti-bot protections.

## 3. Resilience

JobScout separates ingestion from presentation.

The API-fetching process writes normalized job data into SQLite, while the Streamlit application reads the stored records for searching, filtering, sorting, and displaying jobs. This separation means the presentation layer does not need to make an external request for every user interaction.

Duplicate protection is handled through the unique `source_id`, preventing repeated ingestion of the same listing.

The application also handles missing job fields by providing safe fallback values for titles, companies, job types, salaries, descriptions, and application links. Job descriptions are cleaned before display so raw HTML, scripts, URLs, or code-like content from the source does not appear directly in the UI.

The current version is intentionally simple. With more development time, I would strengthen the ingestion layer with retries, exponential backoff, timeouts, schema validation, structured logs, source-health monitoring, and explicit handling for empty or malformed API responses.

## 4. Where I Stop

JobScout is designed around responsible ingestion rather than defeating a website's defenses.

I would use a source only when its public/API access is permitted and would respect published usage restrictions, rate limits, terms, and authentication boundaries.

I would stop the automated approach if the source required bypassing CAPTCHA, authentication, access controls, or other anti-bot mechanisms. If a source begins blocking requests, the preferred response is to reduce/stop requests, investigate the permitted access method, and switch to an allowed fallback source rather than attempting to evade the block.

This keeps the project focused on demonstrating an end-to-end ingestion system without putting a real user account or third-party platform at risk.

## 5. AI-Assisted Development & Personal Verification

AI tools were used during development as a development assistant for understanding APIs, debugging Python/SQLite issues, improving the Streamlit interface, reasoning about filtering/search behavior, explaining errors, and reviewing implementation approaches.

I did not treat AI output as automatically correct. I personally ran the project locally, tested API ingestion, verified the SQLite records, diagnosed a database schema mismatch, resolved Python/package environment issues, tested the Streamlit application, tested search and filtering behavior, checked job links, and verified the final deployed application.

I also changed and rejected generated code when it affected the existing UI or produced incorrect behavior. For example, the search/filter implementation was tested against actual stored listings, including Analyst-related jobs, and the final version was verified locally and again on the deployed Streamlit application.

The final implementation therefore represents AI-assisted development combined with manual testing, debugging, and verification rather than unverified generated code.