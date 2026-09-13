import os
import time

from huggingface_hub import snapshot_download

REPO_ID = os.environ.get("REPO_ID", "hkunlp/instructor-xl")
REVISION = os.environ.get("REVISION", "ce48b213095e647a6c3536364b9fa00daf57f436")

# Respect an externally-set value; default to disabled because hf_transfer
# bypasses the normal HTTP stack and can fail with non-standard HF_ENDPOINT
# or unstable links.
if "HF_HUB_ENABLE_HF_TRANSFER" not in os.environ:
    os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0"

# Retry wrapper because large model downloads occasionally fail mid-transfer
# over flaky network paths.
MAX_RETRIES = 5
last_error = None
for attempt in range(1, MAX_RETRIES + 1):
    try:
        snapshot_download(
            repo_id=REPO_ID,
            local_dir=".model",
            local_dir_use_symlinks=False,
            revision=REVISION,
        )
        break
    except Exception as exc:  # noqa: BLE001
        last_error = exc
        print(f"Model download attempt {attempt}/{MAX_RETRIES} failed: {exc}")
        if attempt < MAX_RETRIES:
            wait = min(2 ** attempt, 60)
            print(f"Retrying in {wait} seconds...")
            time.sleep(wait)
else:
    raise last_error
