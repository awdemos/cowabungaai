import fnmatch
import os
from huggingface_hub import snapshot_download
from config import DownloadConfig

REPO_ID = DownloadConfig().download_options.repo_id
REVISION = DownloadConfig().download_options.revision

# Optional allowlist via env, e.g. GGUF_ALLOW="Ternary-Bonsai-1.7B-Q2_0*.gguf"
# (GGUF repos carry every quant; grabbing the whole snapshot wastes GBs.)
ALLOW = os.environ.get("COWABUNGA_MODEL_ALLOW")
IGNORE = None
if ALLOW:
    patterns = [p.strip() for p in ALLOW.split(",") if p.strip()]
    IGNORE = ["*"]
    for p in patterns:
        # snapshot_download ignores are match patterns relative to repo root
        IGNORE.append("!*" + p + "*") if not p.startswith("!") else IGNORE.append(p)

# enable hf_transfer to max-out model download bandwidth
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

print(f"Downloading model from {REPO_ID} at revision {REVISION}...")

snapshot_download(
    repo_id=REPO_ID,
    local_dir=".model",
    revision=REVISION,
    ignore_patterns=IGNORE,
    allow_patterns=None,
)

print("Download complete.")
