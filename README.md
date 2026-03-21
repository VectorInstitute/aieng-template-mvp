# GCP Cloud Run vLLM Template

A production-ready template for deploying an LLM-backed application on **Google Cloud Run** using [vLLM](https://docs.vllm.ai) as the inference backend.

The template ships two Cloud Run services:

| Service | Runtime | Purpose |
|---------|---------|---------|
| **vLLM GPU service** | NVIDIA L4 GPU | OpenAI-compatible inference (`/v1`) |
| **Demo CPU service** | CPU (nginx + FastAPI) | Web UI + API proxy |

The UI is served by nginx instantly on cold start; the FastAPI/uvicorn process loads in the background and handles API calls once ready. The frontend auto-retries 502 responses during the warm-up window.

---

## Architecture

```
User
 │
 ▼
Cloud Run CPU service (port 8080)
 ├── nginx — serves /  and /static/ instantly from filesystem
 └── uvicorn (port 8000, background) — /health  /generate  /generate/stream
                          │
                          │  OpenAI-compatible HTTP
                          ▼
              Cloud Run GPU service (vLLM, port 8080)
                          │
                          │  GCS FUSE volume
                          ▼
               GCS bucket (cached model weights)
```

---

## Prerequisites

- **GCP project** with billing enabled
- `gcloud` CLI authenticated (`gcloud auth login`)
- **Artifact Registry** repository for Docker images
- **Workload Identity Federation** pool and provider for keyless GitHub Actions auth
- A **GCS bucket** for caching model weights (optional but strongly recommended)
- GPU quota for NVIDIA L4 in your chosen region (request via IAM & Admin → Quotas)

---

## Quick Start

### 1. Fork / clone this repository

```bash
git clone https://github.com/your-org/your-repo
cd your-repo
```

### 2. Configure GitHub Actions secrets & variables

In your repository's **Settings → Secrets and variables → Actions**, set:

**Secrets**
| Name | Value |
|------|-------|
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | Full WIF provider resource name |
| `GCP_SERVICE_ACCOUNT` | Service account email used for deployments |
| `HF_TOKEN` | HuggingFace token (required for gated models like Llama 3) |

**Variables** (or edit defaults at the top of `.github/workflows/deploy.yml`)
| Name | Example |
|------|---------|
| `GCP_PROJECT_ID` | `my-gcp-project` |
| `GCP_REGION` | `us-east4` |
| `ARTIFACT_REGISTRY_REPO` | `us-east4-docker.pkg.dev/my-project/my-repo` |
| `VLLM_SERVICE_NAME` | `my-vllm-service` |
| `DEMO_SERVICE_NAME` | `my-demo-service` |
| `GCS_BUCKET` | `gs://my-model-cache` |
| `VLLM_MODEL_NAME` | `my-model` |

### 3. Customise the model

Edit `Dockerfile.vllm` — change the model ID and serving flags:

```dockerfile
CMD [ \
    "meta-llama/Llama-3.1-8B-Instruct", \   # ← HuggingFace model ID
    "--served-model-name", "my-model", \     # ← must match VLLM_MODEL_NAME
    "--max-model-len", "8192", \
    "--max-num-seqs", "16", \
    "--dtype", "bfloat16" \
]
```

The `--served-model-name` value must match the `VLLM_MODEL_NAME` variable and the `VLLM_MODEL_NAME` env var set on the demo service.

### 4. Customise the demo app

Replace the `/generate` and `/generate/stream` endpoint logic in `app/api.py` with your use case — parse model output, apply post-processing, add system prompts, etc.

The frontend files live in `app/demo/`:
- `templates/index.html` — page structure
- `static/style.css` — styling
- `static/script.js` — SSE streaming + cold-start auto-retry

### 5. Deploy

Push to `main` to trigger the full deploy workflow, or run it manually from **Actions → Deploy to Cloud Run**.

The workflow:
1. Builds and pushes both Docker images to Artifact Registry
2. Deploys the vLLM GPU service (waits for health check)
3. Passes the vLLM service URL to the demo service as `VLLM_BASE_URL`
4. Deploys the demo CPU service

---

## Local Development

```bash
# Install dependencies
uv sync --dev

# Run the API server (requires VLLM_BASE_URL to point at a running vLLM instance)
VLLM_BASE_URL=http://localhost:9999/v1 uv run uvicorn app.api:app --reload --port 8000

# Lint & format
uv run ruff check . --fix
uv run ruff format .

# Type check
uv run mypy app/

# Tests
uv run pytest
```

---

## Infrastructure Setup Reference

### Workload Identity Federation (keyless auth for GitHub Actions)

```bash
PROJECT_ID=my-gcp-project
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
REPO=your-org/your-repo

# Create the WIF pool
gcloud iam workload-identity-pools create github-pool \
  --project=$PROJECT_ID --location=global \
  --display-name="GitHub Actions pool"

# Create the provider
gcloud iam workload-identity-pools providers create-oidc github-provider \
  --project=$PROJECT_ID --location=global \
  --workload-identity-pool=github-pool \
  --display-name="GitHub provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"

# Allow your repo to impersonate the deploy service account
SA_EMAIL=deploy-sa@$PROJECT_ID.iam.gserviceaccount.com
gcloud iam service-accounts add-iam-policy-binding $SA_EMAIL \
  --project=$PROJECT_ID \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/$REPO"
```

Add these GitHub Actions secrets:
- `GCP_WORKLOAD_IDENTITY_PROVIDER`: `projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider`
- `GCP_SERVICE_ACCOUNT`: `$SA_EMAIL`

> **Reusing an existing WIF pool?** If the pool and service account already exist (e.g. from another repo in the same GCP project), skip the creation steps above and just grant the new repo permission to impersonate the SA:
> ```bash
> gcloud iam service-accounts add-iam-policy-binding $SA_EMAIL \
>   --project=$PROJECT_ID \
>   --role=roles/iam.workloadIdentityUser \
>   --member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/YOUR_ORG/YOUR_REPO"
> ```

### Required IAM roles for the deploy service account

```bash
for ROLE in \
  roles/run.admin \
  roles/artifactregistry.writer \
  roles/iam.serviceAccountUser \
  roles/storage.objectViewer; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" --role=$ROLE
done
```

### GCS bucket for model weight caching

```bash
gcloud storage buckets create gs://my-model-cache \
  --project=$PROJECT_ID --location=US-EAST4

# Allow the Cloud Run GPU service's runtime SA to read/write
gcloud storage buckets add-iam-policy-binding gs://my-model-cache \
  --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role=roles/storage.objectAdmin
```

On first deploy, vLLM downloads weights from HuggingFace into the bucket. Subsequent cold starts read from GCS (~10s) instead of HuggingFace (~5-15min for 8B models).

---

## Key Design Decisions

### Why nginx in front of uvicorn?

Cloud Run performs a TCP health check against port 8080. If the check passes before Python finishes importing heavy ML libraries (~20-30s), the container enters "serving" mode and the CPU is throttled between requests — starving the background import process and turning a 30s startup into 2+ minutes.

nginx answers the TCP probe in <1s and serves the static UI immediately. The `--no-cpu-throttling` flag (set in the deploy workflow) ensures the background Python process always has CPU.

### Why `--no-cpu-throttling`?

Without it, Cloud Run throttles CPU to near-zero between requests. After nginx answers the health check, the Python background process receives almost no CPU time until the first real request arrives — by which point the user has already seen a 502.

### SSE streaming

The `/generate/stream` endpoint uses Server-Sent Events. nginx is configured with `proxy_buffering off` and `proxy_cache off` to prevent it from buffering the stream. The frontend accumulates tokens into the output box as they arrive.

---

## File Reference

```
.
├── app/
│   ├── __init__.py
│   ├── api.py                  # FastAPI app — customise /generate logic here
│   └── demo/
│       ├── templates/
│       │   └── index.html      # Demo UI
│       └── static/
│           ├── style.css
│           └── script.js       # SSE client + cold-start retry
├── tests/
│   └── test_api.py
├── .github/
│   └── workflows/
│       ├── deploy.yml          # Two-service Cloud Run deploy
│       └── ci.yml              # Lint / type-check / test
├── Dockerfile                  # Demo CPU service
├── Dockerfile.vllm             # vLLM GPU service
├── nginx.conf                  # nginx config (serves UI, proxies API)
├── entrypoint.sh               # Starts uvicorn in background, then nginx
├── pyproject.toml
└── .env.example
```
