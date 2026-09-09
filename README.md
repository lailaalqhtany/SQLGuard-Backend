# 🛡️ SQLGuard

## AI-Powered SQL Injection Detection System

## Project Overview

SQLGuard is an AI-powered SQL Injection Detection System designed to detect and classify potentially malicious SQL queries.

The system combines two detection approaches:

- Machine Learning using TF-IDF and Random Forest.
- Rule-Based Detection using Regex and security rules.

The two approaches work together to calculate a final risk score and classify the query as Safe, Suspicious, or Malicious.

SQLGuard provides an interactive Streamlit interface and a FastAPI backend for real-time query analysis.

## How It Works

1. The user enters an SQL query through the Streamlit interface.
2. Streamlit sends the query to the FastAPI backend.
3. The backend analyzes the query using the Machine Learning and Rule-Based engines.
4. The ML engine calculates the probability of SQL Injection.
5. The Rule Engine checks for known SQL Injection patterns.
6. The results are combined to calculate the final risk score.
7. SQLGuard returns the verdict, severity, risk score, and detected indicators.

8. ## Results & Performance

SQLGuard was evaluated using a dataset of SQL queries and achieved strong classification performance.

| Metric | Result |
|---|---:|
| Accuracy | 99.53% |
| Precision | 99.82% |
| Recall | 98.95% |
| F1-Score | 99.38% |

The Machine Learning model uses TF-IDF for text feature extraction and a Random Forest classifier for SQL Injection detection.

In addition to Machine Learning, SQLGuard uses a Rule-Based Detection Engine to identify known SQL Injection patterns and provide additional security indicators.

## Technologies Used

- Python
- FastAPI
- Streamlit
- Scikit-learn
- TF-IDF
- Random Forest
- Regular Expressions (Regex)
- Git & GitHub
- Render
- Streamlit Cloud

SQLGuard is a cybersecurity system designed to detect SQL Injection attacks using a hybrid approach that combines **Machine Learning** with **Rule-Based Detection**.

The system analyzes SQL queries and provides a security verdict along with a risk score, severity level, machine-learning probability, rule score, and detected attack indicators.

---

## 🎯 Project Idea

SQL Injection is one of the most common web application security threats.

SQLGuard provides an automated detection mechanism that analyzes SQL queries before they are processed by an application.

The system combines:

- 🤖 Machine Learning
- 🛡️ Rule-Based Detection
- 📊 Risk Assessment
- 🔍 Explainable Detection Indicators

---

## 🏗️ System Architecture

## System Architecture

![SQLGuard Architecture](Architecture.png)

```text
User
  │
  ▼
Streamlit Web Interface
  │
  │ HTTP POST /predict
  ▼
FastAPI Backend
  │
  ├───────────────┬───────────────┐
  ▼               ▼               │
ML Engine      Rule Engine        │
  │               │               │
  │               │               │
  └───────┬───────┘               │
          ▼                       │
   Hybrid Risk Assessment        │
          │                       │
          ▼                       │
     Final Result ────────────────┘
     🤖 Machine Learning

The Machine Learning component uses:

* TF-IDF Vectorizer for text feature extraction.
* Random Forest Classifier for SQL Injection classification.

The trained model analyzes the SQL query and estimates the probability that the query represents a SQL Injection attack.

Model Performance

The model achieved approximately:

99.53% Accuracy

The evaluation was performed using a separate testing dataset.

⸻

🛡️ Rule-Based Detection

SQLGuard also uses a Rule Engine based on pattern matching and security heuristics.

The Rule Engine helps identify known SQL Injection patterns such as:

* Tautology-based attacks
* SQL comments
* UNION-based patterns
* Suspicious SQL operators
* Other known injection indicators

This provides an additional detection layer alongside Machine Learning.

⸻

🔄 Hybrid Detection

Instead of relying only on Machine Learning, SQLGuard combines:

ML Probability + Rule Score

to calculate an overall risk assessment.

The system then determines:

* Safe
* Suspicious
* Malicious

and assigns an appropriate severity level.

⸻

📊 Detection Results

For every analyzed query, SQLGuard can provide:

* Verdict
* Risk Score
* ML Probability
* Rule Score
* Severity
* Detected Indicators
* Matched Security Rules

This makes the detection process more explainable to the user.

## 💻 Technologies Used

- **Python** — Core development
- **FastAPI** — Backend API
- **Streamlit** — Web Interface
- **Scikit-learn** — Machine Learning
- **TF-IDF** — Text Feature Extraction
- **Random Forest** — Classification
- **Regex** — Rule-Based Detection
- **Git & GitHub** — Version Control
- **Render** — API Deployment
- **Streamlit Cloud** — Web Deployment
Deployment

SQLGuard consists of two main deployed components:

Backend API

The FastAPI backend is deployed as a web service.

Frontend

The Streamlit application provides the interactive web interface and communicates with the deployed API.
Example

Malicious Query
SELECT * FROM users WHERE username='admin' OR '1'='1'
Expected result:
Verdict: Malicious
Risk Score: High
Safe Query
 SELECT * FROM users WHERE username='admin'
Expected result:
Verdict: Safe
Project Purpose

SQLGuard was developed as a cybersecurity project demonstrating the practical use of Artificial Intelligence and Machine Learning for detecting web application security threats.

The project focuses on combining automated machine-learning classification with explainable rule-based security analysis.
Project Team

SQLGuard

Cybersecurity Project

⸻

📌 Future Improvements

Possible future improvements include:

* Expanding the training dataset
* Supporting additional SQL Injection techniques
* Improving the rule engine
* Adding authentication and access control
* Adding security monitoring and logging
* Integrating SQLGuard with web applications
* Developing a REST API for external security tools

⸻

🛡️ Conclusion

SQLGuard demonstrates how Artificial Intelligence can be integrated into cybersecurity systems to automate SQL Injection detection.

By combining Machine Learning and Rule-Based Detection, the system provides both automated classification and understandable security indicators.
