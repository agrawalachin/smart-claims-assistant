# Official lightweight Python runtime for Google Cloud Run
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    STREAMLIT_SERVER_PORT=8080 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_THEME_BASE="light" \
    STREAMLIT_THEME_PRIMARY_COLOR="#005587" \
    STREAMLIT_THEME_BACKGROUND_COLOR="#FFFFFF" \
    STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR="#F4F7FA" \
    STREAMLIT_THEME_TEXT_COLOR="#0F172A" \
    GCP_PROJECT_ID="newproject-496103" \
    GCP_REGION="us-central1" \
    VERTEX_LOCATION="global" \
    GEMINI_MODEL="gemini-4-argon" \
    PORTAL_ACCESS_PIN="WCB2026" \
    GCS_POLICY_BUCKET="newproject-496103-wcb-policies"

WORKDIR /app

# Install system dependencies required by scientific/cloud wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for optimal layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code and Streamlit theme config
COPY . .

# Expose Cloud Run default port
EXPOSE 8080

# Healthcheck for container orchestration
HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health || exit 1

# Run Streamlit bound to Cloud Run's $PORT
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]
