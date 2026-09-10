# CowabungaAI — live on k3d `uds` (2026-09-10)

## Stack status (all pods Running/Completed)
| workload | ns | status |
|---|---|---|
| cowabunga-api 2/2 (+migrations job Completed) | cowabungaai | Service :8080, /ready = {ready:true, database:true, models:true} |
| text-embeddings-tiny 1/1 (ONNX MiniLM, 340MB) | cowabungaai | Service :50051 |
| turso (libsql sqld) 1/1 | cowabunga | Service :8080, local-path PVC |
| cowabunga-ui 1/1 (+ui migrations Completed) | cowabunga | Service :3000, HTTP 200 |
| zarf registry | zarf | :31711 seeded |

## Verified end-to-end
- GPU: torch 2.3.0+cu121 matmul on H200, Pod-Succeeded (vllm image, nvidia runtime class)
- API /healthz `/ready` (sidecar wget): ready:true
- UI webpage: HTTP 200 on service
- All images sourced from the in-cluster zarf registry (no host dependency)

## Access (from the build host — cluster lives in the podman-machine VM)
- UI: http://10.89.195.51:30081/ (door container `ui-door`, restore `docker start ui-door`)
- HTTPS (tailnet): https://acl-dgxh200-1.taila1d7c5.ts.net:9445/ (`tailscale serve` -> 127.0.0.1:30081)
- UI NodePort is 30080 on the node IP 10.89.2.5 (reachable only from containers on the k3d network)
- Node IP 10.89.2.5 has no host route; access = podman-published forwarder containers
- `(node) export KUBECONFIG=/etc/rancher/k3s/k3s.yaml` via `docker exec k3d-uds-server-0`
- Logs: /tmp/podman-clogs/*.log (containerd k8s-file driver via docker-proxy.py)

## Remaining work (see KNOWN_ISSUES.md + postmortem in this session log)
1. vLLM zarf package (19GB) deploy — same docker-cp + zarf deploy path; API chat/models wiring then uses real GPU backend.
2. (optional) expose UI/API to the real host: needs gvproxy route or socat relay on the VM bridge (host can reach machine VM only via rootlessport rules — API 44225 cmd currently EOF).
3. RegicideOSArch `cowabunga` branch (separate side task).
