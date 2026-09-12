# CowabungaAI — Agent Handbook

Instructions for AI coding agents working in this repository.
CowabungaAI (formerly LeapfrogAI) is a UDS-Zarf-deployable LLM inference
platform: a Rust OpenAI-compatible API, a React UI, zarf-packaged model
backends, and a GPU k3d cluster runtime.

*Verified against the working deployment: 2026-09-10.*

## Repository Layout

- `rust/crates/api/` — the main API service (Axum, OpenAI-compatible).
  - `rust/crates/api/src/main.rs` — server startup. Wires `LibsqlStorage`
    when `TURSO_URL` is set (remote for `libsql://`/`https://`, local file
    otherwise); falls back to in-memory storage with a hardcoded dev
    `test-key` only when `TURSO_URL` is unset. Non-TLS `http://` URLs fall
    back to in-memory (the client only speaks TLS remotely).
  - `rust/crates/api/src/bin/migrate.rs` — schema migrations binary.
    Reads `TURSO_URL` and optionally `TURSO_DATABASE_PATH`.
  - `rust/crates/repeater/` — minimal gRPC model backend in Rust
    (echo backend) proving the SDK server side; `just dev-repeater`.
- `rust/crates/db/src/libsql.rs` — libSQL client wrapper.
  **Important**: remote mode is used only for `libsql://` or `https://`
  URLs (both TLS); any other scheme (`http://`, `ws://`) falls back to
  `Builder::new_local` (file mode). Plain HTTP sqld endpoints therefore
  cannot be used remotely unless TLS is terminated.
- `rust/crates/cowabunga_sdk/` — shared SDK: gRPC/Python bindings used
  by model backends (embeddings, llama.cpp, whisper, vllm wrappers).
- `packages/` — one zarf package per component, each self-contained:
  - `packages/api/`, `packages/ui/`, `packages/vllm/`,
    `packages/text-embeddings/` (torch, 5.75 GB),
    `packages/text-embeddings-tiny/` (ONNX MiniLM, no torch),
    `packages/llama-cpp-python/`, `packages/whisper/`,
    `packages/turso/` (libSQL server), `packages/k3d-gpu/`.
  - Each has: `Dockerfile`, `zarf.yaml` (+ optional `zarf-config.yaml`
    for create-time sets/flavors), `values/upstream-values.yaml`
    (Helm), sometimes `chart/` ( Helm chart vendored) and `src/`.
- `legacy/cowabunga_sdk/` — source of the SDK wheel image.
- `Makefile` — the authoritative build/deploy flow (`make help`).
- `GPU_DEPLOYMENT_REPORT.md`, `KNOWN_ISSUES.md` — recon notes from the
  first GPU bring-up (some contents are stale; verify against code).

## Build & Deploy (the flow that actually works here)

The build host runs docker = **podman 6.1.1 shim** over a rootful
podman machine VM. Everything is non-root via the world-writable socket:

```bash
# 1. Local registry (required before any image build)
make local-registry                      # registry on localhost:5000

# 2. Images (tag = git short SHA, e.g. 0bf35225)
docker build --platform linux/amd64 \
  --build-arg LOCAL_VERSION=$V --build-arg SDK_REGISTRY=localhost:5000 \
  -t ghcr.io/defenseunicorns/cowabungaai/<component>:$V \
  -f packages/<component>/Dockerfile .
docker push --tls-verify=false localhost:5000/...
```

**Zarf package create + deploy** (works with no internet access on the
deploy target — models are downloaded at `create` time via
`scripts/model_download*.py` and data-injected into `/data/.model`):

```bash
zarf package create <pkg dir> -o . --flavor upstream \
  --set IMAGE_VERSION=$V --confirm
# copy the .tar.zst into the k3d node and deploy from inside the node
zarf package deploy /tmp/<pkg>.tar.zst --confirm
```

**Cluster** (one-time, see `packages/k3d-gpu/`): custom node image
`ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:<tag or :patched2>` with the
k3d entrypoint fix; cluster created, then `zarf init` + package deploys
for turso, tiny-embeddings, api, ui (and llama-cpp-python / vllm).

## Gotchas (verified the hard way — keep these)

1. **Zarf variables must have defaults.** An unset `ZARF_VAR_*` renders
   as the literal `###ZARF_VAR_X###` in Helm values, which evaluates
   truthy — that once silently rendered `uds.dev` Package CRDs that
   fail without UDS/Istio CRDs ("resource mapping not found"). If this
   repo's app is deployed without UDS Studio, the api/ui charts must
   NOT render `uds-package.yaml`/`istio-*` templates.
2. **`write_file`/patch tools refuse templated YAML** — Helm files
   containing `{{ }}` must be edited via Python, not the built-in
   write/patch tools (their linter misparses them).
3. **Always `docker cp` the freshly built package into the node
   before deploy** — a previously copied `/tmp/pkg-*.tar.zst` is NOT
   refreshed automatically; stale packages have caused silent rollbacks
   of fixes (the UI deploy loop lost ~30 min to this).
4. **Half-installed Helm releases**: interrupted deploys leave
   `pending-install` releases in surprise namespaces (e.g. UI in
   `cowabunga` instead of `cowabungaai`). Check with
   `zarf tools helm list -A` before re-deploying; uninstall leftovers.
5. **Migration job env contract** (api + ui charts): `TURSO_URL` must
   be set; if `TURSO_DATABASE_PATH` is set, the migrate binary runs in
   local-file mode (and needs a mounted `/data`). The current deploy
   uses local-file mode on an emptyDir because the bundled turso sqld
   is plain HTTP while the client build only speaks TLS for remote.
6. **Model package layout**: backends read `/data/.model/…`. For
   llama-cpp-python the gguf must be named `model.gguf`; for
   text-embeddings-tiny the ONNX must be `onnx/model.onnx` →
   normalized to `model.onnx`.
7. **GGUF architecture support**: `prism-ml/Ternary-Bonsai-1.7B-gguf`
   declares `general.architecture=qwen3` — needs llama-cpp-python
   >= 0.3.x (qwen3 support, Apr 2025). The repo pinned 0.2.72 and was
   bumped to 0.3.20 for this reason. Do not downgrade blindly.
8. **vLLM image has no GGUF loader** (no gguf entry in
   `QUANTIZATION_METHODS` at the pinned version) — GGUF models go to
   llama-cpp-python, not vLLM.

## Code Style

- Rust: follow workspace conventions (`rust/crates/*`), keep error
  handling explicit; prefer `thiserror`-style variants.
- Python (backends): stdlib + SDK imports, log via `logging`, gRPC
  service classes subclass the SDK base classes (see
  `packages/*/main*.py`).
- TS/React only in the UI: explicit named imports, no `any`,
  camelCase test functions, kebab-case test files.
- Keep `zarf.yaml` variables defaulted; keep chart values valid
  Kubernetes quantities (never `cpu: 0`).

## Environment

- Registry: `localhost:5000` (world-access on the build host).
- In-cluster zarf registry: `127.0.0.1:31711` (from the node).
- Secrets: `turso-auth` (key `token`) in `cowabungaai` and `cowabunga`
  namespaces; dummy `sso-client-uds-cowabunga` (keycloak disabled via
  `PUBLIC_DISABLE_KEYCLOAK`).
- NodePorts: UI on `30080/30081` (node-level; reach patterns documented
  in the podman-machine-k8s skill).
- Model tooling venv for HF downloads: `.venv-modeltools/`
  (python3.12; huggingface_hub + hf_transfer). PEP 668 blocks pip
  system installs — always use this venv.

## Verification Checklist Before Claiming "Deployed"

- `kubectl -n cowabungaai get pods` → all Running/Completed, no
  `CreateContainerError`.
- `kubectl exec deploy/cowabunga-api -c sidecar -- wget -qO- \
  http://cowabunga-api:8080/ready` → `{"ready":true,...}`.
- UI service returns HTTP 200 (`wget`/curl probe through a pod).
- For model services: one real inference round-trip before declaring
  success (embed call for te*, generate for llama-cpp / vllm).
