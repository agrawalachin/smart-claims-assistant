# Google Cloud AI Claims Assistant — Complete Demo Guide (`go/demos`)

> [!IMPORTANT]
> **Live Demo Access (`go/demos` Ready)**
> - **Live Cloud Run URL**: `https://wcb-manitoba-portal-gpyorjpwra-uc.a.run.app`
> - **Portal Access PIN**: `WCB2026`
> - **Sample Claim PDF to Upload**: [Sample_WCB_Claim_Report_C849201.pdf](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/Sample_WCB_Claim_Report_C849201.pdf)
> - **Recorded Walkthrough Video**: [claims_assistant_demo_walkthrough.mp4](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/claims_assistant_demo_walkthrough.mp4)

---

## 1. Executive Pitch & Customer Framing

### Elevator Pitch (30 Seconds)
**Google Cloud AI Claims Assistant** transforms how Workers' Compensation Boards, Public Sector agencies, and Property & Casualty / Health / Disability insurers process complex injury and medical claims. Built on **Vertex AI (Gemini Multimodal Models)**, **Google Cloud Run**, and **Google Cloud Storage**, the solution ingests multi-page medical reports (including cursive physician handwriting), extracts deterministic Pydantic-validated JSON, synthesizes clinical Return-to-Work (RTW) and medication formulary recommendations, and grounds every decision in official policy PDFs—opening the exact cited policy page in an interactive pop-up viewer with zero vector database overhead.

### Target Audience & Industry Verticals
- **Primary Personas**: Chief Claims Officers, VP of Claims Transformation, Public Sector Digital Transformation Leaders, Medical Adjudication Directors, Chief Information / AI Officers.
- **Target Industries**:
  - **Public Sector & Workers' Compensation Boards** (e.g., WCB Manitoba, WSIB, WorkSafeBC, State Workers' Comp Agencies, VA / Disability Agencies)
  - **Insurance** (Health, Disability, Auto Bodily Injury, Property & Casualty, Third-Party Administrators)
  - **Healthcare Payers** (Prior Authorization, Utilization Review, Medical Necessity Auditing)

### Key Customer Pain Points Solved
1. **Unstructured & Handwritten Medical Intake Bottlenecks**: Claim adjudicators spend 30–45 minutes per file manually reading faxed/scanned PDFs, physician notes (Box 8 incident descriptions, Box 25 handwritten prescriptions), and multi-page TIFFs.
2. **Opaque AI "Hallucinations" in Regulated Adjudication**: Claims teams cannot trust black-box summaries without immediate, auditable proof linking back to both the **source claim document** and the **exact regulatory/policy clause**.
3. **Complex Policy & Formulary Compliance**: Adjudicators must cross-reference pre-existing conditions (`Policy 44.10.20.10`), injury recurrences (`Policy 44.10.20.60`), and opioid/medication formulary schedules (`Policy 44.120.10 Schedule A`) under tight statutory SLA timelines.

---

## 2. Pre-Demo Preparation (30 Seconds)

1. Open Chrome to `https://wcb-manitoba-portal-gpyorjpwra-uc.a.run.app`.
2. Download or locate the sample claim file [Sample_WCB_Claim_Report_C849201.pdf](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/Sample_WCB_Claim_Report_C849201.pdf) (or any workplace injury PDF/image) on your desktop for live upload.
3. Have your **Access PIN** ready: `WCB2026`.

---

## 3. Step-by-Step Presenter Click-Track & Talk-Track (5–7 Minutes)

### Step 1: Portal Security Gate & Overview (0:00 – 0:45)
- **What to Do**:
  1. Show the login screen featuring the WCB Manitoba & SAFE Work Manitoba header.
  2. Enter Access PIN `WCB2026` and click **🔓 Unlock Portal**.
- **What to Say**:
  > *"Today we're looking at the Google Cloud AI Claims Assistant, deployed serverlessly on Google Cloud Run and tailored here for the Workers Compensation Board of Manitoba. When a claim owner or adjudicator logs in, they get a unified split-screen workspace designed around two core principles: **multimodal speed** and **100% regulatory auditability**."*

---

### Step 2: Workspace Tour & Gemini Model Selection (0:45 – 1:30)
- **What to Do**:
  1. Point out the **Left Panel** (*Upload Claim Report & Extracted JSON*) and the **Right Panel** (*Claim Owner Insights*).
  2. Click the **Select Google Gemini Model** dropdown on the left (`Gemini 4 Pro (Argon — Experimental)`, `Gemini 3.8 Flash`, `Gemini 2.5 Pro`, `Gemini 2.5 Flash`).
- **What to Say**:
  > *"On the left, adjudicators can choose the right Vertex AI Gemini model for their workload—from ultra-low-latency Gemini Flash models for high-volume triage to Gemini Pro / Argon for complex clinical causation and pre-existing condition analysis. Notice that the portal starts with a reference case, and the upload button is always available at the top."*

---

### Step 3: Live Single-Document Upload & Two-Stage Multimodal Pipeline (1:30 – 2:45)
- **What to Do**:
  1. Click **Browse files** in the upload box and select [Sample_WCB_Claim_Report_C849201.pdf](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/Sample_WCB_Claim_Report_C849201.pdf) (Worker: *Marcus J. Vance*, Claim `#WCB-MB-2026-849201`).
  2. Point out that uploading a new document automatically clears the previous claim state and triggers the animated **AI Multimodal Ingestion & Clinical Summarization in Progress** banner.
- **What to Say**:
  > *"As soon as I upload a new physician report—whether it's a PDF, PNG, JPG, or multi-page faxed TIFF—three things happen automatically:*
  > *1. First, the raw document is hashed and archived directly into a dedicated Google Cloud Storage claim bucket (`gs://wcb-manitoba-claims-newproject-496103`) for compliance.*
  > *2. Second, **Stage 1** sends the document bytes to Vertex AI Gemini with a strict Pydantic schema (`ExtractedClaimDocument`) to extract every worker, employer, diagnosis, ICD-10 code, and prescription field—including cursive handwriting.*
  > *3. Third, **Stage 2** synthesizes that clean JSON against WCB Manitoba's official policies to generate actionable Claim Owner Insights."*

---

### Step 4: Inspecting the Extracted JSON & Source Document Verification Modal (2:45 – 3:45)
- **What to Do**:
  1. Point out the **Document Extraction Performance & Accuracy** metrics and the syntax-highlighted **Structured Claim JSON** box on the left.
  2. Click the **🔍 View Uploaded Document for Verification** button directly above the JSON box.
  3. Scroll through the high-resolution rendered claim document inside the pop-up modal, then close the modal (`✕`).
- **What to Say**:
  > *"On the left, we see the schema-validated JSON output along with extraction accuracy and latency metrics. If a claim owner wants to verify any extracted field—say, the ICD-10 code or handwritten prescription—they simply click **View Uploaded Document for Verification**. This streams the active claim document directly from Google Cloud Storage into a pop-up viewer so the adjudicator never has to leave the screen or switch tabs."*

---

### Step 5: Reviewing Claim Owner Insights & Return-to-Work (RTW) Plan (3:45 – 4:45)
- **What to Do**:
  1. Direct attention to the **Right Panel** (*Claim Owner Insights*).
  2. Walk through the **Executive Summary**, **Risk & Severity KPI badges**, **Primary Diagnosis & Causation**, **Modified Return-to-Work (RTW) Plan**, and **Medication & Opioid Formulary Review**.
- **What to Say**:
  > *"On the right, Gemini translates raw clinical data into an adjudication-ready brief. It flags whether a pre-existing condition—like lumbar spondylosis—was structurally enhanced by the workplace injury, outlines specific functional Return-to-Work restrictions (such as a 10-pound lifting limit), and automatically flags prescribed opioids or medications against WCB's Medical Aid formulary schedules."*

---

### Step 6: Clicking Inline WCB Policy Hyperlinks for Verbatim PDF Verification (4:45 – 6:00)
- **What to Do**:
  1. Point out the underlined blue hyperlinks embedded naturally inside the insight paragraphs (e.g., `WCB Policy 44.10.20.10`, `WCB Policy 44.120.10`, `Schedule A`).
  2. Click on **`WCB Policy 44.10.20.10`** (or **`WCB Policy 44.120.10`**).
  3. Show the **Official WCB Policy Reference Modal** that opens: highlight the **Policy Metadata Banner**, the **Highlighted Verbatim Policy Clause**, and the **Official Policy PDF Page (`#page=N`)** fetched live from Google Cloud Storage (`gs://newproject-496103-wcb-policies`).
  4. Close the modal (`✕`) and click a **second policy link** (e.g., `Schedule A` or `WCB Policy 44.10.20.60`) to demonstrate instant, repeatable multi-policy verification.
- **What to Say**:
  > *"Here is what sets this Claims Assistant apart for regulated industries: every single time an insight references a policy or schedule—like **WCB Policy 44.10.20.10** on Pre-existing Conditions or **Policy 44.120.10 Schedule A** on Opioid Formulary limits—it is rendered as an interactive inline hyperlink.*
  > *When I click the link, the app fetches the official WCB Manitoba policy PDF from Google Cloud Storage, displays the exact verbatim clause that grounded the AI's recommendation, and opens the official PDF right to the cited page number (`#page=N`). And notably, we achieve this **without maintaining a complex vector database**—combining Gemini's long-context policy grounding with deterministic Cloud Storage document retrieval."*

---

## 4. Frequently Asked Questions & Objection Handling

| Question / Objection | Recommended Response |
| :--- | :--- |
| **"Why didn't you use a Vector Database / RAG chunking for the policy PDFs?"** | Official claims adjudication policies are structured legal documents where cross-section context matters (e.g., Definitions in Section 1 governing Schedules A–G in `Policy 44.120.10`). Chunking policies into small vector embeddings often strips critical exceptions. By combining Gemini's long context window with a deterministic Policy Registry (`WCB_POLICY_REGISTRY`) and direct PDF page retrieval from Google Cloud Storage (`gs://newproject-496103-wcb-policies`), we get **zero chunking loss, lower infrastructure cost, and exact `#page=N` visual verification**. |
| **"How does it handle messy cursive handwriting on physician forms?"** | Stage 1 sends the high-resolution document bytes directly to Vertex AI Gemini's native multimodal vision encoder (`Part.from_bytes`) with specialized clinical OCR instructions targeting Box 8 (incident narrative) and Box 25 (prescriptions), avoiding legacy OCR pipeline brittle template rules. |
| **"Can this be adapted to another state agency or private insurer?"** | Yes—in under an hour. Simply upload the customer's policy PDFs to the GCS policy bucket, update `WCB_POLICY_REGISTRY` in `app.py` with their policy numbers/titles, and adjust the Pydantic schemas (`ExtractedClaimDocument` and `ClaimOwnerInsights`) to match their claim form fields. |
| **"How are uploaded claim documents secured?"** | Every uploaded document is transmitted over HTTPS to Cloud Run and stored in a private, project-scoped Google Cloud Storage bucket (`gs://wcb-manitoba-claims-newproject-496103`) using IAM-authenticated service accounts. The UI verification modal only exposes the currently active document in the user's session. |

---

## 5. Re-Deployment & Customization Guide

To deploy this demo into any Google Cloud project:

```bash
# 1. Set your Google Cloud Project & Region
export GCP_PROJECT_ID="your-gcp-project-id"
export GCP_REGION="us-central1"

# 2. Create the Cloud Storage buckets for claims and policies
gcloud storage buckets create gs://wcb-manitoba-claims-${GCP_PROJECT_ID} --location=${GCP_REGION}
gcloud storage buckets create gs://${GCP_PROJECT_ID}-wcb-policies --location=${GCP_REGION}

# 3. Upload the official WCB Policy PDFs
gcloud storage cp "Policy 44.10.20.10.pdf" "Policy 44.10.20.60.pdf" "Policy 44.120.10.pdf" \
  gs://${GCP_PROJECT_ID}-wcb-policies/policies/

# 4. Build & Deploy to Cloud Run
gcloud run deploy wcb-manitoba-portal \
  --source . \
  --region ${GCP_REGION} \
  --allow-unauthenticated \
  --set-env-vars="GCP_PROJECT_ID=${GCP_PROJECT_ID},GCP_REGION=${GCP_REGION},GCS_POLICY_BUCKET=${GCP_PROJECT_ID}-wcb-policies,PORTAL_ACCESS_PIN=WCB2026"
```
