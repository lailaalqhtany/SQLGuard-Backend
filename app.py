from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import re


# ==========================================
# Load ML Model
# ==========================================

model = joblib.load("sqlguard_model.pkl")
vectorizer = joblib.load("sqlguard_vectorizer.pkl")


app = FastAPI(title="SQLGuard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==========================================
# Request Model
# ==========================================

class QueryRequest(BaseModel):
    query: str


# ==========================================
# SQL Injection Rules
# ==========================================

RULES = [

    {
        "name": "Tautology",
        "severity": "high",
        "weight": 45,
        "pattern": re.compile(
            r"('|\" )\s*(or|and)\s+('|\" )?\s*\d+\s*('|\" )?\s*=\s*('|\" )?\s*\d+",
            re.IGNORECASE
        )
    },

    {
        "name": "OR 1=1",
        "severity": "high",
        "weight": 45,
        "pattern": re.compile(
            r"\b(or|and)\b\s+\d+\s*=\s*\d+",
            re.IGNORECASE
        )
    },

    {
        "name": "UNION SELECT",
        "severity": "critical",
        "weight": 55,
        "pattern": re.compile(
            r"\bunion\b(\s+all)?\s+\bselect\b",
            re.IGNORECASE
        )
    },

    {
        "name": "Stacked Query",
        "severity": "high",
        "weight": 40,
        "pattern": re.compile(
            r";\s*(drop|delete|update|insert|truncate|alter|create|exec|shutdown)\b",
            re.IGNORECASE
        )
    },

    {
        "name": "Comment Evasion",
        "severity": "medium",
        "weight": 25,
        "pattern": re.compile(
            r"(--\s|#|/\*).*",
            re.IGNORECASE
        )
    },

    {
        "name": "Time Based Blind",
        "severity": "critical",
        "weight": 55,
        "pattern": re.compile(
            r"\b(sleep|waitfor\s+delay|pg_sleep|benchmark)\s*\(",
            re.IGNORECASE
        )
    },

    {
        "name": "Schema Enumeration",
        "severity": "high",
        "weight": 40,
        "pattern": re.compile(
            r"\b(information_schema|sys\.databases|sysobjects|pg_catalog)\b",
            re.IGNORECASE
        )
    },

    {
        "name": "OOB / RCE",
        "severity": "critical",
        "weight": 60,
        "pattern": re.compile(
            r"\b(xp_cmdshell|load_file|into\s+outfile|into\s+dumpfile)\b",
            re.IGNORECASE
        )
    }
]


# ==========================================
# Rule Engine
# ==========================================

def detect_rules(query):

    score = 0
    indicators = []
    highest_severity = "none"

    severity_rank = {
        "none": 0,
        "low": 1,
        "medium": 2,
        "high": 3,
        "critical": 4
    }

    for rule in RULES:

        match = rule["pattern"].search(query)

        if match:

            score += rule["weight"]

            indicators.append({
                "rule": rule["name"],
                "match": match.group(0)[:80]
            })

            if severity_rank[rule["severity"]] > severity_rank[highest_severity]:
                highest_severity = rule["severity"]

    return score, indicators, highest_severity


# ==========================================
# Hybrid Detection
# ==========================================

def hybrid_detection(query):

    # ---------- ML ----------
    query_vector = vectorizer.transform([query])

    probabilities = model.predict_proba(query_vector)[0]

    ml_probability = probabilities[1] * 100


    # ---------- Rules ----------
    rule_score, indicators, rule_severity = detect_rules(query)


    # ======================================
    # Risk Engine
    # ======================================

    if rule_score >= 35:

        verdict = "Malicious"

        risk_score = max(
            ml_probability,
            min(100, rule_score)
        )

    elif ml_probability >= 80:

        verdict = "Malicious"

        risk_score = ml_probability

    elif ml_probability >= 50:

        verdict = "Suspicious"

        risk_score = ml_probability

    else:

        verdict = "Safe"

        risk_score = ml_probability


    return {
        "query": query,
        "ml_probability": round(ml_probability, 2),
        "rule_score": rule_score,
        "rule_detected": len(indicators) > 0,
        "indicators": indicators,
        "severity": rule_severity,
        "risk_score": round(risk_score, 2),
        "verdict": verdict
    }


# ==========================================
# API Routes
# ==========================================

@app.get("/")
def home():

    return {
        "message": "SQLGuard API is running"
    }


@app.post("/predict")
def predict(request: QueryRequest):

    return hybrid_detection(request.query)