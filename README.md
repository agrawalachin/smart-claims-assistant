# AI-Powered Claims Intake & Adjudication Assistant

An end-to-end, serverless **Claims Intake & Clinical Adjudication Copilot** built on **Google Cloud Run**, **Vertex AI (Gemini)**, and **Google Cloud Storage** (showcased with a Workers Compensation Board of Manitoba reference implementation).

It ingests unstructured scanned medical forms—including **cursive physician handwriting**—extracts strict **Pydantic-validated JSON**, evaluates causation, Return-to-Work (RTW) restrictions, and medication/opioid formularies against authoritative policy PDFs, and renders **1-click source & `#page=N` verbatim policy verification modals** with **zero vector database overhead**.

---

## Key Capabilities

- **Stage 1 — Multimodal Extraction & Cursive Handwriting Vision**: Streams scanned PDFs, PNGs, JPGs, and multi-page TIFFs to Vertex AI Gemini (`google-genai` SDK) with strict structured outputs (`ExtractedClaimDocument`) and archives raw files to Google Cloud Storage with SHA-256 deduplication.
- **Stage 2 — 1M-Context Policy Synthesis (Zero Vector DB)**: Co-loads authoritative policy PDFs (`Policy 44.10.20.10`, `Policy 44.10.20.60`, `Policy 44.120.10`) directly from Cloud Storage alongside extracted clinical JSON to produce an Executive Summary, 4-Step Approval Action Plan, Pre-Existing & Recurrence checks, RTW guidance, and Medication/Device formulary reviews (`ClaimOwnerInsights`).
- **1-Click Source & `#page=N` Verbatim Policy Modals**:
  - **Source Claim Viewer**: Streams the active uploaded claim PDF directly from Cloud Storage so Claim Owners verify handwritten PHINs, dates, and clinical notes side-by-side.
  - **Official Policy `#page=N` Viewer**: Converts inline policy references into interactive citations that highlight the verbatim statutory clause and open the official PDF directly at the cited page (`#page=N`).
- **Dynamic Multi-Model Routing**: Supports switching across `Gemini 3.8 Flash` (`gemini-3.8-flash`), `Gemini 4 Pro / Argon` (`gemini-4-argon`), `Gemini 3.1 Pro` (`gemini-3.1-pro-preview`), and `Gemini 3.5 Flash-Lite` (`gemini-3.5-flash-lite`).

---

## Repository Structure

```text
├── app.py                     # Streamlit portal, two-stage Gemini pipeline & PDF modals
├── Dockerfile                 # Production container for Google Cloud Run
├── requirements.txt           # Python dependencies (streamlit, google-genai, google-cloud-storage, pypdfium2, pydantic)
├── .streamlit/config.toml     # UI theme & upload configuration
├── assets/                    # Portal header & brand assets
├── policies/                  # Reference WCB Manitoba policy PDFs (44.10.20.10, 44.10.20.60, 44.120.10)
└── demo_artifacts/            # Sample claim PDFs, .docx Demo Guide, Google-template Slide Deck & walkthrough videos
    ├── Claims_Assistant_Demo_Guide.docx
    ├── WCB_Claims_Assistant_Executive_Deck.pptx
    ├── WCB_Claims_Assistant_Executive_Deck.pdf
    ├── Doctor_First_Report_David_Johnson_CLM-112233.pdf   # Sample #1: Cursive handwritten Form 4036
    └── Sample_WCB_Claim_Report_C849201.pdf                # Sample #2: Lumbar injury + 21-day opioid alert
```

---

## Local Development Quickstart

### 1. Prerequisites
- Python `3.11+`
- A Google Cloud project with the **Vertex AI API** and **Cloud Storage API** enabled (or a Gemini API key)

### 2. Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Authenticate & Configure Environment Variables
```bash
gcloud auth application-default login

export GCP_PROJECT_ID="your-gcp-project-id"
export GCP_REGION="us-central1"
export WCB_GCS_BUCKET="wcb-manitoba-claims-${GCP_PROJECT_ID}"
export GCS_POLICY_BUCKET="${GCP_PROJECT_ID}-wcb-policies"
export PORTAL_ACCESS_PIN="WCB2026"
```

### 4. Run Locally
```bash
streamlit run app.py
```
Open `http://localhost:8501`, enter Access PIN `WCB2026`, and upload either sample report from `demo_artifacts/`.

---

## Deploy to Google Cloud Run

```bash
export GCP_PROJECT_ID="your-gcp-project-id"
export GCP_REGION="us-central1"

# 1. Create Cloud Storage buckets for claim archives and official policies
gcloud storage buckets create gs://wcb-manitoba-claims-${GCP_PROJECT_ID} --location=${GCP_REGION}
gcloud storage buckets create gs://${GCP_PROJECT_ID}-wcb-policies --location=${GCP_REGION}

# 2. Upload official reference policy PDFs
gcloud storage cp policies/*.pdf gs://${GCP_PROJECT_ID}-wcb-policies/policies/

# 3. Build & deploy serverlessly to Cloud Run
gcloud run deploy wcb-manitoba-portal \
  --source . \
  --region ${GCP_REGION} \
  --allow-unauthenticated \
  --set-env-vars="GCP_PROJECT_ID=${GCP_PROJECT_ID},GCP_REGION=${GCP_REGION},WCB_GCS_BUCKET=wcb-manitoba-claims-${GCP_PROJECT_ID},GCS_POLICY_BUCKET=${GCP_PROJECT_ID}-wcb-policies,PORTAL_ACCESS_PIN=WCB2026"
```

---

## Environment Variables Reference

| Variable | Default | Description |
| :--- | :--- | :--- |
| `GCP_PROJECT_ID` | `newproject-496103` | Google Cloud Project ID for Vertex AI & Cloud Storage |
| `GCP_REGION` | `us-central1` | Cloud Run & Cloud Storage region |
| `VERTEX_LOCATION` | `global` | Vertex AI Gemini endpoint location |
| `GEMINI_MODEL` | `gemini-4-argon` | Default selected Gemini model in the portal |
| `WCB_GCS_BUCKET` | `wcb-manitoba-claims-${GCP_PROJECT_ID}` | Private GCS bucket archiving uploaded claim documents |
| `GCS_POLICY_BUCKET` | `${GCP_PROJECT_ID}-wcb-policies` | GCS bucket storing official reference policy PDFs |
| `PORTAL_ACCESS_PIN` | `WCB2026` | Security gate PIN required to unlock the portal |
| `GEMINI_API_KEY` | *(Optional)* | Optional Gemini Developer API key fallback if not using Vertex AI ADC |
