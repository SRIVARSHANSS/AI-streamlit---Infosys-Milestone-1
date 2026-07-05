import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import textwrap

# 1. Must call set_page_config as the first Streamlit command
st.set_page_config(
    page_title="AI Recruitment & Talent Copilot",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Safe rerun function to support different Streamlit versions
def safe_rerun():
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

# Initialize session state for shortlist
if "shortlist" not in st.session_state:
    st.session_state["shortlist"] = []

# Helper to load data safely
def load_csv_data(filepath):
    try:
        if os.path.exists(filepath):
            return pd.read_csv(filepath)
        else:
            st.error(f"⚠️ Critical Error: Data file '{filepath}' is missing from the disk.")
            return None
    except Exception as e:
        st.error(f"⚠️ Error reading '{filepath}': {e}")
        return None

# Load dataset
candidates_df = load_csv_data("data/candidates.csv")
requirements_df = load_csv_data("data/job_requirements.csv")

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
        st.write("🏢 [Logo Placeholder]")

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
    
    # 2. Sidebar Filters
    st.sidebar.markdown("### 🔍 Target Job Role")
    roles = requirements_df["Role"].tolist()
    selected_role = st.sidebar.selectbox("Select Target Position", roles)
    
    # Extract role requirements
    role_req = requirements_df[requirements_df["Role"] == selected_role].iloc[0]
    required_skills = [s.strip() for s in role_req["Required_Skills"].split(",")]
    min_experience = int(role_req["Min_Experience"])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🛠️ Filter Candidate Pool")
    
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
    st.sidebar.markdown("### 📋 Shortlist Control")
    if st.sidebar.button("Clear Candidate Shortlist", use_container_width=True):
        st.session_state["shortlist"] = []
        st.sidebar.success("Shortlist cleared!")
        safe_rerun()
        
    st.sidebar.info(f"Currently Shortlisted: **{len(st.session_state['shortlist'])}** candidate(s)")
    
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
        
    # 3. Main tab layout
    tab_pool, tab_explain, tab_bias = st.tabs([
        "📊 Candidate Pool", 
        "🕸️ Comparison & Explainability", 
        "⚖️ Bias & Fairness Audit"
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
                            safe_rerun()
                    else:
                        if st.button("Shortlist", key=f"shortlist_{name}_{idx}", use_container_width=True, type="primary"):
                            st.session_state["shortlist"].append(name)
                            safe_rerun()
                st.write("") # small spacing
                
    # ------------------ TAB 2: COMPARISON & EXPLAINABILITY ------------------
    with tab_explain:
        st.markdown("### Candidate Comparison Radar & Explainability Ledger")
        
        # Select candidates to compare from shortlist
        shortlisted_names = list(set(st.session_state["shortlist"]))
        
        st.markdown("Select 2 to 3 candidates from your shortlist to analyze side-by-side:")
        selected_candidates = st.multiselect(
            "Select Candidates",
            options=shortlisted_names,
            default=shortlisted_names[:3] if len(shortlisted_names) >= 2 else None,
            max_selections=3
        )
        
        if len(selected_candidates) < 2:
            st.info("⚠️ Please shortlist and select at least 2 candidates in the multiselect above to generate the radar comparison and explainability ledger.")
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
            st.markdown("### 📑 Explainability Ledger")
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
        st.markdown("### ⚖️ Bias & Fairness Audit Panel")
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
            # Group into experience bands:
            # - Entry (0-2 years)
            # - Mid-Level (2-5 years)
            # - Senior (5+ years)
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
                            ⚠️ **Potential Shortlist Skew Detected!**
                            
                            The experience band **{skewed_band}** represents **{skew_pct:.1f}%** of your shortlist, which exceeds the recommended 70% threshold.
                            
                            **Ethical AI Recommendation:**
                            A highly concentrated shortlist might introduce age or tier-based bias. To ensure cognitive diversity and team growth potential, we recommend reviewing candidates in other experience brackets before submitting the final hiring recommendation.
                        """)
                    )
                else:
                    st.success(
                        textwrap.dedent(f"""
                            ✅ **Shortlist Diversity Check Passed**
                            
                            No single experience band exceeds the 70% concentration limit. The shortlist represents a healthy, balanced spread of experience levels.
                        """)
                    )
                    
        st.markdown("")
        st.caption("ℹ️ **Fairness Auditor Note:** This tool evaluates simple statistical distribution skews on selected parameters. It is a rule-based heuristic check intended for decision support, not an automated legal fairness/ML audit.")
        
else:
    st.error("Please configure the CSV data files under the `data/` folder to run the Recruitment Copilot.")
