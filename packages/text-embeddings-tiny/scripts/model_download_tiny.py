import os
import time

from huggingface_hub import hf_hub_download

REPO_ID = os.environ.get("REPO_ID", "Xenova/all-MiniLM-L6-v2")
REVISION = os.environ.get("REVISION", "main")

# ONNX file may live at the repo root or under an onnx/ subdirectory.
CANDIDATES = ["model.onnx", "onnx/model.onnx"]

DEST_DIR = ".model"
os.makedirs(DEST_DIR, exist_ok=True)

MAX_RETRIES = 5
last_error = None
for attempt in range(1, MAX_RETRIES + 1):
    try:
        for name in ["tokenizer.json", "config.json", "special_tokens_map.json"]:
            try:
                p = hf_hub_download(
                    repo_id=REPO_ID,
                    filename=name,
                    revision=REVISION,
                    local_dir=DEST_DIR,
                )
                print(f"downloaded {name} -> {p}")
            except Exception as exc:  # noqa: BLE001
                print(f"skipping {name}: {exc}")

        onnx_path = None
        for candidate in CANDIDATES:
            try:
                onnx_path = hf_hub_download(
                    repo_id=REPO_ID,
                    filename=candidate,
                    revision=REVISION,
                    local_dir=DEST_DIR,
                )
                break
            except Exception:  # noqa: PERF203
                continue

        if onnx_path is None:
            raise RuntimeError(f"no ONNX model found in {REPO_ID} at revisions {CANDIDATES}")

        # Normalize to .model/model.onnx for the runtime's fixed path lookup.
        if os.path.basename(onnx_path) != "model.onnx":
            import shutil

            dest = os.path.join(DEST_DIR, "model.onnx")
            shutil.copy2(onnx_path, dest)
            print(f"copied {onnx_path} -> {dest}")

        print("model download complete")
        break
    except Exception as exc:  # noqa: BLE001
        last_error = exc
        print(f"Model download attempt {attempt}/{MAX_RETRIES} failed: {exc}")
        time.sleep(5 * attempt)
else:
    raise SystemExit(f"Failed to download {REPO_ID}: {last_error}")
