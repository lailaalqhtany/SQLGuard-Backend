import streamlit as st
import requests


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="SQLGuard | SQL Injection Detection",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================
# Custom CSS
# ==========================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 1.15rem;
        opacity: 0.75;
        margin-bottom: 2rem;
    }

    .result-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }

    .safe {
        border: 2px solid #21c55d;
    }

    .suspicious {
        border: 2px solid #f59e0b;
    }

    .malicious {
        border: 2px solid #ef4444;
    }

    .result-title {
        font-size: 2rem;
        font-weight: 800;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# Header
# ==========================================

st.markdown(
    '<div class="main-title">🛡️ SQLGuard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Hybrid SQL Injection Detection System using Machine Learning and Rule-Based Analysis'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# Information
# ==========================================

with st.expander("ℹ️ About SQLGuard"):

    st.write(
        """
        SQLGuard is a cybersecurity detection system designed to identify
        potentially malicious SQL queries.

        It combines two detection approaches:

        • Machine Learning using TF-IDF and Random Forest  
        • Rule-Based Detection for known SQL injection patterns

        The final verdict is based on a hybrid risk engine.
        """
    )


# ==========================================
# Query Input
# ==========================================

st.markdown(
    '<div class="section-title">🔍 Analyze SQL Query</div>',
    unsafe_allow_html=True
)

query = st.text_area(
    "Enter your SQL query",
    placeholder="Example: SELECT * FROM users WHERE username='admin'",
    height=180,
    label_visibility="collapsed"
)


# ==========================================
# Example Queries
# ==========================================

st.caption("Try an example:")

example_col1, example_col2, example_col3 = st.columns(3)

with example_col1:

    if st.button("✅ Safe Example", use_container_width=True):

        query = "SELECT * FROM users WHERE username='admin'"


with example_col2:

    if st.button("⚠️ Suspicious Example", use_container_width=True):

        query = "SELECT * FROM users WHERE username='admin' OR id=5"


with example_col3:

    if st.button("🚨 Malicious Example", use_container_width=True):

        query = "' OR 1=1 --"


# ==========================================
# Analyze
# ==========================================

if st.button(
    "🔎 Analyze Query",
    type="primary",
    use_container_width=True
):

    if not query.strip():

        st.warning("Please enter an SQL query first.")

    else:

        try:

            with st.spinner("Analyzing query..."):

                response = requests.post(
                    "https://sqlguard-api.onrender.com/predict",
                    json={"query": query},
                    timeout=30
                )


            if response.status_code == 200:

                result = response.json()

                verdict = result["verdict"]
                risk_score = result["risk_score"]
                ml_probability = result["ml_probability"]
                rule_score = result["rule_score"]
                severity = result["severity"]
                indicators = result["indicators"]


                st.divider()

                # ==================================
                # Verdict
                # ==================================

                if verdict == "Malicious":

                    st.markdown(
                        """
                        <div class="result-box malicious">
                            <div class="result-title">
                                🚨 MALICIOUS
                            </div>
                            <div>
                                Potential SQL Injection Detected
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                elif verdict == "Suspicious":

                    st.markdown(
                        """
                        <div class="result-box suspicious">
                            <div class="result-title">
                                ⚠️ SUSPICIOUS
                            </div>
                            <div>
                                Query Requires Further Investigation
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        """
                        <div class="result-box safe">
                            <div class="result-title">
                                ✅ SAFE
                            </div>
                            <div>
                                No Significant SQL Injection Risk Detected
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                # ==================================
                # Metrics
                # ==================================

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Risk Score",
                        f"{risk_score}%"
                    )

                with col2:

                    st.metric(
                        "ML Probability",
                        f"{ml_probability}%"
                    )

                with col3:

                    st.metric(
                        "Rule Score",
                        rule_score
                    )


                # ==================================
                # Severity
                # ==================================

                st.markdown(
                    '<div class="section-title">⚡ Severity</div>',
                    unsafe_allow_html=True
                )

                if severity == "critical":

                    st.error("🔴 CRITICAL")

                elif severity == "high":

                    st.warning("🟠 HIGH")

                elif severity == "medium":

                    st.warning("🟡 MEDIUM")

                else:

                    st.success("🟢 NONE")


                # ==================================
                # Indicators
                # ==================================

                st.markdown(
                    '<div class="section-title">🧩 Detected Indicators</div>',
                    unsafe_allow_html=True
                )

                if indicators:

                    for indicator in indicators:

                        st.write(
                            f"**Rule:** {indicator['rule']}"
                        )

                        st.code(
                            indicator["match"],
                            language="sql"
                        )

                else:

                    st.success(
                        "No suspicious SQL injection indicators detected."
                    )


                # ==================================
                # Technical Details
                # ==================================

                with st.expander("🧪 View Technical Details"):

                    st.json(result)


            else:

                st.error(
                    f"API Error: {response.status_code}"
                )

                st.code(response.text)


        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Could not connect to SQLGuard API."
            )


        except requests.exceptions.Timeout:

            st.error(
                "⏱️ The API request timed out."
            )


# ==========================================
# Footer
# ==========================================

st.divider()

st.caption(
    "🛡️ SQLGuard — Hybrid Machine Learning + Rule-Based SQL Injection Detection"
)