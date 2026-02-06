# ==========================================
# STAGE 1: Build Frontend (Node.js)
# ==========================================
FROM node:20-alpine as build-frontend

WORKDIR /app/frontend

# 1. Install frontend dependencies
COPY frontend/package*.json ./
RUN npm ci

# 2. Copy source and build
COPY frontend/ ./

ARG VITE_GEMINI_API_KEY
ENV VITE_GEMINI_API_KEY=$VITE_GEMINI_API_KEY

RUN npx vite build

# ==========================================
# STAGE 2: Backend (Python 3.11 Stable)
# ==========================================
# Using 3.11 for maximum compatibility with ML libraries (OpenCV, etc.)
FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# 1. Install system dependencies for OpenCV (gl1, glib2 are required)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 2. Install uv (fast package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 3. Copy dependency files
COPY pyproject.toml uv.lock ./

# 4. Install Python dependencies into system (no venv needed in Docker)
RUN uv sync --frozen --no-dev

# 5. Copy Backend code and AI Agent
COPY backend/ ./backend/
COPY my_agent/ ./my_agent/
# Uncomment if you have a data folder:
# COPY data/ ./data/

# 6. --- MONOLITH MAGIC: COPY FRONTEND BUILD ---
# Copy the 'dist' folder from Stage 1 to where FastAPI expects it
COPY --from=build-frontend /app/frontend/dist ./frontend/dist

# 7. Start Server
ENV PORT=8080
CMD ["uv", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]