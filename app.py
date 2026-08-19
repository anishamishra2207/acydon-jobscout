import streamlit as st
import sqlite3
import re
import html

# ============================================================
# JOBSCOUT — polished Streamlit job discovery app
# ============================================================

st.set_page_config(
    page_title="JobScout | Find Your Next Opportunity",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- State --------------------

if "saved_jobs" not in st.session_state:
    st.session_state.saved_jobs = set()

# -------------------- CSS --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f7f8fc;
}

.block-container {
    max-width: 1240px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* Navigation */
.nav {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding: 14px 0 24px 0;
}

.logo {
    font-size: 25px;
    font-weight: 800;
    color:#1d4ed8;
    letter-spacing:-0.8px;
}

.logo span { color:#111827; }

.nav-pill {
    background:#eef2ff;
    color:#4338ca;
    border:1px solid #e0e7ff;
    padding:7px 13px;
    border-radius:999px;
    font-size:12px;
    font-weight:700;
}

/* Hero */
.hero {
    position:relative;
    overflow:hidden;
    border-radius:28px;
    padding:48px 50px;
    margin-bottom:24px;
    background:
        radial-gradient(circle at 82% 20%, rgba(129,140,248,.38), transparent 28%),
        radial-gradient(circle at 68% 85%, rgba(236,72,153,.20), transparent 28%),
        linear-gradient(120deg,#07142f 0%,#102a68 52%,#4520a5 100%);
    color:white;
    min-height:350px;
    box-shadow:0 18px 50px rgba(30,41,110,.18);
}

.hero:after {
    content:"";
    position:absolute;
    width:300px;
    height:300px;
    right:-80px;
    bottom:-120px;
    border-radius:50%;
    background:rgba(255,255,255,.08);
}

.hero-kicker {
    color:#a5b4fc;
    font-size:12px;
    font-weight:800;
    letter-spacing:1.5px;
    margin-bottom:12px;
}

.hero h1 {
    font-size:44px;
    line-height:1.08;
    letter-spacing:-2px;
    margin:0;
    max-width:650px;
}

.hero h1 span {
    color:#8b5cf6;
}

.hero p {
    color:#dbeafe;
    max-width:650px;
    line-height:1.7;
    margin-top:16px;
    font-size:15px;
}

.hero-art {
    position:absolute;
    right:45px;
    top:55px;
    width:330px;
    height:230px;
    border-radius:32px;
    background:linear-gradient(145deg,rgba(255,255,255,.14),rgba(255,255,255,.04));
    border:1px solid rgba(255,255,255,.16);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:115px;
    box-shadow:inset 0 1px rgba(255,255,255,.15);
}

@media(max-width:850px){
    .hero-art { display:none; }
    .hero { padding:35px 28px; }
    .hero h1 { font-size:34px; }
}

/* Search */
.search-box {
    background:white;
    border:1px solid #e5e7eb;
    border-radius:20px;
    padding:18px;
    margin-top:-48px;
    position:relative;
    z-index:5;
    box-shadow:0 12px 35px rgba(15,23,42,.10);
}

.search-title {
    font-size:15px;
    font-weight:800;
    color:#111827;
    margin-bottom:9px;
}

.popular {
    margin-top:9px;
    color:#64748b;
    font-size:12px;
}

.chip {
    display:inline-block;
    background:#f1f5f9;
    color:#334155;
    padding:5px 9px;
    border-radius:999px;
    margin-left:5px;
    font-size:11px;
    font-weight:600;
}

/* Stats */
.stat {
    background:#fff;
    border:1px solid #e5e7eb;
    border-radius:18px;
    padding:18px;
    box-shadow:0 5px 18px rgba(15,23,42,.035);
}

.stat-icon {
    width:40px;
    height:40px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:12px;
    font-size:19px;
    background:#eff6ff;
}

.stat-number {
    font-size:25px;
    font-weight:800;
    color:#0f172a;
    margin-top:10px;
}

.stat-label {
    color:#64748b;
    font-size:12px;
    margin-top:2px;
}

/* Sections */
.section-title {
    font-size:23px;
    font-weight:800;
    color:#0f172a;
    margin-top:30px;
}

.section-subtitle {
    color:#64748b;
    font-size:13px;
    margin-bottom:14px;
}

/* Job cards */
.job {
    background:white;
    border:1px solid #e5e7eb;
    border-radius:20px;
    padding:20px;
    margin-bottom:13px;
    box-shadow:0 5px 20px rgba(15,23,42,.035);
}

.job:hover {
    border-color:#c7d2fe;
}

.job-title {
    color:#111827;
    font-size:17px;
    font-weight:750;
    margin-bottom:3px;
}

.company {
    color:#475569;
    font-size:13px;
    font-weight:600;
}

.badge {
    display:inline-block;
    border-radius:999px;
    padding:5px 9px;
    margin-right:5px;
    margin-top:10px;
    font-size:11px;
    font-weight:700;
    background:#f1f5f9;
    color:#475569;
}

.badge-green {
    background:#ecfdf5;
    color:#047857;
}

.badge-purple {
    background:#f3e8ff;
    color:#7e22ce;
}

.badge-match {
    background:#eef2ff;
    color:#4338ca;
}

.salary {
    color:#059669;
    font-weight:800;
    font-size:14px;
}

.description {
    color:#64748b;
    font-size:13px;
    line-height:1.65;
    margin-top:13px;
}

/* Side panel */
.panel {
    background:white;
    border:1px solid #e5e7eb;
    border-radius:20px;
    padding:20px;
    margin-bottom:15px;
    box-shadow:0 5px 20px rgba(15,23,42,.035);
}

.panel-title {
    font-size:17px;
    font-weight:800;
    color:#111827;
}

.panel-text {
    color:#64748b;
    font-size:12px;
    line-height:1.6;
    margin-top:5px;
}

.smart {
    background:linear-gradient(135deg,#312e81,#7c3aed);
    color:white;
    border-radius:20px;
    padding:22px;
    margin-top:15px;
}

.smart h3 {
    margin:0;
    font-size:18px;
}

.smart p {
    color:#ede9fe;
    font-size:12px;
    line-height:1.6;
}

/* Footer */
.footer {
    margin-top:55px;
    padding:30px 0 5px;
    border-top:1px solid #e5e7eb;
    color:#94a3b8;
    text-align:center;
    font-size:12px;
}

div[data-testid="stLinkButton"] a {
    border-radius:10px !important;
    font-weight:700 !important;
}

.stButton button {
    border-radius:10px !important;
    font-weight:700 !important;
}

div[data-baseweb="input"] > div {
    border-radius:12px !important;
}
</style>
""", unsafe_allow_html=True)


# -------------------- Helpers --------------------

def clean_description(text):
    """Return readable job text, removing HTML/code/noisy API payloads."""
    if not text:
        return "No job description is available for this opportunity."

    text = html.unescape(str(text))

    # Remove scripts/styles and HTML tags
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove markdown/code fences
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)

    # Remove obvious JSON / code-like fragments
    text = re.sub(r'\{[^{}]{0,500}\}', ' ', text)
    text = re.sub(r'\[[^\[\]]{0,500}\]', ' ', text)
    text = re.sub(
        r'\b(import|from|def|class|return|SELECT|INSERT|UPDATE|DELETE|'
        r'CREATE TABLE|function|const|let|var)\b[^.!?]{0,180}',
        ' ',
        text,
        flags=re.I
    )

    # Remove URLs and excessive punctuation
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[{}<>]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) < 20:
        return "Explore this opportunity to view the complete job description."

    if len(text) > 330:
        text = text[:330].rsplit(" ", 1)[0] + "..."

    return text


def logo_url(company):
    """Use a clean company logo when the company is known."""
    c = str(company or "").lower()

    mapping = {
        "google": "https://cdn.simpleicons.org/google/4285F4",
        "microsoft": "https://cdn.simpleicons.org/microsoft/5E5CE6",
        "amazon": "https://cdn.simpleicons.org/amazon/FF9900",
        "meta": "https://cdn.simpleicons.org/meta/0866FF",
        "apple": "https://cdn.simpleicons.org/apple/111111",
        "ibm": "https://cdn.simpleicons.org/ibm/1261FE",
        "spotify": "https://cdn.simpleicons.org/spotify/1DB954",
        "netflix": "https://cdn.simpleicons.org/netflix/E50914",
        "tcs": "https://cdn.simpleicons.org/tcs/1478C8",
        "infosys": "https://cdn.simpleicons.org/infosys/007CC3",
        "wipro": "https://cdn.simpleicons.org/wipro/341C9B",
        "accenture": "https://cdn.simpleicons.org/accenture/A100FF",
        "deloitte": "https://cdn.simpleicons.org/deloitte/86BC25",
        "adobe": "https://cdn.simpleicons.org/adobe/FF0000",
        "salesforce": "https://cdn.simpleicons.org/salesforce/00A1E0",
    }

    for name, url in mapping.items():
        if name in c:
            return url

    return None


def match_score(job, keywords):
    if not keywords:
        return None

    words = [x.strip().lower() for x in keywords.split(",") if x.strip()]
    if not words:
        return None

    text = " ".join([
        str(job[1] or ""),
        str(job[2] or ""),
        str(job[5] or "")
    ]).lower()

    matched = sum(1 for w in words if w in text)
    return round((matched / len(words)) * 100)


# -------------------- Database --------------------

try:
    conn = sqlite3.connect("jobs.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT id, title, company, job_type, salary, description, job_url
        FROM jobs
    """)

    jobs = cur.fetchall()
    conn.close()

except Exception as e:
    st.error("Could not load the job database.")
    st.stop()


# -------------------- Navigation --------------------

st.markdown("""
<div class="nav">
    <div class="logo">🔎 Job<span>Scout</span></div>
    <div class="nav-pill">SMART JOB DISCOVERY</div>
</div>
""", unsafe_allow_html=True)


# -------------------- Hero --------------------

st.markdown("""
<section class="hero">
    <div class="hero-kicker">CAREER DISCOVERY PLATFORM</div>
    <h1>Find Opportunities<br>That <span>Match Your Future.</span></h1>
    <p>
        Discover relevant job opportunities, compare roles and
        find your next career move through one simple platform.
    </p>
    <div class="hero-art">💼</div>
</section>
""", unsafe_allow_html=True)


# -------------------- Search --------------------

st.markdown('<div class="search-box">', unsafe_allow_html=True)

st.markdown(
    '<div class="search-title">🔎 Find your next opportunity</div>',
    unsafe_allow_html=True
)

search = st.text_input(
    "Search",
    placeholder="Search by job title, company or keyword...",
    label_visibility="collapsed",
    key="search_query"
)

st.markdown("""
<div class="popular">
Popular:
<span class="chip">Python</span>
<span class="chip">Data Science</span>
<span class="chip">Machine Learning</span>
<span class="chip">Developer</span>
<span class="chip">SQL</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.write("")


# -------------------- Stats --------------------

companies = {
    str(j[2]).strip() for j in jobs if j[2]
}

types = {
    str(j[3]).strip() for j in jobs if j[3]
}

c1, c2, c3, c4 = st.columns(4)

stats = [
    (c1, "💼", len(jobs), "Jobs Available"),
    (c2, "🏢", len(companies), "Companies"),
    (c3, "🧩", len(types), "Job Types"),
    (c4, "♥", len(st.session_state.saved_jobs), "Saved Jobs"),
]

for col, icon, number, label in stats:
    with col:
        st.markdown(
            f"""
            <div class="stat">
                <div class="stat-icon">{icon}</div>
                <div class="stat-number">{number}</div>
                <div class="stat-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# -------------------- Filters --------------------

# -------------------- Filters --------------------

st.markdown(
    '<div class="section-title">Featured Opportunities</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">Explore roles and use filters to narrow your search.</div>',
    unsafe_allow_html=True
)

left, right = st.columns([2.7, 1])

with right:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown(
        '<div class="panel-title">🎯 Refine your search</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="panel-text">Choose a job type, company or ranking method.</div>',
        unsafe_allow_html=True
    )

    type_options = ["All Types"] + sorted(
        {str(j[3]).strip() for j in jobs if j[3]}
    )

    company_options = ["All Companies"] + sorted(
        {str(j[2]).strip() for j in jobs if j[2]}
    )

    selected_type = st.selectbox(
        "Job Type",
        type_options,
        key="job_type_filter"
    )

    selected_company = st.selectbox(
        "Company",
        company_options,
        key="company_filter"
    )

    sort_by = st.selectbox(
        "Sort By",
        [
            "Newest",
            "Job Title A-Z",
            "Job Title Z-A",
            "Company A-Z",
            "Company Z-A"
        ],
        key="sort_filter"
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------- Smart Match --------------------

    st.markdown("""
    <div class="smart">
        <h3>✨ Smart Match</h3>
        <p>
            Enter your skills and JobScout will rank opportunities
            by keyword relevance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    smart_keywords = st.text_input(
        "Skills",
        placeholder="Python, SQL, ML",
        label_visibility="collapsed",
        key="smart_keywords"
    )

    # Reset button
    if st.button(
        "↺ Reset All Filters",
        use_container_width=True,
        key="reset_filters"
    ):
        st.session_state.search_query = ""
        st.session_state.job_type_filter = "All Types"
        st.session_state.company_filter = "All Companies"
        st.session_state.sort_filter = "Newest"
        st.session_state.smart_keywords = ""
        st.rerun()


# ============================================================
# FILTERING
# ============================================================

filtered = []

search_text = str(search or "").strip().lower()

# Convert search into useful words.
# Example:
# "data analyst" -> ["data", "analyst"]
search_words = [
    word for word in re.findall(r"[a-zA-Z0-9+#.-]+", search_text)
    if len(word) > 1
]

for job in jobs:

    job_id = job[0]

    title = str(job[1] or "").strip()
    company = str(job[2] or "").strip()
    job_type = str(job[3] or "").strip()
    salary = str(job[4] or "").strip()
    description = str(job[5] or "").strip()
    job_url = str(job[6] or "").strip()

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    searchable_text = " ".join([
        title,
        company,
        job_type,
        salary,
        description
    ]).lower()

    # Every search word must exist somewhere in the job.
    # This makes:
    # analyst       -> analyst jobs
    # data analyst  -> jobs containing both words
    if search_words:
        if not all(word in searchable_text for word in search_words):
            continue

    # --------------------------------------------------------
    # Job Type
    # --------------------------------------------------------

    if selected_type != "All Types":

        if job_type.lower() != selected_type.lower():
            continue

    # --------------------------------------------------------
    # Company
    # --------------------------------------------------------

    if selected_company != "All Companies":

        if company.lower() != selected_company.lower():
            continue

    # Passed every filter
    filtered.append(job)


# ============================================================
# SORTING
# ============================================================

if sort_by == "Job Title A-Z":

    filtered.sort(
        key=lambda x: str(x[1] or "").lower()
    )

elif sort_by == "Job Title Z-A":

    filtered.sort(
        key=lambda x: str(x[1] or "").lower(),
        reverse=True
    )

elif sort_by == "Company A-Z":

    filtered.sort(
        key=lambda x: str(x[2] or "").lower()
    )

elif sort_by == "Company Z-A":

    filtered.sort(
        key=lambda x: str(x[2] or "").lower(),
        reverse=True
    )

else:
    # Newest/default = database order
    # No artificial sorting needed.
    pass


# ============================================================
# SMART MATCH
# ============================================================

smart_text = str(smart_keywords or "").strip()

if smart_text:

    # Smart Match should rank the ALREADY FILTERED jobs.
    # It should NOT remove jobs selected by the normal filters.

    filtered.sort(
        key=lambda x: match_score(x, smart_text) or 0,
        reverse=True
    )


# ============================================================
# RESULT SUMMARY
# ============================================================

with left:

    if smart_text:

        st.info(
            "✨ Smart Match is ranking the filtered opportunities "
            "according to your selected skills."
        )

    # Result information

    if search_text:

        st.markdown(
            f"""
            <div style="
                background:#eef2ff;
                border:1px solid #e0e7ff;
                padding:10px 14px;
                border-radius:10px;
                margin-bottom:15px;
                color:#3730a3;
                font-size:13px;
                font-weight:600;
            ">
                🔎 Showing {len(filtered)} result(s) for
                <strong>{html.escape(search)}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

    if not filtered:

        st.warning(
            "No matching opportunities found. "
            "Try another keyword or reset the filters."
        )

    # ========================================================
    # JOB CARDS
    # ========================================================

    for job in filtered:

        job_id, title, company, job_type, salary, raw_description, job_url = job

        title = str(title or "Untitled Role")
        company = str(company or "Company not listed")
        job_type = str(job_type or "Not specified")
        salary = str(salary or "")
        job_url = str(job_url or "").strip()

        # Clean API HTML before displaying it
        description = clean_description(raw_description)

        # Smart Match score
        score = match_score(job, smart_text)

        # Company logo
        logo = logo_url(company)

        # ----------------------------------------------------
        # Card
        # ----------------------------------------------------

        st.markdown(
            '<div class="job">',
            unsafe_allow_html=True
        )

        top1, top2, top3 = st.columns(
            [0.55, 3.5, 1.4]
        )

        # Logo
        with top1:

            if logo:

                st.image(
                    logo,
                    width=48
                )

            else:

                st.markdown("### 🏢")

        # Title + company
        with top2:

            st.markdown(
                f"""
                <div class="job-title">
                    {html.escape(title)}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="company">
                    {html.escape(company)}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Salary
        with top3:

            if salary:

                st.markdown(
                    f"""
                    <div class="salary">
                        {html.escape(salary)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ----------------------------------------------------
        # Badges
        # ----------------------------------------------------

        jt = html.escape(job_type)

        st.markdown(
            f"""
            <span class="badge badge-green">
                💼 {jt}
            </span>

            <span class="badge">
                📌 Open Position
            </span>
            """,
            unsafe_allow_html=True
        )

        if smart_text:

            st.markdown(
                f"""
                <span class="badge badge-match">
                    ✨ {score or 0}% Skill Match
                </span>
                """,
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        # IMPORTANT:
        # escape() prevents API HTML from appearing as code.
        # clean_description() removes the unwanted HTML first.

        st.markdown(
            f"""
            <div class="description">
                {html.escape(description)}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        a, b = st.columns([1, 2.2])

        # Save
        with a:

            if job_id in st.session_state.saved_jobs:

                if st.button(
                    "♥ Saved",
                    key=f"save_{job_id}",
                    use_container_width=True
                ):

                    st.session_state.saved_jobs.remove(job_id)
                    st.rerun()

            else:

                if st.button(
                    "♡ Save",
                    key=f"save_{job_id}",
                    use_container_width=True
                ):

                    st.session_state.saved_jobs.add(job_id)
                    st.rerun()

        # Open actual job
        with b:

            if job_url and job_url.startswith(("http://", "https://")):

                st.link_button(
                    "View Full Opportunity →",
                    job_url,
                    use_container_width=True
                )

            else:

                st.button(
                    "Opportunity link unavailable",
                    key=f"no_link_{job_id}",
                    disabled=True,
                    use_container_width=True
                )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    <strong style="color:#475569;">🔎 JobScout</strong>
    · Find opportunities that match your future.
    <br><br>
    Built with Python · Streamlit · REST API · SQLite
</div>
""", unsafe_allow_html=True)