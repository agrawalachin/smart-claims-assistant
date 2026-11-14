# WCB Manitoba Claim Intake & Insights Portal — Cloud Architecture

## 1. End-to-End Google Cloud Architecture Diagram

```mermaid
flowchart TB
    %% Styling
    classDef userNode fill:#002F6C,stroke:#005587,stroke-width:2px,color:#FFFFFF,font-weight:bold
    classDef runNode fill:#005587,stroke:#002F6C,stroke-width:2px,color:#FFFFFF
    classDef moduleNode fill:#F8FAFC,stroke:#005587,stroke-width:1.5px,color:#0F172A
    classDef aiNode fill:#007A87,stroke:#005587,stroke-width:2px,color:#FFFFFF,font-weight:bold
    classDef gcsNode fill:#E0F2FE,stroke:#0284C7,stroke-width:2px,color:#0F172A
    classDef cicdNode fill:#F1F5F9,stroke:#64748B,stroke-width:1.5px,color:#334155

    %% Client Layer
    subgraph Client["👤 Client Layer (Web Browser)"]
        Browser["WCB Claim Owner / Adjudicator Browser"]:::userNode
        UI_Left["Left Panel: Single-Doc Upload + Color-Coded JSON + Verification Modal"]:::moduleNode
        UI_Right["Right Panel: Claim Owner Insights + Inline Policy Hyperlinks + Policy Modal"]:::moduleNode
        Browser --> UI_Left
        Browser --> UI_Right
    end

    %% Compute Layer (Cloud Run)
    subgraph Compute["☁️ Serverless Compute Layer — Google Cloud Run (us-central1)"]
        CloudRun["Cloud Run Service: wcb-manitoba-portal\n(https://wcb-manitoba-portal-gpyorjpwra-uc.a.run.app)"]:::runNode

        subgraph AppEngine["Python 3.12 / Streamlit Container (app.py)"]
            AuthGate["🔒 PIN Auth Gate (PORTAL_ACCESS_PIN)"]:::moduleNode
            DocIntake["📤 Multimodal Intake & SHA-256 Deduplication"]:::moduleNode
            PydanticSchema["📐 Pydantic v2 Schema Validation\n(ExtractedClaimDocument & ClaimOwnerInsights)"]:::moduleNode
            PDFRenderer["🖼️ High-Res PDF/Image Page Renderer\n(pypdfium2 + Pillow -> Base64 PNG)"]:::moduleNode
            CitationBridge["🔗 Inline Policy Regex Linkifier & Parent-Realm JS Bridge\n(linkify_wcb_policies + @st.dialog)"]:::moduleNode
        end

        CloudRun --> AuthGate
        AuthGate --> DocIntake
        DocIntake --> PydanticSchema
        DocIntake --> PDFRenderer
        PydanticSchema --> CitationBridge
    end

    %% AI & Reasoning Layer (Vertex AI)
    subgraph VertexAI["🧠 AI & Multimodal Reasoning Layer — Google Cloud Vertex AI (google-genai SDK)"]
        GeminiStage1["Stage 1: Multimodal Vision & OCR Extraction\n(Gemini 4 Argon / 3.8 Flash / 2.5 Pro)\nParses Printed Forms & Cursive Handwriting (Box 8 & Box 25)"]:::aiNode
        GeminiStage2["Stage 2: Policy-Grounded Adjudication & Clinical Synthesis\nGenerates Risk Severity, RTW Plan, Schedule A Rx Limits & Policy Citations"]:::aiNode
        GeminiStage1 -->|"Validated Clean JSON"| GeminiStage2
    end

    %% Storage Layer (Google Cloud Storage)
    subgraph Storage["🗄️ Storage & Document Grounding Layer — Google Cloud Storage (GCS)"]
        ClaimsBucket[("GCS Bucket: Uploaded Claim Documents\ngs://wcb-manitoba-claims-newproject-496103\nPath: claims/{YYYYMMDD}/{sha256}_{filename}")]:::gcsNode
        PoliciesBucket[("GCS Bucket: Official WCB Policy PDFs\ngs://newproject-496103-wcb-policies\n• Policy 44.10.20.10.pdf (Pre-existing Conditions)\n• Policy 44.10.20.60.pdf (Recurrences)\n• Policy 44.120.10.pdf (Medical Aid Schedules A-G)")]:::gcsNode
        LocalFallback[("Container Local Fallback Cache\n/app/policies/*.pdf + @st.cache_data")]:::moduleNode
    end

    %% CI/CD Build & Deployment Pipeline
    subgraph CICD["🚀 Container Build & Deployment Pipeline (GCP Project: newproject-496103)"]
        SourceBucket[("GCS Source Staging Bucket\ngs://newproject-496103-source-bucket")]:::cicdNode
        CloudBuild["Google Cloud Build\n(Docker Multi-Layer Build)"]:::cicdNode
        ArtifactReg[("Artifact Registry (Docker Repo)\nus-central1-docker.pkg.dev/newproject-496103/\nmcp-cloud-run-deployments/wcb-manitoba-portal")]:::cicdNode
        SourceBucket --> CloudBuild --> ArtifactReg -->|"Deploy Revision"| CloudRun
    end

    %% Connections Across Layers
    UI_Left <-->|"HTTPS / WebSocket (Port 8080)"| CloudRun
    UI_Right <-->|"HTTPS / WebSocket (Port 8080)"| CloudRun

    DocIntake -->|"1. Archive Raw Claim Document\n(upload_document_to_gcs)"| ClaimsBucket
    ClaimsBucket -->|"2. Fetch Active Claim Bytes for Pop-Up Verification\n(fetch_document_from_gcs)"| PDFRenderer

    DocIntake -->|"3. Send Raw Document Bytes + MimeType + Extraction Schema"| GeminiStage1
    GeminiStage2 -->|"4. Return Structured JSON + Policy Citations"| PydanticSchema

    CitationBridge -->|"5. Fetch Cited Policy PDF (#page=N)\n(load_policy_pdf_bytes)"| PoliciesBucket
    PoliciesBucket -.->|"Hybrid Fallback"| LocalFallback
    PoliciesBucket -->|"6. Render Cited Page & Full Policy PDF"| PDFRenderer
```

---

## 2. Runtime Execution & Pop-Up Verification Sequence

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Claim Owner (Browser)
    participant CR as ☁️ Cloud Run (Streamlit app.py)
    participant GCS_Claims as 🗄️ GCS Claim Bucket
    participant Vertex as 🧠 Vertex AI (Gemini Models)
    participant GCS_Policy as 📜 GCS Policy Bucket

    User->>CR: Enter Access PIN (WCB2026) & Unlock Portal
    CR-->>User: Render Split-Screen Portal (WCB Light Theme & HD Logos)

    User->>CR: Upload Claim Report (PDF / PNG / JPG / TIFF)
    activate CR
    CR->>CR: Compute SHA-256 hash & clear previous session state
    CR->>GCS_Claims: upload_document_to_gcs(file_bytes, claims/{date}/{hash}_{name})
    GCS_Claims-->>CR: Return gs://wcb-manitoba-claims-newproject-496103/...

    CR->>Vertex: Stage 1 — extract_document_to_json_with_gemini(file_bytes, mime_type)
    Vertex-->>CR: Validated ExtractedClaimDocument JSON + Accuracy & Latency Metrics

    CR->>Vertex: Stage 2 — generate_insights_from_json_with_gemini(clean_json)
    Vertex-->>CR: Validated ClaimOwnerInsights (RTW, Formulary, Policy Citations)

    CR->>CR: linkify_wcb_policies() converts inline policy refs to <a class="wcb-policy-link">
    CR-->>User: Render Left Panel (Color-Coded JSON) & Right Panel (Insights + Policy Links)
    deactivate CR

    opt Verify Uploaded Source Document
        User->>CR: Click "🔍 View Uploaded Document for Verification"
        CR->>GCS_Claims: fetch_document_from_gcs(current_doc_gcs_object)
        GCS_Claims-->>CR: Return raw claim document bytes
        CR->>CR: Render pages via pypdfium2/Pillow to high-res PNGs
        CR-->>User: Open @st.dialog Verification Modal (Active Document Only)
    end

    loop Click Any Inline WCB Policy Hyperlink (1st, 2nd, Nth time)
        User->>CR: Click inline link (e.g., "WCB Policy 44.10.20.10" or "Schedule A")
        CR->>GCS_Policy: load_policy_pdf_bytes(policy_id) [Cached + Local Fallback]
        GCS_Policy-->>CR: Official WCB Policy PDF bytes
        CR->>CR: Render cited page (#page=N) first + complete policy document
        CR-->>User: Open @st.dialog Policy Reference Modal (Verbatim Clause + Highlighted Page)
        User->>CR: Close Modal (on_dismiss="rerun" resets dialog state cleanly)
    end
```

---

## 3. Deployed Google Cloud Resource Inventory

| Layer | GCP Service | Resource Name / Identifier | Region / Location | Role in Architecture |
| :--- | :--- | :--- | :--- | :--- |
| **Compute & Web UI** | **Cloud Run** | `wcb-manitoba-portal` (`wcb-manitoba-portal-00009-knm`) | `us-central1` | Hosts the containerized Python 3.12 + Streamlit portal at `https://wcb-manitoba-portal-gpyorjpwra-uc.a.run.app` |
| **AI Extraction & Reasoning** | **Vertex AI (Gemini API)** | `google-genai` SDK (`gemini-4-argon`, `gemini-3.8-flash`, `gemini-2.5-pro`, `gemini-2.5-flash`) | `global` / `us-central1` | Performs Stage 1 Multimodal OCR/JSON extraction and Stage 2 policy-grounded Claim Owner Insights synthesis |
| **Claim Document Storage** | **Cloud Storage (GCS)** | `gs://wcb-manitoba-claims-newproject-496103` | `us-central1` | Archives every uploaded workplace injury report (`claims/{YYYYMMDD}/{sha256}_{filename}`) and serves bytes to the document verification modal |
| **Policy Document Storage** | **Cloud Storage (GCS)** | `gs://newproject-496103-wcb-policies` | `us-central1` | Stores official WCB Manitoba PDFs (`Policy 44.10.20.10.pdf`, `Policy 44.10.20.60.pdf`, `Policy 44.120.10.pdf`) under `policies/` for the citation pop-up viewer |
| **Container Registry** | **Artifact Registry** | `us-central1-docker.pkg.dev/newproject-496103/mcp-cloud-run-deployments/wcb-manitoba-portal` | `us-central1` | Stores versioned and `:latest` Docker container images built by Cloud Build |
| **CI/CD Build Pipeline** | **Cloud Build & GCS** | `gs://newproject-496103-source-bucket` | `us-central1` | Stages application source archives and executes automated container builds (`Dockerfile`) |
