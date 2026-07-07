import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import textwrap
import datetime

# 1. Must call set_page_config as the first Streamlit command
st.set_page_config(
    page_title="AI Recruitment & Talent Copilot",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Safe rerun function to support different Streamlit versions
def safe_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# Helper to load data safely
def load_csv_data(filepath):
    try:
        if os.path.exists(filepath):
            return pd.read_csv(filepath)
        else:
            st.error(f"Critical Error: Data file '{filepath}' is missing from the disk.")
            return None
    except Exception as e:
        st.error(f"Error reading '{filepath}': {e}")
        return None

# Load raw dataset once
candidates_df_raw = load_csv_data("data/candidates.csv")
requirements_df_raw = load_csv_data("data/job_requirements.csv")

# Initialize session state databases for CRUD operations if not already set
if "jobs_db" not in st.session_state and requirements_df_raw is not None:
    st.session_state["jobs_db"] = requirements_df_raw.to_dict(orient="records")

if "candidates_db" not in st.session_state and candidates_df_raw is not None:
    st.session_state["candidates_db"] = candidates_df_raw.to_dict(orient="records")

# Ensure shortlist is in session state
if "shortlist" not in st.session_state:
    st.session_state["shortlist"] = []

# Mock data initializations if not in state
if "interviews" not in st.session_state:
    st.session_state["interviews"] = [
        {"Name": "Arun", "Role": "Software Engineer", "Date": "2026-07-10", "Time": "10:00 AM", "Mode": "Zoom Meeting", "Status": "Scheduled"},
        {"Name": "Priya", "Role": "Data Scientist", "Date": "2026-07-11", "Time": "02:00 PM", "Mode": "Microsoft Teams", "Status": "Scheduled"},
        {"Name": "Rohan", "Role": "Product Manager", "Date": "2026-07-12", "Time": "11:30 AM", "Mode": "Zoom Meeting", "Status": "Completed"}
    ]
    
if "notifications" not in st.session_state:
    st.session_state["notifications"] = [
        {"Message": "Arun has been shortlisted for Software Engineer", "Time": "2 hours ago", "Read": False},
        {"Message": "Priya has been shortlisted for Data Scientist", "Time": "4 hours ago", "Read": False},
        {"Message": "Rohan finished the Product Manager interview", "Time": "Yesterday", "Read": True}
    ]

if "employee_db" not in st.session_state:
    st.session_state["employee_db"] = [
        {"Name": "Vijay Kumar", "Role": "Senior Software Engineer", "Department": "Engineering", "Tenure": "3 Years", "Performance": "Exceeds Expectations"},
        {"Name": "Sneha Sharma", "Role": "Data Scientist", "Department": "Analytics", "Tenure": "1.5 Years", "Performance": "Meets Expectations"},
        {"Name": "Ramesh Patel", "Role": "Lead UX Designer", "Department": "Design", "Tenure": "4 Years", "Performance": "Outstanding"},
        {"Name": "Anjali Sen", "Role": "HR Specialist", "Department": "Human Resources", "Tenure": "2 Years", "Performance": "Meets Expectations"}
    ]
    
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "content": "Hello! I am your AI Talent Assistant. Ask me questions about candidates, matching criteria, or recruitment metrics."}
    ]
    
if "settings_weights" not in st.session_state:
    st.session_state["settings_weights"] = {
        "Technical Fit": 40,
        "Experience Fit": 30,
        "Communication": 15,
        "Culture Fit": 15
    }

if "candidate_notes" not in st.session_state:
    st.session_state["candidate_notes"] = {}

# Convert session states back to dataframes so application works seamlessly
if "jobs_db" in st.session_state and len(st.session_state["jobs_db"]) > 0:
    requirements_df = pd.DataFrame(st.session_state["jobs_db"])
else:
    requirements_df = requirements_df_raw

if "candidates_db" in st.session_state and len(st.session_state["candidates_db"]) > 0:
    candidates_df = pd.DataFrame(st.session_state["candidates_db"])
else:
    candidates_df = candidates_df_raw

# 7. Apply a custom theme via st.markdown
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* Main font application */
html, body, [class*="css"], .stMarkdown {
    font-family: 'Inter', 'Sora', sans-serif;
}

/* Custom header with gradient */
.header-container {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    padding: 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    border: 1px solid #2d3748;
    color: #f8fafc;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
}

.header-title {
    font-family: 'Sora', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(to right, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.header-subtitle {
    font-size: 1.1rem;
    opacity: 0.8;
    margin-top: 0.5rem;
    color: #cbd5e1;
}

/* Styled Card container for candidate details */
.candidate-card {
    background-color: #1e293b;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid #334155;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.candidate-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
    border-color: #475569;
}

.score-badge {
    background-color: #0f172a;
    border: 1px solid #3b82f6;
    color: #60a5fa;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9rem;
    display: inline-block;
}

.shortlisted-badge {
    background-color: #064e3b;
    border: 1px solid #059669;
    color: #34d399;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9rem;
    display: inline-block;
}

.explainability-card {
    background-color: #1e293b;
    border-left: 5px solid #3b82f6;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    border-top: 1px solid #334155;
    border-right: 1px solid #334155;
    border-bottom: 1px solid #334155;
}

.explainability-header {
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 1.3rem;
    color: #f8fafc;
    margin-bottom: 0.8rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.audit-metric-card {
    background-color: #1e293b;
    border: 1px solid #334155;
    padding: 1.2rem;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.audit-number {
    font-family: 'Sora', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #60a5fa;
}

.audit-label {
    font-size: 0.9rem;
    color: #94a3b8;
    margin-top: 0.3rem;
}

/* Chat bubble styling */
.chat-bubble-user {
    background-color: #1e3a8a;
    color: #f8fafc;
    padding: 0.8rem 1.2rem;
    border-radius: 16px 16px 4px 16px;
    margin-bottom: 0.8rem;
    max-width: 80%;
    margin-left: auto;
    text-align: right;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border: 1px solid #3b82f6;
}

.chat-bubble-assistant {
    background-color: #1e293b;
    color: #cbd5e1;
    padding: 0.8rem 1.2rem;
    border-radius: 16px 16px 16px 4px;
    margin-bottom: 0.8rem;
    max-width: 80%;
    margin-right: auto;
    text-align: left;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border: 1px solid #334155;
}

/* Calendar Card styling */
.calendar-card {
    background-color: #1e293b;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 0.8rem;
    border-top: 1px solid #334155;
    border-right: 1px solid #334155;
    border-bottom: 1px solid #334155;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

/* Timeline/Experience Tracker */
.timeline-item {
    border-left: 2px solid #3b82f6;
    padding-left: 1.2rem;
    margin-left: 0.6rem;
    padding-bottom: 1.2rem;
    position: relative;
}

.timeline-marker {
    width: 12px;
    height: 12px;
    background-color: #60a5fa;
    border-radius: 50%;
    position: absolute;
    left: -7px;
    top: 4px;
    border: 2px solid #0f172a;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Main Dashboard Layout
# Title Bar containing Logo & Main Heading
col_logo, col_title = st.columns([1, 8])

with col_logo:
    # 5. Safe Logo Loading
    if os.path.exists("assets/company_logo.png"):
        st.image("assets/company_logo.png", width=110)
    else:
        st.write("[Logo Placeholder]")

with col_title:
    st.markdown(
        textwrap.dedent("""
            <div class="header-container">
                <h1 class="header-title">AI Recruitment & Talent Copilot</h1>
                <p class="header-subtitle">Advanced HR decision-making with explainable matching and fairness auditing</p>
            </div>
        """),
        unsafe_allow_html=True
    )

# Check if data successfully loaded before continuing
if candidates_df is not None and requirements_df is not None:
    
    # 1. Global Navigation in Sidebar
    st.sidebar.markdown("### Navigation Module")
    navigation_option = st.sidebar.selectbox(
        "Select Workspace",
        [
            "Candidate Assessment Suite",
            "Pipeline Dashboard",
            "Job Role Management (CRUD)",
            "Candidate Profile Browser",
            "Interview Scheduler & Calendar",
            "Notifications Center",
            "Advanced HR Analytics",
            "Employee Directory",
            "AI Chatbot Assistant",
            "System Settings"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Target Job Role")
    roles = requirements_df["Role"].tolist()
    
    # Get index of selected role or fallback to 0
    selected_role = st.sidebar.selectbox("Select Target Position", roles)
    
    # Extract role requirements
    role_req = requirements_df[requirements_df["Role"] == selected_role].iloc[0]
    required_skills = [s.strip() for s in role_req["Required_Skills"].split(",")]
    min_experience = int(role_req["Min_Experience"])
    
    # 2. Render Conditional Sidebar Filters ONLY for Assessment Suite
    if navigation_option == "Candidate Assessment Suite":
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Filter Candidate Pool")
        
        # Get unique list of all skills across candidates for filtering
        all_skills = set()
        for s_list in candidates_df["Skills"].dropna():
            for skill in s_list.split(","):
                all_skills.add(skill.strip())
                
        filtered_skills = st.sidebar.multiselect(
            "Filter by skills (Union)", 
            options=sorted(list(all_skills)),
            help="Display candidates who possess any of these selected skills."
        )
        
        st.sidebar.markdown("---")
        # Quick reset shortlist button
        st.sidebar.markdown("### Shortlist Control")
        if st.sidebar.button("Clear Candidate Shortlist", use_container_width=True):
            st.session_state["shortlist"] = []
            st.sidebar.success("Shortlist cleared!")
            safe_rerun()
            
        st.sidebar.info(f"Currently Shortlisted: **{len(st.session_state['shortlist'])}** candidate(s)")
    else:
        filtered_skills = []

    # Calculate Dynamic Match Score & Prepare DataFrame
    candidates_df_calc = candidates_df.copy()
    
    # Perform Dynamic Overlap Keyword Match Calculation
    def calculate_score(candidate_skills_str, req_skills_list):
        if not candidate_skills_str:
            return 0
        c_skills = [s.strip().lower() for s in candidate_skills_str.split(",")]
        r_skills = [s.lower() for s in req_skills_list]
        
        matches = [s for s in c_skills if s in r_skills]
        if not r_skills:
            return 100
        return int((len(matches) / len(r_skills)) * 100)
    
    # Calculate scores with configured settings weights if available
    weights = st.session_state.get("settings_weights", {"Technical Fit": 40, "Experience Fit": 30, "Communication": 15, "Culture Fit": 15})
    
    candidates_df_calc["Match_Score"] = candidates_df_calc["Skills"].apply(
        lambda x: calculate_score(x, required_skills)
    )
    
    # Sort candidates by match score
    candidates_df_calc = candidates_df_calc.sort_values(by="Match_Score", ascending=False)
    
    # Filter candidates based on Role Applied and Skill selection
    display_candidates = candidates_df_calc[candidates_df_calc["Role Applied"] == selected_role]
    
    if filtered_skills:
        # Keep candidates who have at least one of the filtered skills
        def matches_skills(skills_str):
            c_skills = [s.strip().lower() for s in skills_str.split(",")]
            f_skills = [s.lower() for s in filtered_skills]
            return any(s in c_skills for s in f_skills)
            
        display_candidates = display_candidates[display_candidates["Skills"].apply(matches_skills)]

    # ------------------ MODULE 1: ASSESSMENT SUITE (ORIGINAL 3 TABS) ------------------
    if navigation_option == "Candidate Assessment Suite":
        
        tab_pool, tab_explain, tab_bias = st.tabs([
            "Candidate Pool", 
            "Comparison & Explainability", 
            "Bias & Fairness Audit"
        ])
        
        # ------------------ TAB 1: CANDIDATE POOL ------------------
        with tab_pool:
            st.markdown(f"### Current Pool for **{selected_role}**")
            
            # Display Job details
            st.markdown(
                f"""
                <div style="background-color: rgba(30, 41, 59, 0.4); padding: 1rem; border-radius: 8px; border: 1px solid #334155; margin-bottom: 1.5rem;">
                    <strong>Position Requirements:</strong> Required Skills: <code>{', '.join(required_skills)}</code> | Minimum Experience: <code>{min_experience} Years</code>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Display tabular view
            st.markdown("#### Overview Table")
            st.dataframe(
                display_candidates[["Name", "Skills", "Experience_Years", "Match_Score"]], 
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("#### Candidate Profile Action Grid")
            if display_candidates.empty:
                st.info("No candidates match your criteria. Try adjusting the sidebar filters.")
            else:
                # Custom styled list view with shortlist button action
                for idx, row in display_candidates.iterrows():
                    name = row["Name"]
                    skills = row["Skills"]
                    experience = row["Experience_Years"]
                    score = row["Match_Score"]
                    
                    is_shortlisted = name in st.session_state["shortlist"]
                    
                    # Construct HTML dynamically without newlines/indentation to avoid markdown parser code-block trigger
                    badge_html = f'<span class="shortlisted-badge" style="margin-left: 0.5rem;">Shortlisted</span>' if is_shortlisted else ''
                    card_html = (
                        f'<div class="candidate-card">'
                        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">'
                        f'<span style="font-size: 1.2rem; font-weight: 600; color: #f8fafc;">{name}</span>'
                        f'<div><span class="score-badge">Match: {score}%</span>{badge_html}</div>'
                        f'</div>'
                        f'<div style="margin-bottom: 0.5rem;"><span style="color: #94a3b8; font-size: 0.9rem;">Skills:</span> '
                        f'<span style="color: #cbd5e1; font-size: 0.9rem;">{skills}</span></div>'
                        f'<div style="display: flex; justify-content: space-between; align-items: center;">'
                        f'<span style="color: #94a3b8; font-size: 0.9rem;">Experience: <strong>{experience} years</strong> (Req: {min_experience})</span>'
                        f'</div>'
                        f'</div>'
                    )
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    # Render shortlisting button under each card safely with unique key
                    col_btn_dummy, col_btn = st.columns([5, 1])
                    with col_btn:
                        if is_shortlisted:
                            if st.button("Remove", key=f"remove_{name}_{idx}", use_container_width=True, type="secondary"):
                                st.session_state["shortlist"].remove(name)
                                
                                # Add notification
                                st.session_state["notifications"].insert(0, {
                                    "Message": f"{name} removed from the {selected_role} shortlist.",
                                    "Time": "Just now",
                                    "Read": False
                                })
                                safe_rerun()
                        else:
                            if st.button("Shortlist", key=f"shortlist_{name}_{idx}", use_container_width=True, type="primary"):
                                st.session_state["shortlist"].append(name)
                                
                                # Add notification
                                st.session_state["notifications"].insert(0, {
                                    "Message": f"{name} added to the {selected_role} shortlist.",
                                    "Time": "Just now",
                                    "Read": False
                                })
                                safe_rerun()
                    st.write("") # small spacing
                    
        # ------------------ TAB 2: COMPARISON & EXPLAINABILITY ------------------
        with tab_explain:
            st.markdown("### Candidate Comparison Radar & Explainability Ledger")
            
            # Select candidates to compare from shortlist
            shortlisted_names = list(set(st.session_state["shortlist"]))
            
            st.markdown("Select candidates from your shortlist to analyze side-by-side:")
            selected_candidates = st.multiselect(
                "Select Candidates",
                options=shortlisted_names,
                default=shortlisted_names
            )
            
            if len(selected_candidates) < 2:
                st.info("Please shortlist and select at least 2 candidates in the multiselect above to generate the radar comparison and explainability ledger.")
            else:
                # 1. Plotly radar chart logic
                radar_data = []
                
                # Prepare dimensions for radar comparison
                categories = ["Technical Fit", "Communication", "Experience Fit", "Culture Fit"]
                
                for name in selected_candidates:
                    candidate_data = candidates_df_calc[candidates_df_calc["Name"] == name].iloc[0]
                    c_skills = [s.strip().lower() for s in candidate_data["Skills"].split(",")]
                    
                    # 1. Technical Fit score (keyword match ratio)
                    tech_score = calculate_score(candidate_data["Skills"], required_skills)
                    
                    # 2. Communication score (rule-based)
                    comm_keywords = ["communication", "leadership", "presentation", "writing", "english"]
                    has_comm_skill = any(k in c_skills for k in comm_keywords)
                    comm_score = 90 if has_comm_skill else (80 if candidate_data["Experience_Years"] >= 5 else 68)
                    
                    # 3. Experience Fit score
                    exp_ratio = float(candidate_data["Experience_Years"]) / max(1, min_experience)
                    exp_score = min(100, int(exp_ratio * 100))
                    
                    # 4. Culture Fit score
                    culture_keywords = ["agile", "git", "scrum", "collaboration", "teamwork", "docker"]
                    culture_matches = len([k for k in culture_keywords if k in c_skills])
                    culture_score = min(100, 70 + (culture_matches * 5))
                    
                    # Plotly trace
                    radar_data.append(go.Scatterpolar(
                        r=[tech_score, comm_score, exp_score, culture_score],
                        theta=categories,
                        fill='toself',
                        name=name
                    ))
                
                # Layout configuration
                layout = go.Layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=True,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#f8fafc", family="Inter"),
                    margin=dict(t=30, b=30, l=30, r=30),
                    height=450
                )
                
                fig = go.Figure(data=radar_data, layout=layout)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 2. Explainability Ledger
                st.markdown("---")
                st.markdown("### Explainability Ledger")
                st.write("Plain-language reasoning trail showing exactly how and why each candidate achieved their score:")
                
                for name in selected_candidates:
                    candidate_data = candidates_df_calc[candidates_df_calc["Name"] == name].iloc[0]
                    c_skills = [s.strip() for s in candidate_data["Skills"].split(",")]
                    
                    # Identify matched and missing required skills
                    c_skills_lower = [s.lower() for s in c_skills]
                    matched = [s for s in required_skills if s.lower() in c_skills_lower]
                    missing = [s for s in required_skills if s.lower() not in c_skills_lower]
                    
                    # Compute score factors
                    tech_score = calculate_score(candidate_data["Skills"], required_skills)
                    c_exp = int(candidate_data["Experience_Years"])
                    
                    # Construct HTML dynamically without newlines/indentation to avoid markdown parser code-block trigger
                    matched_str = ', '.join(matched) if matched else 'None'
                    missing_str = ', '.join(missing) if missing else 'None'
                    
                    exp_analysis = (
                        f"This exceeds the minimum requirement of <strong>{min_experience} years</strong> by {c_exp - min_experience} year(s)."
                        if c_exp >= min_experience else
                        f"This is short of the minimum requirement of <strong>{min_experience} years</strong> by {min_experience - c_exp} year(s)."
                    )
                    
                    derivation_logic = (
                        f"A further experience buffer of {c_exp} years validates competency level."
                        if c_exp >= min_experience else
                        "Experience shortfall is flagged, which may affect practical execution."
                    )
                    
                    explain_html = (
                        f'<div class="explainability-card">'
                        f'<div class="explainability-header">'
                        f'<span>Candidate: <strong>{name}</strong></span>'
                        f'<span class="score-badge">Final Match Score: {tech_score}%</span>'
                        f'</div>'
                        f'<ul style="color: #cbd5e1; margin-bottom: 0; padding-left: 1.2rem;">'
                        f'<li><strong>Matched Required Skills:</strong> <span style="color: #34d399; font-weight: 500;">{matched_str}</span></li>'
                        f'<li><strong>Missing Required Skills:</strong> <span style="color: #f87171; font-weight: 500;">{missing_str}</span></li>'
                        f'<li><strong>Experience Analysis:</strong> Candidate has <strong>{c_exp} years</strong> of experience. {exp_analysis}</li>'
                        f'<li><strong>Score Derivation Logic:</strong> Technical keyword matching matched <strong>{len(matched)} of {len(required_skills)}</strong> required skills ({tech_score}% weight). {derivation_logic}</li>'
                        f'</ul>'
                        f'</div>'
                    )
                    st.markdown(explain_html, unsafe_allow_html=True)
                    
        # ------------------ TAB 3: BIAS & FAIRNESS AUDIT ------------------
        with tab_bias:
            st.markdown("### Bias & Fairness Audit Panel")
            st.markdown("This panel monitors candidate shortlisting choices for experience-based concentration, helping ensure a diverse pipeline.")
            
            shortlisted_candidates = candidates_df_calc[candidates_df_calc["Name"].isin(st.session_state["shortlist"])]
            
            # Display Overview Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    f'<div class="audit-metric-card">'
                    f'<div class="audit-number">{len(st.session_state["shortlist"])}</div>'
                    f'<div class="audit-label">Total Shortlisted Candidates</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            with col2:
                st.markdown(
                    f'<div class="audit-metric-card">'
                    f'<div class="audit-number">{len(display_candidates)}</div>'
                    f'<div class="audit-label">Available Applicant Pool</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
            with col3:
                conversion_rate = round((len(st.session_state["shortlist"]) / max(1, len(display_candidates))) * 100, 1)
                st.markdown(
                    f'<div class="audit-metric-card">'
                    f'<div class="audit-number">{conversion_rate}%</div>'
                    f'<div class="audit-label">Shortlist Conversion Ratio</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
            st.markdown("---")
            st.markdown("#### Experience Band Distribution Analysis")
            
            if shortlisted_candidates.empty:
                st.info("Please shortlist some candidates from the **Candidate Pool** tab to view the live fairness analysis.")
            else:
                # Group into experience bands
                def categorize_exp(exp):
                    if exp <= 2:
                        return "Entry (0-2 Years)"
                    elif exp <= 5:
                        return "Mid-Level (3-5 Years)"
                    else:
                        return "Senior (6+ Years)"
                        
                shortlisted_candidates = shortlisted_candidates.copy()
                shortlisted_candidates["Experience_Band"] = shortlisted_candidates["Experience_Years"].apply(categorize_exp)
                
                # Count sizes
                counts = shortlisted_candidates["Experience_Band"].value_counts()
                total_shortlisted = len(shortlisted_candidates)
                
                # Render distributions
                bands = ["Entry (0-2 Years)", "Mid-Level (3-5 Years)", "Senior (6+ Years)"]
                
                col_bar1, col_bar2 = st.columns([1, 1])
                
                with col_bar1:
                    st.markdown("##### Current Shortlist Spread")
                    for band in bands:
                        count = counts.get(band, 0)
                        pct = (count / total_shortlisted) * 100
                        st.write(f"**{band}**: {count} candidate(s) ({pct:.1f}%)")
                        st.progress(int(pct))
                
                with col_bar2:
                    # Audit Flag Logic
                    skewed_band = None
                    skew_pct = 0.0
                    
                    for band in bands:
                        count = counts.get(band, 0)
                        pct = (count / total_shortlisted) * 100
                        if pct > 70.0:
                            skewed_band = band
                            skew_pct = pct
                            break
                    
                    if skewed_band:
                        st.warning(
                            textwrap.dedent(f"""
                                **Potential Shortlist Skew Detected!**
                                
                                The experience band **{skewed_band}** represents **{skew_pct:.1f}%** of your shortlist, which exceeds the recommended 70% threshold.
                                
                                **Ethical AI Recommendation:**
                                A highly concentrated shortlist might introduce age or tier-based bias. To ensure cognitive diversity and team growth potential, we recommend reviewing candidates in other experience brackets before submitting the final hiring recommendation.
                            """)
                        )
                    else:
                        st.success(
                            textwrap.dedent(f"""
                                **Shortlist Diversity Check Passed**
                                
                                No single experience band exceeds the 70% concentration limit. The shortlist represents a healthy, balanced spread of experience levels.
                            """)
                        )
                        
            st.markdown("")
            st.caption("**Fairness Auditor Note:** This tool evaluates simple statistical distribution skews on selected parameters. It is a rule-based heuristic check intended for decision support, not an automated legal fairness/ML audit.")

    # ------------------ MODULE 2: PIPELINE DASHBOARD ------------------
    elif navigation_option == "Pipeline Dashboard":
        st.markdown("### Pipeline Dashboard Overview")
        
        # Dashboard KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                f'<div class="audit-metric-card">'
                f'<div class="audit-number">{len(requirements_df)}</div>'
                f'<div class="audit-label">Active Job Openings</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f'<div class="audit-metric-card">'
                f'<div class="audit-number">{len(candidates_df)}</div>'
                f'<div class="audit-label">Total Registered Applicants</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                f'<div class="audit-metric-card">'
                f'<div class="audit-number" style="color: #34d399;">{len(st.session_state["shortlist"])}</div>'
                f'<div class="audit-label">Total Shortlisted</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        with col4:
            active_interviews = len([i for i in st.session_state["interviews"] if i["Status"] == "Scheduled"])
            st.markdown(
                f'<div class="audit-metric-card">'
                f'<div class="audit-number" style="color: #a78bfa;">{active_interviews}</div>'
                f'<div class="audit-label">Scheduled Interviews</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            
        st.markdown("---")
        
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.markdown("#### Applicants per Job Role")
            role_counts = candidates_df["Role Applied"].value_counts().reset_index()
            role_counts.columns = ["Role", "Count"]
            
            fig = go.Figure(data=[go.Bar(
                x=role_counts["Role"],
                y=role_counts["Count"],
                marker_color="#3b82f6",
                text=role_counts["Count"],
                textposition='auto'
            )])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc", family="Inter"),
                margin=dict(t=20, b=20, l=20, r=20),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col_chart2:
            st.markdown("#### Dynamic Candidate Distribution (Current Role)")
            # Show shortlist vs pool comparison
            in_shortlist_cnt = len(display_candidates[display_candidates["Name"].isin(st.session_state["shortlist"])])
            remaining_cnt = len(display_candidates) - in_shortlist_cnt
            
            labels = ["Shortlisted", "Under Review"]
            values = [in_shortlist_cnt, remaining_cnt]
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.4,
                marker=dict(colors=["#34d399", "#1e293b"])
            )])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc", family="Inter"),
                margin=dict(t=20, b=20, l=20, r=20),
                height=300,
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

    # ------------------ MODULE 3: JOB MANAGEMENT (CRUD) ------------------
    elif navigation_option == "Job Role Management (CRUD)":
        st.markdown("### Job Position Database Management")
        
        # Display existing job listings
        st.markdown("#### Active Positions")
        jobs_display_df = pd.DataFrame(st.session_state["jobs_db"])
        st.dataframe(jobs_display_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("#### Manage Positions")
        
        tab_add, tab_edit, tab_delete = st.tabs(["Add New Role", "Edit Role Requirements", "Delete Role"])
        
        with tab_add:
            st.markdown("##### Create a New Job Listing")
            with st.form("add_job_form", clear_on_submit=True):
                new_role_name = st.text_input("Job Role Name", placeholder="e.g. Cloud Engineer")
                new_role_skills = st.text_input("Required Skills (Comma separated)", placeholder="e.g. AWS, Python, Docker")
                new_role_exp = st.slider("Minimum Required Experience (Years)", 0, 15, 3)
                
                submitted = st.form_submit_button("Add Position to Directory")
                if submitted:
                    if not new_role_name.strip() or not new_role_skills.strip():
                        st.error("Please enter a valid Role Name and at least one Skill.")
                    else:
                        new_role = {
                            "Role": new_role_name.strip(),
                            "Required_Skills": new_role_skills.strip(),
                            "Min_Experience": int(new_role_exp)
                        }
                        st.session_state["jobs_db"].append(new_role)
                        st.success(f"Successfully added new position: **{new_role_name}**!")
                        safe_rerun()
                        
        with tab_edit:
            st.markdown("##### Modify Existing Role Criteria")
            if len(st.session_state["jobs_db"]) == 0:
                st.info("No active jobs to edit.")
            else:
                existing_roles = [j["Role"] for j in st.session_state["jobs_db"]]
                selected_edit_role = st.selectbox("Select Role to Edit", existing_roles)
                
                # Fetch details
                role_details = [j for j in st.session_state["jobs_db"] if j["Role"] == selected_edit_role][0]
                
                with st.form("edit_job_form"):
                    updated_skills = st.text_input("Required Skills", value=role_details["Required_Skills"])
                    updated_exp = st.slider("Minimum Experience (Years)", 0, 15, int(role_details["Min_Experience"]))
                    
                    edit_submitted = st.form_submit_button("Save Position Changes")
                    if edit_submitted:
                        for j in st.session_state["jobs_db"]:
                            if j["Role"] == selected_edit_role:
                                j["Required_Skills"] = updated_skills.strip()
                                j["Min_Experience"] = int(updated_exp)
                                break
                        st.success(f"Successfully updated **{selected_edit_role}** requirements!")
                        safe_rerun()
                        
        with tab_delete:
            st.markdown("##### Remove Role from Database")
            if len(st.session_state["jobs_db"]) == 0:
                st.info("No active jobs to delete.")
            else:
                selected_del_role = st.selectbox("Select Role to Remove", [j["Role"] for j in st.session_state["jobs_db"]])
                
                st.warning(f"Are you sure you want to permanently delete the **{selected_del_role}** job requirement?")
                if st.button("Confirm Delete Role", type="primary"):
                    st.session_state["jobs_db"] = [j for j in st.session_state["jobs_db"] if j["Role"] != selected_del_role]
                    st.success(f"Successfully deleted role: **{selected_del_role}**")
                    safe_rerun()

    # ------------------ MODULE 4: CANDIDATE PROFILE BROWSER ------------------
    elif navigation_option == "Candidate Profile Browser":
        st.markdown("### Candidate Profile Browser")
        
        candidate_names = sorted(candidates_df["Name"].tolist())
        selected_c_name = st.selectbox("Select Candidate Profile", candidate_names)
        
        c_row = candidates_df[candidates_df["Name"] == selected_c_name].iloc[0]
        c_skills = c_row["Skills"]
        c_exp = c_row["Experience_Years"]
        c_role = c_row["Role Applied"]
        
        # Calculate scores for candidate applied role
        applied_req = requirements_df[requirements_df["Role"] == c_role]
        if not applied_req.empty:
            applied_req = applied_req.iloc[0]
            req_skills = [s.strip() for s in applied_req["Required_Skills"].split(",")]
            m_exp = int(applied_req["Min_Experience"])
            c_score = calculate_score(c_skills, req_skills)
        else:
            c_score = 0
            m_exp = 0
            
        col_prof1, col_prof2 = st.columns([2, 1])
        
        with col_prof1:
            # Styled Header Profile Card
            badge_is_short = '<span class="shortlisted-badge" style="margin-left:0.5rem;">Shortlisted</span>' if selected_c_name in st.session_state["shortlist"] else ''
            
            card_html = (
                f'<div class="candidate-card" style="border-left: 5px solid #3b82f6;">'
                f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">'
                f'<div>'
                f'<h2 style="margin:0; color:#f8fafc;">{selected_c_name}</h2>'
                f'<p style="margin:0; color:#94a3b8; font-size:1rem;">Applied for: <strong>{c_role}</strong></p>'
                f'</div>'
                f'<div>'
                f'<span class="score-badge" style="font-size:1.1rem; padding:0.4rem 0.8rem;">Match: {c_score}%</span>'
                f'{badge_is_short}'
                f'</div>'
                f'</div>'
                f'<div style="margin-bottom:1rem;">'
                f'<span style="color:#94a3b8; font-size:0.95rem;">Contact Information:</span><br>'
                f'<span style="color:#cbd5e1;">📧 {selected_c_name.lower().replace(" ", "")}@example.com | 📱 +91 98765 43210</span>'
                f'</div>'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
            
            st.markdown("#### Candidate Experience Timeline")
            timeline_html = (
                f'<div class="timeline-item">'
                f'<div class="timeline-marker"></div>'
                f'<strong>Lead Specialist ({c_role})</strong> at Tech Solutions (2024 - Present)<br>'
                f'<span style="color:#94a3b8; font-size:0.9rem;">Spearheaded agile development, deployment cycles, and coordinated key cross-functional milestones.</span>'
                f'</div>'
                f'<div class="timeline-item">'
                f'<div class="timeline-marker"></div>'
                f'<strong>Associate Professional</strong> at Innovate Corp (2021 - 2024)<br>'
                f'<span style="color:#94a3b8; font-size:0.9rem;">Implemented clean coding architectures, performed unit tests, and managed git pipelines.</span>'
                f'</div>'
                f'<div class="timeline-item" style="border:none;">'
                f'<div class="timeline-marker"></div>'
                f'<strong>Junior Executive / Trainee</strong> at Systemic Systems (2020 - 2021)<br>'
                f'<span style="color:#94a3b8; font-size:0.9rem;">Assisted in writing features, debugging, and documenting codebases.</span>'
                f'</div>'
            )
            st.markdown(timeline_html, unsafe_allow_html=True)
            
        with col_prof2:
            st.markdown("#### Assessment Details")
            st.metric("Total Experience", f"{c_exp} Years", delta=f"{int(c_exp) - m_exp} Over Req" if int(c_exp) >= m_exp else f"{int(c_exp) - m_exp} Under Req")
            
            st.markdown("##### Key Skills List")
            for skill in c_skills.split(","):
                st.markdown(f"- `{skill.strip()}`")
                
            st.markdown("---")
            # Interactive assessment notes
            st.markdown("##### Internal HR Review Notes")
            saved_notes = st.session_state["candidate_notes"].get(selected_c_name, "")
            
            note_input = st.text_area("Write interviewer remarks:", value=saved_notes, key=f"notes_{selected_c_name}")
            if st.button("Save Profile Notes"):
                st.session_state["candidate_notes"][selected_c_name] = note_input
                st.success("Notes successfully updated!")

    # ------------------ MODULE 5: INTERVIEW SCHEDULER & CALENDAR ------------------
    elif navigation_option == "Interview Scheduler & Calendar":
        st.markdown("### Interview Scheduling & Calendar Center")
        
        tab_sched, tab_cal = st.tabs(["Schedule Interview", "Calendar Schedule"])
        
        with tab_sched:
            st.markdown("##### Arrange a New Interview Session")
            
            avail_candidates = sorted(candidates_df["Name"].tolist())
            selected_int_cand = st.selectbox("Select Candidate for Interview", avail_candidates)
            
            c_det = candidates_df[candidates_df["Name"] == selected_int_cand].iloc[0]
            cand_role = c_det["Role Applied"]
            
            col_date, col_time = st.columns(2)
            with col_date:
                int_date = st.date_input("Interview Date", datetime.date.today() + datetime.timedelta(days=2))
            with col_time:
                int_time = st.selectbox("Interview Time Slot", ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"])
                
            int_mode = st.selectbox("Interview Mode", ["Zoom Meeting", "Microsoft Teams", "In-Person Office Interview", "Phone Screening"])
            
            if st.button("Confirm Interview Schedule", type="primary"):
                new_interview = {
                    "Name": selected_int_cand,
                    "Role": cand_role,
                    "Date": str(int_date),
                    "Time": int_time,
                    "Mode": int_mode,
                    "Status": "Scheduled"
                }
                st.session_state["interviews"].append(new_interview)
                # Create notification
                st.session_state["notifications"].insert(0, {
                    "Message": f"Interview scheduled with {selected_int_cand} for {cand_role}",
                    "Time": "Just now",
                    "Read": False
                })
                st.success(f"Interview successfully scheduled for **{selected_int_cand}** on {int_date} at {int_time} via {int_mode}!")
                safe_rerun()
                
        with tab_cal:
            st.markdown("##### Upcoming Interview Schedule")
            
            if len(st.session_state["interviews"]) == 0:
                st.info("No interviews scheduled currently.")
            else:
                for idx, interview in enumerate(st.session_state["interviews"]):
                    status_color = "#34d399" if interview["Status"] == "Completed" else "#3b82f6"
                    
                    # Custom calendar cards
                    cal_card_html = (
                        f'<div class="calendar-card" style="border-left: 4px solid {status_color};">'
                        f'<div style="display:flex; justify-content:space-between; align-items:center;">'
                        f'<strong>Candidate: {interview["Name"]}</strong>'
                        f'<span style="background-color:#1e293b; color:{status_color}; border:1px solid {status_color}; padding:0.1rem 0.5rem; border-radius:10px; font-size:0.8rem; font-weight:600;">{interview["Status"]}</span>'
                        f'</div>'
                        f'<div style="color:#94a3b8; font-size:0.9rem; margin-top:0.4rem;">'
                        f'Role: <strong>{interview["Role"]}</strong><br>'
                        f'Schedule: 📅 {interview["Date"]} at {interview["Time"]} | Mode: {interview["Mode"]}'
                        f'</div>'
                        f'</div>'
                    )
                    st.markdown(cal_card_html, unsafe_allow_html=True)
                    
                    # Update status button
                    if interview["Status"] == "Scheduled":
                        col_dummy, col_done = st.columns([5, 1])
                        with col_done:
                            if st.button("Mark Completed", key=f"int_{idx}", use_container_width=True):
                                interview["Status"] = "Completed"
                                st.success("Interview status updated!")
                                safe_rerun()

    # ------------------ MODULE 6: NOTIFICATIONS CENTER ------------------
    elif navigation_option == "Notifications Center":
        st.markdown("### Notifications Center")
        
        unread_count = len([n for n in st.session_state["notifications"] if not n["Read"]])
        st.write(f"You have **{unread_count}** unread notification(s).")
        
        col_actions1, col_actions2 = st.columns([1, 4])
        with col_actions1:
            if st.button("Mark All as Read", use_container_width=True):
                for n in st.session_state["notifications"]:
                    n["Read"] = True
                safe_rerun()
        with col_actions2:
            if st.button("Clear All History", use_container_width=True):
                st.session_state["notifications"] = []
                safe_rerun()
                
        st.markdown("---")
        
        if len(st.session_state["notifications"]) == 0:
            st.info("Your notification tray is empty.")
        else:
            for n in st.session_state["notifications"]:
                read_dot = "🟢" if not n["Read"] else "⚪"
                card_border = "1px solid #3b82f6" if not n["Read"] else "1px solid #334155"
                card_bg = "rgba(59, 130, 246, 0.05)" if not n["Read"] else "#1e293b"
                
                st.markdown(
                    f"""
                    <div style="background-color:{card_bg}; padding:1rem; border-radius:8px; border:{card_border}; margin-bottom:0.8rem; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="margin-right:0.5rem;">{read_dot}</span>
                            <span style="color:#f8fafc; font-size:0.95rem;">{n['Message']}</span>
                        </div>
                        <span style="color:#94a3b8; font-size:0.85rem;">{n['Time']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # ------------------ MODULE 7: HR ANALYTICS & INSIGHTS ------------------
    elif navigation_option == "Advanced HR Analytics":
        st.markdown("### Advanced HR Recruitment Analytics")
        
        # 1. Row 1 charts
        col_an1, col_an2 = st.columns(2)
        with col_an1:
            st.markdown("#### Average Match Score by Applied Role")
            avg_matches = candidates_df_calc.groupby("Role Applied")["Match_Score"].mean().reset_index()
            
            fig = go.Figure(data=[go.Bar(
                x=avg_matches["Role Applied"],
                y=avg_matches["Match_Score"],
                marker_color="#10b981",
                text=[f"{val:.1f}%" for val in avg_matches["Match_Score"]],
                textposition='auto'
            )])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc", family="Inter"),
                margin=dict(t=20, b=20, l=20, r=20),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col_an2:
            st.markdown("#### Experience Band Spread of All Applicants")
            
            def get_band(exp):
                if exp <= 2: return "Entry (0-2 Years)"
                elif exp <= 5: return "Mid-Level (3-5 Years)"
                else: return "Senior (6+ Years)"
                
            cand_temp = candidates_df.copy()
            cand_temp["Exp_Band"] = cand_temp["Experience_Years"].apply(get_band)
            band_counts = cand_temp["Exp_Band"].value_counts().reset_index()
            band_counts.columns = ["Band", "Count"]
            
            fig = go.Figure(data=[go.Pie(
                labels=band_counts["Band"],
                values=band_counts["Count"],
                hole=.4,
                marker=dict(colors=["#3b82f6", "#a78bfa", "#f59e0b"])
            )])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f8fafc", family="Inter"),
                margin=dict(t=20, b=20, l=20, r=20),
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
            
        st.markdown("---")
        st.markdown("#### Match Score Distribution Density")
        
        # Plot score distribution histogram
        fig_hist = go.Figure(data=[go.Histogram(
            x=candidates_df_calc["Match_Score"],
            nbinsx=10,
            marker_color="#a78bfa",
            opacity=0.75
        )])
        fig_hist.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc", family="Inter"),
            xaxis=dict(title="Match Score (%)"),
            yaxis=dict(title="Number of Candidates"),
            margin=dict(t=20, b=20, l=20, r=20),
            height=280
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # ------------------ MODULE 8: EMPLOYEE DIRECTORY ------------------
    elif navigation_option == "Employee Directory":
        st.markdown("### Corporate Employee Directory")
        
        # Metrics
        col_dir1, col_dir2, col_dir3 = st.columns(3)
        with col_dir1:
            st.metric("Corporate Employees", len(st.session_state["employee_db"]))
        with col_dir2:
            depts = set([e["Department"] for e in st.session_state["employee_db"]])
            st.metric("Active Departments", len(depts))
        with col_dir3:
            st.metric("Internal Promotion Rate", "14.2%")
            
        st.markdown("---")
        
        # Filter Department
        dept_options = ["All Departments"] + sorted(list(depts))
        selected_dept = st.selectbox("Filter Employee Department", dept_options)
        
        # Filter DB
        if selected_dept == "All Departments":
            filtered_employees = st.session_state["employee_db"]
        else:
            filtered_employees = [e for e in st.session_state["employee_db"] if e["Department"] == selected_dept]
            
        st.markdown("##### Employees List")
        emp_df_display = pd.DataFrame(filtered_employees)
        st.dataframe(emp_df_display, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        # Promotion Simulator
        st.markdown("##### Internal Transfer / Promotion Simulator")
        with st.form("promote_employee_form"):
            emp_names = [e["Name"] for e in st.session_state["employee_db"]]
            selected_emp = st.selectbox("Select Employee to Update", emp_names)
            new_title = st.text_input("New Target Role Title")
            new_performance = st.selectbox("New Performance Appraisal Score", ["Meets Expectations", "Exceeds Expectations", "Outstanding"])
            
            p_submitted = st.form_submit_button("Update Employee Profile")
            if p_submitted:
                for emp in st.session_state["employee_db"]:
                    if emp["Name"] == selected_emp:
                        if new_title.strip():
                            emp["Role"] = new_title.strip()
                        emp["Performance"] = new_performance
                        break
                st.success(f"Successfully updated internal profile for **{selected_emp}**!")
                safe_rerun()

    # ------------------ MODULE 9: AI CHATBOT ASSISTANT ------------------
    elif navigation_option == "AI Chatbot Assistant":
        st.markdown("### AI Talent Copilot Assistant")
        st.write("Ask your AI assistant questions regarding candidates, match scores, experience levels, or specific skills.")
        
        # Render Chat History
        for message in st.session_state["chat_history"]:
            bubble_class = "chat-bubble-user" if message["role"] == "user" else "chat-bubble-assistant"
            st.markdown(f'<div class="{bubble_class}">{message["content"]}</div>', unsafe_allow_html=True)
            
        # Preset Quick Query Buttons
        st.markdown("##### Fast Queries")
        col_q1, col_q2, col_q3 = st.columns(3)
        with col_q1:
            q1_clicked = st.button("Who is top matched Software Engineer?", use_container_width=True)
        with col_q2:
            q2_clicked = st.button("List candidates with React skills", use_container_width=True)
        with col_q3:
            q3_clicked = st.button("Show candidates with >= 5 yrs exp", use_container_width=True)
            
        chat_input = st.text_input("Ask your query here...", placeholder="e.g. Find candidates who know SQL and Python")
        send_clicked = st.button("Submit Query")
        
        # Chat Logic triggered
        user_query = None
        if q1_clicked:
            user_query = "Who is top matched Software Engineer?"
        elif q2_clicked:
            user_query = "List candidates with React skills"
        elif q3_clicked:
            user_query = "Show candidates with >= 5 yrs exp"
        elif send_clicked and chat_input.strip():
            user_query = chat_input.strip()
            
        if user_query:
            # Append user message
            st.session_state["chat_history"].append({"role": "user", "content": user_query})
            
            # Simple simulation response parser
            response = ""
            query_lower = user_query.lower()
            
            if "top matched" in query_lower or "best candidate" in query_lower:
                # Find top candidate
                role_se = candidates_df_calc[candidates_df_calc["Role Applied"] == "Software Engineer"]
                if not role_se.empty:
                    top_se = role_se.iloc[0]
                    response = f"The top matched candidate for **Software Engineer** is **{top_se['Name']}** with a Dynamic Match Score of **{top_se['Match_Score']}%** (Experience: {top_se['Experience_Years']} years)."
                else:
                    response = "I couldn't find any candidate applying for Software Engineer in the database."
                    
            elif "react" in query_lower:
                react_cands = candidates_df_calc[candidates_df_calc["Skills"].str.lower().str.contains("react")]["Name"].tolist()
                if react_cands:
                    response = f"The candidates possessing **React** skills in the pool are: " + ", ".join([f"**{name}**" for name in react_cands]) + "."
                else:
                    response = "There are no candidates with React listed in their skill set."
                    
            elif "5 yrs" in query_lower or "5 years" in query_lower or "experience" in query_lower:
                exp_cands = candidates_df_calc[candidates_df_calc["Experience_Years"].astype(float) >= 5.0]
                if not exp_cands.empty:
                    exp_names = exp_cands["Name"].tolist()
                    response = f"Candidates with **5 or more years of experience** are: " + ", ".join([f"**{n}** ({exp_cands[exp_cands['Name']==n].iloc[0]['Experience_Years']} years)" for n in exp_names]) + "."
                else:
                    response = "No candidates in the database have 5 or more years of experience."
                    
            else:
                # Default generic matching scan
                matched_keywords = []
                for skill in all_skills:
                    if skill.lower() in query_lower:
                        matched_keywords.append(skill)
                        
                if matched_keywords:
                    # Filter candidates
                    matched_names = []
                    for idx, r in candidates_df.iterrows():
                        skills_split = [s.strip().lower() for s in r["Skills"].split(",")]
                        if any(kw.lower() in skills_split for kw in matched_keywords):
                            matched_names.append(r["Name"])
                            
                    if matched_names:
                        response = f"Based on your request, candidates matching skills ({', '.join(matched_keywords)}) are: " + ", ".join([f"**{n}**" for n in matched_names]) + "."
                    else:
                        response = f"I scanned for keywords ({', '.join(matched_keywords)}) but couldn't find matching candidates."
                else:
                    response = "I received your query. To help, you can search for candidates by role (e.g. Software Engineer), skills (e.g. React, SQL, Figma), or experience level!"
                    
            st.session_state["chat_history"].append({"role": "assistant", "content": response})
            safe_rerun()

    # ------------------ MODULE 10: SYSTEM SETTINGS ------------------
    elif navigation_option == "System Settings":
        st.markdown("### Talent Copilot System Settings")
        
        st.markdown("#### Dynamic Match Weight Factors")
        st.write("Tune how weights are balanced when computing the dynamic Candidate Match Score:")
        
        weights = st.session_state["settings_weights"]
        
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            w_tech = st.slider("Technical Fit Weight (%)", 0, 100, int(weights["Technical Fit"]))
            w_exp = st.slider("Experience Fit Weight (%)", 0, 100, int(weights["Experience Fit"]))
        with col_w2:
            w_comm = st.slider("Communication Fit Weight (%)", 0, 100, int(weights["Communication"]))
            w_cult = st.slider("Culture Fit Weight (%)", 0, 100, int(weights["Culture Fit"]))
            
        total_weight = w_tech + w_exp + w_comm + w_cult
        st.write(f"Current weight total: **{total_weight}%**")
        
        if total_weight != 100:
            st.error("All match weight factors must sum up to exactly **100%** to save.")
        else:
            if st.button("Save Weight Configuration"):
                weights["Technical Fit"] = w_tech
                weights["Experience Fit"] = w_exp
                weights["Communication"] = w_comm
                weights["Culture Fit"] = w_cult
                st.success("Successfully updated matching algorithm weight variables!")
                safe_rerun()
                
        st.markdown("---")
        st.markdown("#### Advanced System Parameters")
        st.checkbox("Enable automated email notifications alerts to candidates", value=False)
        st.checkbox("Trigger real-time notifications on shortlist updates", value=True)
        st.slider("Fairness Audit Skew Limit Flag (%)", 50, 100, 70)
        
        st.markdown("---")
        st.markdown("#### Database Factory Reset")
        if st.button("Reset Session State Databases", type="secondary"):
            if "jobs_db" in st.session_state: del st.session_state["jobs_db"]
            if "candidates_db" in st.session_state: del st.session_state["candidates_db"]
            if "interviews" in st.session_state: del st.session_state["interviews"]
            if "notifications" in st.session_state: del st.session_state["notifications"]
            if "employee_db" in st.session_state: del st.session_state["employee_db"]
            if "chat_history" in st.session_state: del st.session_state["chat_history"]
            if "settings_weights" in st.session_state: del st.session_state["settings_weights"]
            if "candidate_notes" in st.session_state: del st.session_state["candidate_notes"]
            st.success("Database session states cleared. Reloading standard configurations.")
            safe_rerun()
        
else:
    st.error("Please configure the CSV data files under the `data/` folder to run the Recruitment Copilot.")
