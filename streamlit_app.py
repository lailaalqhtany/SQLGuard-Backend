import streamlit as st
import requests


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="SQLGuard",
    page_icon="🛡️",
    layout="centered"
)


# ==========================================
# Title
# ==========================================

st.title("🛡️ SQLGuard")
st.subheader("SQL Injection Detection System")

st.write(
    "Enter an SQL query below to analyze it using "
    "Machine Learning and Rule-Based Detection."
)


# ==========================================
# SQL Query Input
# ==========================================

query = st.text_area(
    "Enter SQL Query",
    placeholder="Example: SELECT * FROM users WHERE username='admin'",
    height=150
)


# ==========================================
# Analyze Button
# ==========================================

if st.button("🔍 Analyze Query"):

    if not query.strip():

        st.warning("Please enter an SQL query.")

    else:

        try:

            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json={"query": query},
                timeout=10
            )


            # ==================================
            # Successful Response
            # ==================================

            if response.status_code == 200:

                result = response.json()

                verdict = result["verdict"]
                risk_score = result["risk_score"]
                ml_probability = result["ml_probability"]
                rule_score = result["rule_score"]
                severity = result["severity"]
                indicators = result["indicators"]


                st.divider()

                st.subheader("Analysis Result")


                # ==================================
                # Verdict
                # ==================================

                if verdict == "Malicious":

                    st.error("🚨 MALICIOUS")

                elif verdict == "Suspicious":

                    st.warning("⚠️ SUSPICIOUS")

                else:

                    st.success("✅ SAFE")


                # ==================================
                # Risk Score
                # ==================================

                st.metric(
                    label="Risk Score",
                    value=f"{risk_score}%"
                )


                # ==================================
                # Detection Details
                # ==================================

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "ML Probability",
                        f"{ml_probability}%"
                    )

                with col2:

                    st.metric(
                        "Rule Score",
                        rule_score
                    )


                st.write("### Severity")

                if severity == "critical":

                    st.error("🔴 Critical")

                elif severity == "high":

                    st.warning("🟠 High")

                elif severity == "medium":

                    st.warning("🟡 Medium")

                else:

                    st.info("🟢 None")


                # ==================================
                # Detected Indicators
                # ==================================

                st.write("### Detected Indicators")

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
                # Full API Response
                # ==================================

                with st.expander("View Technical Details"):

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

            st.info(
                "Make sure FastAPI is running on http://127.0.0.1:8000"
            )


        except requests.exceptions.Timeout:

            st.error(
                "❌ The API request timed out."
            )