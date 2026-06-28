# ── Stage 1: build the Next.js frontend into static files ──
FROM node:20-slim AS frontend-build
WORKDIR /frontend

# Next.js bakes NEXT_PUBLIC_* vars in at build time, so it must be
# passed as a build arg (set this in Railway's Variables tab — Railway
# automatically forwards a matching variable name into ARGs).
ARG NEXT_PUBLIC_CYBERSH_API
ENV NEXT_PUBLIC_CYBERSH_API=$NEXT_PUBLIC_CYBERSH_API

# Copy frontend source (lives in the "frontend/" folder of this repo)
COPY frontend_updated/ai-app-builder-main/package.json ./
RUN npm install -g pnpm && pnpm install

COPY frontend_updated/ai-app-builder-main/ ./
RUN pnpm build
# Output lands in /frontend/out because next.config.mjs has output: 'export'

# ── Stage 2: Python backend + the built frontend ──
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend source (everything at repo root, excluding the frontend/ folder)
COPY auth.py cybersh_api.py cybersh_direct.py ./

# Built frontend static files, served by FastAPI's StaticFiles mount
COPY --from=frontend-build /frontend/out ./out

ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "uvicorn cybersh_api:app --host 0.0.0.0 --port ${PORT}"]
