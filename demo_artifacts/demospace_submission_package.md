# `go/demos` (DemoSpace) Submission Package — Google Cloud AI Claims Assistant

This package contains all required assets, recorded media, copy-paste form fields, and supporting materials to publish the **Google Cloud AI Claims Assistant (WCB Manitoba Reference Implementation)** to **`go/demos` (`https://demospace.corp.goog/`)**.

---

## 1. Recorded Demo Walkthrough Video (1080p MP4)

![Google Cloud AI Claims Assistant — Full Live Walkthrough Video (46s, 1920x1080)](/home/achinagrawal/.gemini/antigravity/brain/444a5fa8-3fef-4889-adb5-5a1f7adcae37/claims_assistant_demo_walkthrough.mp4)

- **Video File (Project Folder)**: [claims_assistant_demo_walkthrough.mp4](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/claims_assistant_demo_walkthrough.mp4) (`1920x1080`, H.264 MP4, 46 seconds)
- **What the Video Demonstrates**:
  1. **Title & Value Proposition**: Overview of the Google Cloud AI Claims Assistant.
  2. **Portal Security Gate**: Authenticating into the live Cloud Run portal (`WCB2026`).
  3. **Split-Screen Claims Workspace**: Selecting Vertex AI Gemini models and reviewing the dual-panel adjudication layout.
  4. **Live Claim Upload & Two-Stage AI Processing**: Uploading [Sample_WCB_Claim_Report_C849201.pdf](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/Sample_WCB_Claim_Report_C849201.pdf), archiving to Google Cloud Storage, and extracting Pydantic-validated JSON + clinical insights.
  5. **Uploaded Document Pop-Up Verification**: Clicking **🔍 View Uploaded Document for Verification** to inspect the active claim report streamed from Google Cloud Storage.
  6. **Interactive Policy Citation Pop-Up Viewer**: Clicking inline hyperlinks (`WCB Policy 44.120.10` and `Policy 44.10.20.10`) to open official policy PDFs from Google Cloud Storage directly at the cited page (`#page=N`) with highlighted verbatim clauses.

---

## 2. Visual Asset Carousel (Thumbnail, Screenshots & Architecture Diagram)

````carousel
![DemoSpace Cover Thumbnail (1920x1080)](/home/achinagrawal/.gemini/antigravity/brain/444a5fa8-3fef-4889-adb5-5a1f7adcae37/demo_thumbnail_cover.png)
<!-- slide -->
![Cloud Architecture Diagram (1920x1080)](/home/achinagrawal/.gemini/antigravity/brain/444a5fa8-3fef-4889-adb5-5a1f7adcae37/cloud_architecture_diagram.png)
<!-- slide -->
![Step 1 — Portal Login & Security Gate](/home/achinagrawal/.gemini/antigravity/brain/444a5fa8-3fef-4889-adb5-5a1f7adcae37/demo_1_login.png)
<!-- slide -->
![Step 2 — Split-Screen Claims Assistant Dashboard](/home/achinagrawal/.gemini/antigravity/brain/444a5fa8-3fef-4889-adb5-5a1f7adcae37/demo_2_dashboard.png)
<!-- slide -->
![Step 3 & 4 — Extracted JSON & Policy-Grounded Claim Owner Insights](/home/achinagrawal/.gemini/antigravity/brain/444a5fa8-3fef-4889-adb5-5a1f7adcae37/demo_4_extracted_json_and_insights.png)
<!-- slide -->
![Step 5 — Uploaded Claim Document Verification Pop-Up Modal (Cloud Storage)](/home/achinagrawal/.gemini/antigravity/brain/444a5fa8-3fef-4889-adb5-5a1f7adcae37/demo_5_claim_doc_verification_modal.png)
<!-- slide -->
![Step 6 — Interactive WCB Policy Citation Pop-Up Modal #1 (WCB Policy 44.120.10)](/home/achinagrawal/.gemini/antigravity/brain/444a5fa8-3fef-4889-adb5-5a1f7adcae37/demo_6_policy_citation_modal.png)
<!-- slide -->
![Step 7 — Interactive WCB Policy Citation Pop-Up Modal #2 (Policy 44.10.20.10)](/home/achinagrawal/.gemini/antigravity/brain/444a5fa8-3fef-4889-adb5-5a1f7adcae37/demo_7_second_policy_modal.png)
````

---

## 3. Copy-Paste Fields for the `go/demos` Submission Form

| `go/demos` Form Field | Copy-Paste Value |
| :--- | :--- |
| **Demo Title** | `AI-Powered Claims Assistant: Multimodal Intake, Clinical Adjudication & Verbatim Policy Grounding` |
| **Short Summary / Subtitle** | `Accelerate insurance and workers' compensation claims processing with Vertex AI Gemini multimodal extraction, automated Return-to-Work (RTW) & formulary insights, and zero-vector-DB policy PDF citation pop-ups backed by Google Cloud Storage.` |
| **Live Demo URL** | `https://wcb-manitoba-portal-gpyorjpwra-uc.a.run.app` |
| **Access Instructions / Credentials** | `Enter Portal Access PIN: WCB2026 and click "Unlock Portal". Use the sample claim PDF (Sample_WCB_Claim_Report_C849201.pdf) or any medical/injury claim document to test live upload and extraction.` |
| **Industry / Verticals** | `Public Sector`, `Government`, `Insurance (P&C, Workers' Compensation, Health, Disability)`, `Healthcare & Life Sciences` |
| **Use Case Category** | `Document AI & Multimodal Extraction`, `Claims Processing & Adjudication`, `Regulatory & Policy Grounding`, `Clinical Summarization` |
| **Google Cloud Products Used** | `Vertex AI (Gemini API / google-genai SDK)`, `Cloud Run`, `Cloud Storage (GCS)`, `Cloud Build`, `Artifact Registry` |
| **Supported Models** | `Gemini 4 Pro (Argon)`, `Gemini 3.8 Flash`, `Gemini 2.5 Pro`, `Gemini 2.5 Flash` |
| **GCP Project ID** | `newproject-496103` (`us-central1`) |

### Detailed Demo Description (Copy-Paste into `go/demos` "Overview / Description" Box)
```markdown
### Overview
The **Google Cloud AI Claims Assistant** (showcased with the **Workers Compensation Board of Manitoba** reference implementation) demonstrates an end-to-end, production-grade claims intake and clinical adjudication portal running serverlessly on **Google Cloud Run**, **Vertex AI (Gemini)**, and **Google Cloud Storage**.

### Key Capabilities
1. **Two-Stage Multimodal Extraction & Clinical Synthesis (Vertex AI Gemini)**:
   - **Stage 1 (Multimodal Vision & Cursive OCR)**: Ingests scanned PDFs, PNGs, JPGs, and multi-page TIFFs—accurately transcribing both printed form fields and cursive physician handwriting (e.g., Box 8 incident mechanisms and Box 25 prescriptions) into a strict Pydantic-validated JSON schema (`ExtractedClaimDocument`).
   - **Stage 2 (Policy-Grounded Adjudication Insights)**: Evaluates the extracted clinical data against official Workers' Compensation policies to produce an Executive Summary, Risk Severity assessment, Causation & Pre-Existing Condition analysis, Modified Return-to-Work (RTW) restrictions, and Opioid/Medication Formulary flags (`ClaimOwnerInsights`).
2. **Instant Source Claim Verification Backed by Cloud Storage**:
   - Every uploaded claim document is automatically archived to `gs://wcb-manitoba-claims-newproject-496103`.
   - Clicking **"🔍 View Uploaded Document for Verification"** above the JSON output opens a high-resolution pop-up modal displaying the active processed claim document side-by-side with the extracted data.
3. **Interactive Policy Citation Hyperlinks & `#page=N` PDF Pop-Up Viewer (No Vector Index Required)**:
   - Inline policy mentions inside the AI insights (e.g., `WCB Policy 44.10.20.10`, `WCB Policy 44.10.20.60`, `WCB Policy 44.120.10`, `Schedule A`) are automatically converted into interactive hyperlinks.
   - Clicking any policy hyperlink opens an **Official Policy Reference Modal** displaying the highlighted verbatim policy clause and rendering the exact cited page (`#page=N`) of the official PDF fetched directly from `gs://newproject-496103-wcb-policies`.
```

---

## 4. Complete Artifact File Index (`/home/achinagrawal/wcb-manitoba/demo_artifacts/`)

All files required for your `go/demos` upload are saved in [`/home/achinagrawal/wcb-manitoba/demo_artifacts/`](file:///home/achinagrawal/wcb-manitoba/demo_artifacts):

1. **Recorded Video (MP4)**: [claims_assistant_demo_walkthrough.mp4](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/claims_assistant_demo_walkthrough.mp4)
2. **Presenter Demo Guide & Talk-Track**: [claims_assistant_demo_guide.md](file:///home/achinagrawal/.gemini/antigravity/brain/444a5fa8-3fef-4889-adb5-5a1f7adcae37/claims_assistant_demo_guide.md)
3. **Cloud Architecture Diagram (Markdown + Mermaid)**: [architecture_diagram.md](file:///home/achinagrawal/.gemini/antigravity/brain/444a5fa8-3fef-4889-adb5-5a1f7adcae37/architecture_diagram.md)
4. **Cloud Architecture Diagram (High-Res PNG)**: [cloud_architecture_diagram.png](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/cloud_architecture_diagram.png)
5. **DemoSpace Cover Thumbnail (1920x1080 PNG)**: [demo_thumbnail_cover.png](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/demo_thumbnail_cover.png)
6. **Sample Claim Report PDF (For Live Demo Uploads)**: [Sample_WCB_Claim_Report_C849201.pdf](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/Sample_WCB_Claim_Report_C849201.pdf)
7. **Step-by-Step High-Resolution Screenshots**:
   - [demo_1_login.png](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/demo_1_login.png) — Security PIN Gate
   - [demo_2_dashboard.png](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/demo_2_dashboard.png) — Split-Screen Workspace
   - [demo_4_extracted_json_and_insights.png](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/demo_4_extracted_json_and_insights.png) — Extracted JSON & Policy-Grounded Insights
   - [demo_5_claim_doc_verification_modal.png](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/demo_5_claim_doc_verification_modal.png) — Uploaded Claim Verification Modal
   - [demo_6_policy_citation_modal.png](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/demo_6_policy_citation_modal.png) — Official Policy Citation Modal (`WCB Policy 44.120.10`)
   - [demo_7_second_policy_modal.png](file:///home/achinagrawal/wcb-manitoba/demo_artifacts/demo_7_second_policy_modal.png) — Official Policy Citation Modal (`Policy 44.10.20.10`)
