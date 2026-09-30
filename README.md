<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=800&size=40&pause=1000&color=2DD4BF&center=true&vCenter=true&repeat=false&width=850&height=90&lines=AI+Scenario+Simulator;Interview+%26+Workplace+Decisions" alt="AI Scenario Simulator" />

**AI Scenario Simulator for Interview & Workplace Decision Making**
**Using Multi-Provider Generative AI & Advanced Prompt Engineering**

<br/>

[![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-3.6%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![Groq](https://img.shields.io/badge/Groq-GPT%20OSS%20120B-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.13.5-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-College%20Project%20Ready-2DD4BF?style=for-the-badge)]()

<br/>

[Report Bug](https://github.com/Aritra-Chats/AI-Scenario-Simulator-for-Interview-Workplace-Decision-Making/issues) · [Request Feature](https://github.com/Aritra-Chats/AI-Scenario-Simulator-for-Interview-Workplace-Decision-Making/issues) · [Star this Repo](https://github.com/Aritra-Chats/AI-Scenario-Simulator-for-Interview-Workplace-Decision-Making)

<br/>

> **"Stop memorizing static interview answers. Start training inside realistic, adaptive workplace simulations."**
> Generate hyper-realistic, role-calibrated interview and workplace decision dilemmas, receive rigorous multi-dimensional scoring across 7 competency dimensions, experience adaptive difficulty progression, and generate executive growth roadmaps — powered by Google Gemini & Groq.

</div>

---

## Table of Contents

| # | Section | Description |
|---|---|---|
| 1 | [The Problem](#the-problem) | Why generic interview preparation fails |
| 2 | [The Solution](#the-solution) | How AI Scenario Simulator solves it |
| 3 | [What Makes This Different](#what-makes-this-different) | Feature comparison & technical distinction |
| 4 | [Demo Video & Status](#demo-video--status) | Walkthrough and deployment status |
| 5 | [Screenshots](#screenshots) | Real app screenshots with details |
| 6 | [Features](#features) | Supported scenario taxonomy & categories |
| 7 | [System Architecture](#system-architecture) | Multi-tier architecture diagram & request flow |
| 8 | [Prompt Engineering Methodology](#prompt-engineering-methodology) | 5 core techniques explained with code |
| 9 | [Tech Stack](#tech-stack) | Technology stack with exact versions |
| 10 | [Project Structure](#project-structure) | Annotated codebase directory map |
| 11 | [Quick Start](#quick-start) | Step-by-step setup in 5 minutes |
| 12 | [API Key Configuration](#api-key-configuration) | Setting up Google Gemini & Groq keys |
| 13 | [Running the App](#running-the-app) | Launch commands and navigation guide |
| 14 | [Limitations](#limitations) | Known constraints |
| 15 | [Future Scope](#future-scope) | Planned enhancements |
| 16 | [License & Author](#license--author) | Licensing terms and developer info |

---

## The Problem

Preparing for high-stakes interviews and complex workplace scenarios is broken, generic, and unhelpful.

Traditional platforms provide static lists of questions ("What is your biggest weakness?", "Explain a time you had a conflict"). Candidates memorize scripted answers that fail the moment an interviewer probes deeper or an actual workplace emergency strikes.

The core problems that existing tools do not solve:

- **Static, Cliché Question Banks:** LeetCode and Glassdoor provide repetitive, static questions. They test memorization rather than situational judgment, executive presence, or crisis communication.
- **No Qualitative, Multi-Dimensional Feedback:** Generic tools either give a binary pass/fail or a vague thumbs-up. They do not evaluate critical workplace competencies like emotional intelligence, trade-off analysis, or clarity.
- **Absence of Consequence-Driven Follow-Ups:** Real workplace decisions trigger immediate stakeholder reactions, unexpected technical complications, and unintended consequences. Static mocks never test a candidate's ability to adapt under pushback.
- **Zero Difficulty Adaptation:** Practicing the same difficulty level leads to complacency or frustration. Traditional platforms lack rule-based adaptive difficulty scaling calibrated to candidate performance.
- **Fragile Vendor Lock-In:** Most AI tools depend on a single proprietary LLM provider with no fallback, causing total application failure during rate limits, outages, or model deprecations.

---

## The Solution

**AI Scenario Simulator** is an advanced Generative AI application that creates dynamic, context-rich interview and workplace decision simulations, evaluates responses across a 7-dimensional rubric, adapts difficulty in real-time, and maintains comprehensive session analytics.

<br/>

**Deep Personalization for Role & Seniority**
The simulator tailors scenarios to your target role (Software Engineer, Product Manager, Data Scientist, DevOps, etc.), experience tier (*Fresher*, *Junior*, *Mid-level*, *Senior*), category, and custom domain skills.

**Realistic Dilemmas — Not Trivia Questions**
Instead of asking "What is database sharding?", the AI places you in an active crisis: *"During a major product launch, a data synchronization race condition is detected that will delay delivery by 5 business days unless a fragile patch is deployed. How do you resolve this with engineering and executive leadership?"*

**Rigorous Multi-Dimensional Evaluation**
Every response is evaluated across **7 core dimensions** on an objective 0–100 integer scale:
- `Overall Score` · `Communication` · `Decision Making` · `Problem Solving` · `Professionalism` · `Relevance` · `Clarity`

**Actionable Strengths, Weaknesses & Benchmark Responses**
The AI extracts concrete strengths, identifies missed nuances, highlights omitted stakeholder perspectives, and generates an **exemplary benchmark model answer** for direct comparison.

**Consequence-Driven Follow-Up Scenarios (Stage 2 Complications)**
The simulator generates intelligent follow-up scenarios that directly test the candidate on the exact weaknesses or blindspots revealed in their previous answer.

**Rule-Based Adaptive Difficulty**
A rolling evaluation engine monitors performance:
- Average score $\ge 75$ $\implies$ Promotes difficulty (`Beginner` $\to$ `Intermediate` $\to$ `Advanced`).
- Average score $< 50$ $\implies$ Adjusts difficulty down to rebuild core fundamentals.

**Holistic Executive Performance Reporting**
After completing 2+ simulations, the platform generates a comprehensive performance report with cumulative averages, recurring blindspots, and a personalized 3-step growth action plan.

**Provider-Agnostic Multi-LLM Architecture**
Seamlessly hot-swap between **Google Gemini** (Gemini 3.6 Flash, 3.5 Flash, 2.5 series) and **Groq** (GPT OSS 120B, Qwen 3.8 27B, LLaMA 3.3 70B) directly from the UI.

---

## What Makes This Different

> Most interview tools test memory. This simulator evaluates judgment, composure, trade-offs, and communication under realistic pressure.

### Feature Comparison

| Capability | This Project | LeetCode / Glassdoor | Generic ChatGPT | Traditional Mock Interview |
|---|:---:|:---:|:---:|:---:|
| Role & Seniority Personalization | **Yes** | No | Partial | Yes |
| Active Workplace Dilemma Simulation | **Yes** | No | No | Partial |
| Multi-Dimensional 7-Criteria Rubric | **Yes** | No | No | No |
| Exemplary Benchmark Model Answer | **Yes** | No | Partial | No |
| Consequence-Driven Stage 2 Follow-Ups | **Yes** | No | No | Partial |
| Automated Adaptive Difficulty Scaling | **Yes** | No | No | No |
| Multi-Session Performance Analytics | **Yes** | No | No | No |
| Hot-Swappable Multi-LLM Support | **Yes (Gemini + Groq)** | N/A | No | N/A |
| Validated Machine-Parseable JSON Schema | **Yes** | N/A | No | N/A |
| 100% Free & Open Source | **Yes** | No | No | No |

### What Makes This Technically Distinct

- **Common LLM Abstraction Layer (`call_llm`)** — A single unified interface routes requests to Google Gemini or Groq without leaking vendor-specific SDK logic into application engines.
- **4-Layer JSON Reliability & Auto-Repair Pipeline** — Strips markdown fences, cleans trailing commas, isolates outermost JSON boundaries, and validates against Pydantic schemas with automatic single-retry recovery.
- **Rule-Based Adaptive Progression** — Zero black-box ML models; transparent rolling threshold rules ensure reproducible difficulty adaptation.
- **Consequence Chaining** — Evaluator weakness tags are automatically synthesized and injected into subsequent prompt cycles to simulate realistic workplace pushback.
- **Strict Score Clamping & Pydantic Validation** — Bounded integer validation ($0 \le score \le 100$) guarantees mathematical consistency in all charts and reports.

---

## Demo Video & Status

> All screenshots and workflows shown below reflect the live running application on `localhost:8501`.

### Deployment Status

| Environment | Status | Details |
|---|---|---|
| **Local Development** | **Active & Running** | `http://localhost:8501` |
| **Streamlit Community Cloud** | Deployment-Ready | Standard entrypoint in `app.py` |
| **Docker Container** | Planned | Future Scope |

---

## Screenshots

### 1. Main Simulation Workspace & Configuration
![AI Scenario Simulator — Workspace](assets/screenshots/workspace.png)

*The main simulation interface showing the 5-KPI active configuration bar, model selector, scenario details card, key considerations, and immediate challenge callout.*

**Technical Highlights:**
- Streamlit wide layout with responsive `st.columns()` and `st.metric()` status indicators.
- Dynamic sidebar synchronized with `st.session_state` and real-time model switching.
- Dedicated `⚡ Test API Connection` diagnostic tool for instant credentials verification.

---

### 2. User Response & Input Validation
![AI Scenario Simulator — Response View](assets/screenshots/response_view.png)

*The candidate input workspace featuring real-time character counting, length threshold checks, and submit locking.*

**Technical Highlights:**
- Custom validation via `utils/validators.py` requiring meaningful response length ($\ge 40$ chars).
- Automatic state locking once submitted to prevent race conditions during evaluation.

---

### 3. Multi-Dimensional Scorecard & Feedback
![AI Scenario Simulator — Evaluation](assets/screenshots/evaluation.png)

*The comprehensive evaluation report showing overall score metric, 6 dimension progress bars, strengths/weaknesses split, detailed narrative feedback, and expandable model answer.*

**Technical Highlights:**
- Multi-dimensional integer scoring ($0 \le score \le 100$) across 7 dimensions.
- Expandable `🌟 View Ideal / Exemplary Response` for benchmark comparison.
- Dual action triggers: `⚡ Generate Follow-Up Scenario` and `🎯 Next Scenario (Adaptive)`.

---

### 4. Cumulative Performance Report & Analytics
![AI Scenario Simulator — Report](assets/screenshots/report.png)

*The executive synthesis view displaying cumulative averages, recurring blindspots, and personalized development recommendations.*

**Technical Highlights:**
- Aggregates multi-session history with rolling averages and extreme dimension detection.
- Provides role-tailored action items and recommended scenario practice categories.

---

## Features

### Supported Scenario Taxonomy

| Scenario Type | Category | Core Focus & Dilemma |
|---|---|---|
| **Interview** | Technical interview | Architecture, trade-offs, debugging, scalability |
| **Interview** | HR interview | Cultural fit, motivation, expectations, teamwork |
| **Interview** | Behavioral interview | Past performance, STAR framework, conflict resolution |
| **Interview** | Leadership interview | Vision, delegation, organizational alignment |
| **Interview** | Situational interview | Hypothetical high-stakes operational crises |
| **Workplace** | Team conflict | Interpersonal friction, cross-functional disputes |
| **Workplace** | Missed deadline | Delivery slippage, stakeholder recovery, scoping |
| **Workplace** | Difficult teammate | Toxic behavior, uncooperative peers, accountability |
| **Workplace** | Client communication | Escalated clients, contract pushback, transparency |
| **Workplace** | Leadership decision | Resource allocation, priority calls under ambiguity |
| **Workplace** | Ethical dilemma | Compliance, data safety, cutting corners |
| **Workplace** | Time management | Competing high-priority demands, burnout prevention |
| **Workplace** | Project failure | Postmortem analysis, outage recovery, blame-free triage |
| **Workplace** | Workplace communication | Announcing changes, organizational messaging |

---

## System Architecture

The application follows a clean, decoupled **Layered Architecture**. The presentation layer never interacts directly with third-party LLM SDKs; all calls flow through a unified service abstraction.

```
+=================================================================+
|                       PRESENTATION LAYER                        |
|                                                                 |
|   Streamlit Web Interface (app.py)                              |
|   ├── ui/sidebar.py           (Provider & Profile Configuration)|
|   ├── ui/scenario_view.py     (Dilemma & Challenge Display)     |
|   ├── ui/response_view.py     (Response Input & Validation)     |
|   ├── ui/evaluation_view.py   (Scorecard & Feedback Metrics)    |
|   ├── ui/history_view.py      (Session Chronological Timeline)  |
|   └── ui/report_view.py       (Executive Analytics & Roadmap)   |
+================================+================================+
                                 |
                                 v
+=================================================================+
|                      BUSINESS LOGIC LAYER                       |
|                                                                 |
|   engines/scenario_engine.py    ── Generation, Retries, Fallbacks|
|   engines/evaluation_engine.py  ── 7-Dimension Rubric Scoring   |
|   engines/difficulty_engine.py  ── Rule-Based Adaptive Difficulty|
|   engines/history_engine.py     ── Session Memory & Aggregations|
|   engines/report_engine.py      ── Multi-Session Synthesis      |
+================================+================================+
                                 |
                                 v
+=================================================================+
|                      PROMPT & DATA LAYER                        |
|                                                                 |
|   prompts/scenario_prompts.py   ── Anti-Cliché Persona Templates |
|   prompts/evaluation_prompts.py ── Multi-Dimensional Rubric     |
|   prompts/followup_prompts.py   ── Consequence Chaining         |
|   prompts/report_prompts.py     ── Growth Synthesis Prompts     |
|   models/scenario_model.py      ── Pydantic Scenario Schema     |
|   models/evaluation_model.py    ── Pydantic Evaluation Schema   |
|   models/user_profile_model.py  ── Pydantic Profile Schema      |
+================================+================================+
                                 |
                                 v
+=================================================================+
|                    COMMON LLM ABSTRACTION                       |
|                                                                 |
|   llm/llm_client.py             ── call_llm() & Diagnostics    |
|   utils/json_parser.py          ── 4-Layer Auto-Repair Pipeline |
|   utils/error_handler.py        ── LLMError Unified Hierarchy   |
|   utils/validators.py           ── Input & Bounds Enforcement   |
+=================+=============================+=================+
                  |                             |
                  v                             v
+=================================+  +============================+
|        GOOGLE GEMINI API        |  |          GROQ API          |
|  llm/gemini_provider.py         |  |  llm/groq_provider.py      |
|  ├── Gemini 3.6 Flash (Default) |  |  ├── GPT OSS 120B (Default)|
|  ├── Gemini 3.5 Flash           |  |  ├── GPT OSS 20B           |
|  └── Gemini 2.5 Series          |  |  └── LLaMA 3.3 / Qwen 3.8  |
+=================================+  +============================+
```

### Request Flow — Complete Simulation Lifecycle

```
User Configures Profile & Provider
        |
        v
engines.scenario_engine.generate_scenario()
   -> Checks history for Adaptive Difficulty upgrade/downgrade
   -> prompts.scenario_prompts.build_scenario_prompt()
   -> llm.llm_client.call_llm()
   -> utils.json_parser.extract_json() (auto-repair on parse failure)
        |
        v
User Reads Scenario & Enters Response
        |
        v
utils.validators.validate_user_response()
   -> Checks minimum length (>= 40 chars)
        |
        v
engines.evaluation_engine.evaluate_response()
   -> prompts.evaluation_prompts.build_evaluation_prompt()
   -> llm.llm_client.call_llm()
   -> JSON parse & score clamping (0-100)
   -> Stored in st.session_state.history
        |
        v
User Chooses Next Step:
   ├── "Generate Follow-Up" ──> prompts.followup_prompts (targets weak spots)
   └── "Next Scenario"      ──> Adaptive difficulty applied automatically
        |
        v (After 2+ sessions)
engines.report_engine.generate_performance_report()
   -> Renders executive synthesis & personalized growth roadmap
```

---

## Prompt Engineering Methodology

The prompt architecture is the core academic contribution of this project. Five distinct prompt engineering techniques are implemented across the codebase:

### Technique 1 — Role & Persona Prompting
**Implementation:** [`prompts/scenario_prompts.py`](file:///d:/AI%20Scenario%20Simulator%20for%20Interview%20&%20Workplace%20Decision%20Making/prompts/scenario_prompts.py)
```python
"You are an elite Executive Interviewer, Organizational Psychologist, and Workplace Simulation Designer. "
"Your role is to craft deeply realistic, immersive, and nuanced workplace or interview scenarios "
"tailored precisely to a candidate's specific job role, experience level, scenario category, and difficulty."
```
*Why it works:* Establishing an expert identity steers the model away from casual assistant behaviors, inducing authoritative, industry-accurate framing.

---

### Technique 2 — Anti-Cliché & Dilemma Directives
**Implementation:** [`prompts/scenario_prompts.py`](file:///d:/AI%20Scenario%20Simulator%20for%20Interview%20&%20Workplace%20Decision%20Making/prompts/scenario_prompts.py)
```python
"CORE DIRECTIVES:
1. Realism: Create authentic situations with competing priorities, realistic team dynamics, or technical hurdles.
2. No Generic Questions: Do NOT ask standard cliché questions like 'tell me about a time you failed' or 'what is polymorphism'. "
"Instead, frame an active dilemma or technical hurdle where the user must take ownership, make decisions, or communicate under pressure."
```
*Why it works:* Negative constraints prevent LLMs from lapsing into generic interview trivia, forcing the generation of active situational tension.

---

### Technique 3 — Structured JSON via Embedded Contract Schema
**Implementation:** [`prompts/evaluation_prompts.py`](file:///d:/AI%20Scenario%20Simulator%20for%20Interview%20&%20Workplace%20Decision%20Making/prompts/evaluation_prompts.py)
```python
"OUTPUT REQUIREMENTS:
Produce a single JSON object with the following schema:
{
  'overall_score': 0-100 (integer composite score),
  'communication': 0-100,
  'decision_making': 0-100,
  'problem_solving': 0-100,
  'professionalism': 0-100,
  'relevance': 0-100,
  'clarity': 0-100,
  'strengths': [...],
  'weaknesses': [...],
  'feedback': '...',
  'ideal_response': '...',
  'missing_points': [...],
  'improvement_suggestions': [...]
}"
```
*Why it works:* Defining the exact keys, types, and value bounds acts as a contract, enabling reliable zero-shot serialization without proprietary vendor flags.

---

### Technique 4 — Consequence Chaining for Follow-Up Complications
**Implementation:** [`prompts/followup_prompts.py`](file:///d:/AI%20Scenario%20Simulator%20for%20Interview%20&%20Workplace%20Decision%20Making/prompts/followup_prompts.py)
```python
"PREVIOUS EVALUATION (AREAS TO TARGET):
- Weaknesses identified: {weaknesses_str}
- Critical considerations omitted: {missing_str}

DIRECTIVE: Generate a Stage 2 complication that naturally evolves from their previous answer "
"and specifically tests them on the blindspots or omissions identified above."
```
*Why it works:* Chaining the evaluation output directly into the next prompt creates dynamic, adaptive narrative continuity.

---

### Technique 5 — Calibration Rubrics & Constraint Injection
**Implementation:** [`prompts/evaluation_prompts.py`](file:///d:/AI%20Scenario%20Simulator%20for%20Interview%20&%20Workplace%20Decision%20Making/prompts/evaluation_prompts.py)
```python
"EVALUATION STANDARDS:
- 90-100: Exceptional, executive-level nuance, anticipates second-order consequences.
- 75-89: Strong, competent, practical, and well-reasoned.
- 55-74: Adequate, but lacks depth, missed key trade-offs, or somewhat generic.
- 0-54: Weak, inappropriate, evasive, or failed to address the core dilemma."
```
*Why it works:* Providing explicit anchor definitions prevents score inflation and establishes consistent grading across models.

---

### JSON Reliability & Auto-Repair Pipeline

A 4-step sanitization pipeline in [`utils/json_parser.py`](file:///d:/AI%20Scenario%20Simulator%20for%20Interview%20&%20Workplace%20Decision%20Making/utils/json_parser.py) ensures raw LLM outputs parse reliably:

```
Raw Model Output
       |
       v
Step 1: Direct JSON Parse Attempt (json.loads)
       | (on failure)
       v
Step 2: Regex Code Fence Stripping (```json ... ``` and ``` ... ```)
       | (on failure)
       v
Step 3: Outermost Bracket Isolation (text.find('{') to text.rfind('}'))
       | (on failure)
       v
Step 4: Trailing Comma Auto-Repair (re.sub for invalid trailing commas)
       | (on failure)
       v
Step 5: Engine-Level Single Retry with Reinforced JSON Instruction
       | (on final failure)
       v
Step 6: Graceful Calibrated Fallback (Zero Crash Guarantee)
```

---

## Tech Stack

### Frontend & UI
| Technology | Version | Purpose |
|---|---|---|
| **Streamlit** | `1.64.0` | Reactive web framework, multi-tab routing, session state |
| **Python** | `3.10.8+` | Core programming language |

### AI & LLM Providers
| Provider / SDK | Version / Model | Role |
|---|---|---|
| **Google Gemini API** | `google-generativeai 0.8.6` | Primary LLM Provider (`Gemini 3.6 Flash`, `Gemini 3.5 Flash`) |
| **Groq API** | `groq 1.7.0` | High-Speed LLM Provider (`GPT OSS 120B`, `Qwen 3.8 27B`, `LLaMA 3.3`) |
| **Prompt Engineering** | Custom | Role, Anti-Cliché, Embedded Schema, Consequence Chaining |

### Data Modeling & Architecture
| Package | Version | Role |
|---|---|---|
| **Pydantic** | `2.13.5` | Strict schema definition, score validation, and type safety |
| **python-dotenv** | `1.2.3` | Secure environment variable management (`.env`) |

---

## Project Structure

```
ai-scenario-simulator/
│
├── .env                               ← Local API credentials (never committed)
├── .env.example                       ← Template for API key configuration
├── .gitignore                         ← Excludes .env, .venv/, __pycache__/
├── requirements.txt                   ← Pinned project dependencies
├── app.py                             ← Main Streamlit application entrypoint
│
├── config/                            ← Centralized Configurations
│   ├── __init__.py                    ← Re-exports all settings and model configs
│   ├── settings.py                    ← App constants, 14 categories, dimensions, thresholds
│   ├── gemini_config.py               ← Gemini model registry & key loader
│   └── groq_config.py                 ← Groq model registry & key loader
│
├── llm/                               ← Unified LLM Provider Layer
│   ├── __init__.py                    ← Exposes call_llm & test_provider_connection
│   ├── llm_client.py                  ← Provider-agnostic router & ping test
│   ├── gemini_provider.py             ← Google Gemini API client & error handling
│   └── groq_provider.py               ← Groq API client & error handling
│
├── prompts/                           ← Prompt Engineering Templates
│   ├── __init__.py                    ← Re-exports prompt builders
│   ├── scenario_prompts.py            ← Anti-cliché personalized scenario generation
│   ├── followup_prompts.py            ← Consequence chaining Stage 2 follow-ups
│   ├── evaluation_prompts.py          ← Multi-dimensional 7-criteria scoring rubric
│   ├── analysis_prompts.py            ← Comparative benchmark model answers
│   └── report_prompts.py              ← Holistic multi-session performance report
│
├── engines/                           ← Core Business Logic
│   ├── __init__.py                    ← Re-exports all engines
│   ├── scenario_engine.py             ← Scenario generation, retry recovery, fallbacks
│   ├── evaluation_engine.py           ← Multi-criteria scoring, score bounds, fallbacks
│   ├── difficulty_engine.py           ← Rule-based adaptive difficulty progression
│   ├── history_engine.py              ← Session memory, rolling averages, extremes
│   └── report_engine.py               ← Cumulative analytics & growth roadmaps
│
├── models/                            ← Pydantic Schemas
│   ├── __init__.py                    ← Re-exports schemas
│   ├── user_profile_model.py          ← UserProfile data model
│   ├── scenario_model.py              ← Scenario data model with auto-UUIDs
│   └── evaluation_model.py            ← EvaluationResult model with bounded scores
│
├── ui/                                ← Modular Presentation Components
│   ├── __init__.py                    ← Re-exports UI view functions
│   ├── sidebar.py                     ← Provider switcher, model selector, profile form
│   ├── scenario_view.py               ← Scenario presentation, badges, context cards
│   ├── response_view.py               ← Response text area with live character counter
│   ├── evaluation_view.py             ← Scorecard, progress bars, strengths/weaknesses
│   ├── history_view.py                ← Chronological collapsible session timeline
│   └── report_view.py                 ← Cumulative analytics & personalized roadmap
│
├── utils/                             ← Shared Utilities
│   ├── __init__.py                    ← Re-exports utilities
│   ├── json_parser.py                 ← 4-step JSON extraction & auto-repair pipeline
│   ├── error_handler.py               ← LLMError hierarchy & user-friendly messages
│   └── validators.py                  ← Input validation & response length checks
│
└── test_all.py                        ← Master automated test suite (Days 1–10)
```

---

## Quick Start

### Prerequisites
- **Python 3.10 or higher** installed.
- At least one API key:
  - **Google Gemini API Key** (free at [aistudio.google.com](https://aistudio.google.com/app/apikey))
  - **Groq API Key** (free at [console.groq.com](https://console.groq.com/keys))

### Step 1 — Clone the Repository
```bash
git clone https://github.com/Aritra-Chats/AI-Scenario-Simulator-for-Interview-Workplace-Decision-Making.git
cd AI-Scenario-Simulator-for-Interview-Workplace-Decision-Making
```

### Step 2 — Create & Activate Virtual Environment
**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Configure Environment
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and add your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

---

## API Key Configuration

| Provider | Where to Get Key | Free Tier Availability |
|---|---|---|
| **Google Gemini** | [Google AI Studio](https://aistudio.google.com/app/apikey) | **Yes** (Generous free requests/min) |
| **Groq** | [Groq Console](https://console.groq.com/keys) | **Yes** (Fast free tier available) |

*(Note: The simulator works completely if you provide either key or both keys!)*

---

## Running the App

Start the application:
```powershell
.\.venv\Scripts\streamlit run app.py
```
Open your browser at: **`http://localhost:8501`**

### Running the Test Suite
Verify all components with the master test suite:
```powershell
.\.venv\Scripts\python.exe test_all.py
```

---

## Limitations

- **Text-Based Simulation:** Currently focuses on written scenario formulation and textual communication rather than real-time voice analysis.
- **Session Memory:** Stored in Streamlit `session_state` during the active browser session; resets when the browser tab is refreshed.
- **Third-Party Rate Limits:** Free-tier API keys may encounter rate limits during rapid successive generation cycles (mitigated by automated retry and fallback mechanisms).

---

## Future Scope

- [ ] **Voice Simulation Mode:** Integration of WebRTC audio recording with Speech-to-Text (Whisper) and Text-to-Speech (ElevenLabs/Gemini TTS).
- [ ] **SQLite / PostgreSQL Persistence:** Storing longitudinal user performance and score trends across multiple distinct sessions.
- [ ] **Resume / CV Parsing:** Uploading candidate resumes (PDF) to auto-extract skills, tech stacks, and customize interview scenarios automatically.
- [ ] **Multi-Agent Cross-Examination:** Introducing distinct interviewer personas (e.g., tough technical architect vs empathetic HR lead) in multi-turn rounds.
- [ ] **PDF Export:** One-click generation of branded evaluation reports and interview performance certificates.

---

## License & Author

Distributed under the **MIT License**. See `LICENSE` for more information.

### Author
**Aritra-Chats**
- GitHub: [@Aritra-Chats](https://github.com/Aritra-Chats)
- Email: [aritrathegamer05@gmail.com](mailto:aritrathegamer05@gmail.com)

---

<div align="center">
<b>Built for College Capstone & Engineering Portfolio</b><br/>
<i>If you found this project helpful, please consider giving it a ⭐ on GitHub!</i>
</div>
