import streamlit as st
import sqlite3
import re
import html


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="JobScout",
    page_icon="💼",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #f7f9fc;
}

.block-container {
    max-width: 1150px;
    padding-top: 30px;
    padding-bottom: 60px;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* ================= NAVBAR ================= */

.navbar {
    background: white;
    padding: 18px 30px;
    margin-top: -30px;
    margin-left: -30px;
    margin-right: -30px;
    margin-bottom: 35px;

    border-bottom: 1px solid #e5e7eb;

    display: flex;
    justify-content: space-between;
    align-items: center;
}

.brand {
    font-size: 28px;
    font-weight: 800;
    color: #2563eb;
    letter-spacing: -1px;
}

.brand-dark {
    color: #111827;
}

.nav-right {
    color: #64748b;
    font-size: 14px;
    font-weight: 600;
}


/* ================= HERO ================= */

.hero {
    background: linear-gradient(
        135deg,
        #eaf2ff,
        #ffffff
    );

    border: 1px solid #dbeafe;

    border-radius: 24px;

    padding: 50px;

    margin-bottom: 25px;

    box-shadow: 0 8px 30px rgba(37, 99, 235, 0.06);
}

.hero-small {
    color: #2563eb;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.hero-title {
    color: #111827;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1.5px;
    margin-bottom: 12px;
}

.hero-description {
    color: #64748b;
    font-size: 16px;
    line-height: 1.6;
    max-width: 700px;
}


/* ================= SEARCH ================= */

div[data-baseweb="input"] {
    border-radius: 12px !important;
}


/* ================= SECTION ================= */

.section-title {
    color: #111827;
    font-size: 24px;
    font-weight: 800;
    margin-top: 25px;
}

.section-description {
    color: #64748b;
    font-size: 14px;
    margin-bottom: 15px;
}


/* ================= JOB CARD ================= */

.job-card {
    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 18px;

    padding: 25px;

    margin-top: 15px;

    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
}

.job-card:hover {
    border-color: #bfdbfe;
    box-shadow: 0 10px 30px rgba(37, 99, 235, 0.08);
}


/* ================= LOGO ================= */

.company-logo {
    width: 58px;
    height: 58px;

    border-radius: 14px;

    background: #eff6ff;

    border: 1px solid #dbeafe;

    display: flex;
    align-items: center;
    justify-content: center;

    color: #2563eb;

    font-size: 22px;
    font-weight: 800;
}


/* ================= JOB INFO ================= */

.job-title {
    color: #111827;

    font-size: 20px;

    font-weight: 750;

    margin-bottom: 5px;
}

.company-name {
    color: #64748b;

    font-size: 14px;

    font-weight: 600;
}


/* ================= TAGS ================= */

.tag {
    display: inline-block;

    background: #f1f5f9;

    color: #475569;

    padding: 6px 11px;

    border-radius: 8px;

    font-size: 12px;

    font-weight: 600;

    margin-right: 6px;
}

.salary-tag {
    background: #ecfdf5;

    color: #047857;
}


/* ================= DESCRIPTION ================= */

.description {
    color: #64748b;

    font-size: 14px;

    line-height: 1.65;

    margin-top: 16px;

    margin-bottom: 16px;
}


/* ================= BUTTON ================= */

.stLinkButton a {
    border-radius: 9px !important;

    font-weight: 650 !important;
}


/* ================= COUNT ================= */

.job-count {
    text-align: right;

    color: #64748b;

    font-size: 13px;

    padding-top: 10px;
}

.job-count strong {
    color: #111827;

    font-size: 20px;
}


/* ================= EMPTY ================= */

.empty-box {
    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 18px;

    padding: 50px;

    text-align: center;

    margin-top: 20px;
}

.empty-title {
    color: #111827;

    font-size: 20px;

    font-weight: 700;
}

.empty-text {
    color: #64748b;

    font-size: 14px;
}


/* ================= FOOTER ================= */

.footer {
    text-align: center;

    color: #94a3b8;

    font-size: 12px;

    margin-top: 55px;

    padding-top: 25px;

    border-top: 1px solid #e5e7eb;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CLEAN DESCRIPTION
# =========================================================

def clean_description(description):

    if not description:
        return "No description available."

    description = str(description)

    description = re.sub(
        r"<[^>]*>",
        " ",
        description
    )

    description = html.unescape(description)

    description = re.sub(
        r"\s+",
        " ",
        description
    )

    return description.strip()


# =========================================================
# GET COMPANY INITIAL
# =========================================================

def get_initial(company):

    if not company:
        return "C"

    company = str(company).strip()

    if not company:
        return "C"

    return company[0].upper()


# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect("jobs.db")

cursor = conn.cursor()

cursor.execute("""
SELECT
    title,
    company,
    job_type,
    salary,
    description,
    job_url
FROM jobs
""")

jobs = cursor.fetchall()

conn.close()


# =========================================================
# NAVBAR
# =========================================================

st.markdown("""
<div class="navbar">
<div class="brand">
Job<span class="brand-dark">Scout</span>
</div>
<div class="nav-right">
Smart Job Discovery
</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">
<div class="hero-small">
JOB DISCOVERY PLATFORM
</div>
<div class="hero-title">
Find your next opportunity.
</div>
<div class="hero-description">
Discover relevant job opportunities from trusted sources
and find opportunities that match your career goals.
</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SEARCH
# =========================================================

search = st.text_input(
    "Search",
    placeholder="🔍  Search by job title or company...",
    label_visibility="collapsed"
)


# =========================================================
# FILTER JOBS
# =========================================================

filtered_jobs = jobs

if search:

    query = search.lower().strip()

    filtered_jobs = []

    for job in jobs:

        title = str(job[0] or "").lower()
        company = str(job[1] or "").lower()

        if query in title or query in company:
            filtered_jobs.append(job)


# =========================================================
# SECTION HEADER
# =========================================================

col1, col2 = st.columns([4, 1])

with col1:

    st.markdown("""
<div class="section-title">
Recommended Jobs
</div>
<div class="section-description">
Explore the latest opportunities available in our database.
</div>
""", unsafe_allow_html=True)

with col2:

    st.markdown(
        f"""
<div class="job-count">
<strong>{len(filtered_jobs)}</strong><br>
opportunities
</div>
""",
        unsafe_allow_html=True
    )


# =========================================================
# JOB CARDS
# =========================================================

for job in filtered_jobs:

    title = job[0]
    company = job[1]
    job_type = job[2]
    salary = job[3]
    description = job[4]
    job_url = job[5]

    title = html.escape(
        str(title or "Untitled Position")
    )

    company = html.escape(
        str(company or "Company not listed")
    )

    job_type = html.escape(
        str(job_type or "Not specified")
    )

    salary = html.escape(
        str(salary or "Salary not disclosed")
    )

    description = clean_description(
        description
    )

    if len(description) > 280:

        description = (
            description[:280]
            + "..."
        )

    description = html.escape(
        description
    )

    initial = get_initial(company)


    # JOB CARD
    st.markdown(
        f"""
<div class="job-card">
<div style="display:flex;align-items:flex-start;gap:18px;">

<div class="company-logo">
{initial}
</div>

<div style="flex:1;">

<div class="job-title">
{title}
</div>

<div class="company-name">
{company}
</div>

</div>

</div>

<div style="margin-top:18px;">

<span class="tag">
💼 {job_type}
</span>

<span class="tag salary-tag">
💰 {salary}
</span>

</div>

<div class="description">
{description}
</div>

</div>
""",
        unsafe_allow_html=True
    )


    # VIEW JOB BUTTON
    if job_url:

        st.link_button(
            "View Job →",
            job_url
        )


# =========================================================
# NO RESULTS
# =========================================================

if len(filtered_jobs) == 0:

    st.markdown("""
<div class="empty-box">
<div class="empty-title">
No jobs found
</div>
<div class="empty-text">
Try searching with another job title or company.
</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
JobScout · AI & Technology Internship Assessment
</div>
""", unsafe_allow_html=True)