FROM python:alpine AS base

# ---- Dependencies ----
FROM base AS dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
 
# ---- Release ----
FROM dependencies AS release
WORKDIR /app
COPY route53-ddns.py .
CMD ["python", "-u", "/app/route53-ddns.py"]