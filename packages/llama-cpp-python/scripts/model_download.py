import os
from huggingface_hub import hf_hub_download

REPO_ID = os.environ.get("REPO_ID", "")
FILENAME = os.environ.get("FILENAME", "")
REVISION = os.environ.get("REVISION", "main")
CHECKSUM = os.environ.get("SHA256_CHECKSUM", "")
OUTPUT_FILE = os.environ.get("OUTPUT_FILE", ".model/model.gguf")

# Enable hf_transfer to max-out model download bandwidth
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"


def download_model():
    # Validate that required environment variables are provided
    if REPO_ID == "" or FILENAME == "":
        print("Please provide REPO_ID and FILENAME environment variables.")
        return

    # Create .model directory if it doesn't exist
    if not os.path.exists(".model"):
        os.makedirs(".model", exist_ok=True)

    # Check if the model is already downloaded
    if os.path.exists(OUTPUT_FILE) and CHECKSUM != "":
        import hashlib
        with open(OUTPUT_FILE, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        if file_hash == CHECKSUM:
            print("Model already downloaded and verified.")
            return
        else:
            print("Model file exists but checksum mismatch. Redownloading...")

    # Download the model using huggingface_hub
    print(f"Downloading {FILENAME} from {REPO_ID} (revision: {REVISION})...")
    try:
        downloaded_path = hf_hub_download(
            repo_id=REPO_ID,
            filename=FILENAME,
            revision=REVISION,
            local_dir=".model",
            local_dir_use_symlinks=False
        )

        # Rename to expected output file if different
        if downloaded_path != OUTPUT_FILE:
            os.rename(downloaded_path, OUTPUT_FILE)

        print(f"Model downloaded successfully to: {OUTPUT_FILE}")

        # Verify checksum if provided
        if CHECKSUM:
            import hashlib
            with open(OUTPUT_FILE, "rb") as f:
                downloaded_hash = hashlib.sha256(f.read()).hexdigest()
            if downloaded_hash == CHECKSUM:
                print("Model checksum verified successfully.")
            else:
                print(f"Warning: Checksum mismatch. Expected: {CHECKSUM}, Got: {downloaded_hash}")

    except Exception as e:
        print(f"Error downloading model: {e}")
        return


if __name__ == "__main__":
    download_model()
