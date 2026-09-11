# packages/llm-stub — TensorZero-backed LLM backend (gRPC :50051)

Dev/deploy-console backend used by the legacy Python API
(`legacy/cowabunga_api`) under the model names `llama-cpp-python` and
`vllm`. Same `cowabunga_sdk` LLM contract as the other backends
(`llfai-cli /app/main.py`, generate/count_tokens, nodeport/service
managed by the API chart), but instead of echoing, `generate()` calls
the TensorZero gateway's OpenAI-compatible streaming endpoint and
yields the real model output in small chunks.

Origin: while wiring the k3d GPU deployment to a real model (see
commit 37b267e9 and PR #1) the legacy API's gRPC path still needed a
backend; this replaces the throwaway echo stub (`llm-stub:0.14.0d`)
without touching the deployed TZ stack.

Gateway plumbing for pods → host TensorZero (k3d + pasta `--no-map-gw`:
pods can only reach the host at `169.254.1.2`, which k8s rejects as a
Service Endpoint). Deployed here as plain k8s objects, not a zarf
package: `tz-bridge-proxy.py` + `Dockerfile.tz-bridge` build the
TCP-proxy image, `tz-bridge-k8s.yaml` creates the `tensorzero-gw`
ClusterIP Service (:3000) and its 1-replica Deployment.

## Note on deployed names

- Live images use short-version tags (`llm-stub:0.14.0e`,
  `llm-stub-tzbridge:latest`); the zarf webhook rewrites to
  `<tag>-zarf-<random>` — remember `ctr tag --force` on the node.

## Env (container)

- `TZ_OPENAI_BASE_URL` (default `http://tensorzero-gw:3000/openai/v1`)
  — in-cluster ClusterIP Service `tensorzero-gw` → TCP-proxy pod → TZ
  gateway on the host (:3000).
- `TZ_API_KEY` — TensorZero API key (inject from a Secret; never bake
  into the image).
- `TZ_MODEL` (default `tensorzero::model_name::glm`).
- `COWABUNGA_CONFIG_FILE=/app/config.yaml`,
  `COWABUNGA_APP=/app/main.py` (set in the Dockerfile).

## Build (matches repo flow)

```bash
docker build --platform linux/amd64 \
  --build-arg LOCAL_VERSION=$V --build-arg SDK_REGISTRY=localhost:5000 \
  -t ghcr.io/defenseunicorns/cowabungaai/llm-stub:$V \
  -f packages/llm-stub/Dockerfile .
```

Note: the SDK wheel dir referenced by the Dockerfile
(`/cowabungaai/src/cowabunga_sdk/build`) is defined by the SDK image,
not this package — no local wheels needed.

## Deploy-verified behavior

- Assistant-path chat (UI → legacy API → gRPC → TZ → GLM) returns real
  model text (verified in-browser 2026-09-10).
- On TZ failure the pod stays alive and streams a `Backend error: …`
  message to the composer.
