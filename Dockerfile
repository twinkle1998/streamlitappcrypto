# ============================================================
# Streamlit App — Render Deployment (Stable + Sydney timezone)
# ============================================================

FROM python:3.11-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=Australia/Sydney

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata curl libgomp1 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app ./app
COPY students ./students
COPY assets ./assets         
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# (Optional) Healthcheck — safer for Render
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8501/ || exit 1

# Run Streamlit (use shell form so $PORT expands properly)
CMD streamlit run app/main.py --server.port=${PORT:-8501} --server.address=0.0.0.0
