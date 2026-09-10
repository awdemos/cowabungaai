import asyncio
import logging
import os
from typing import Any, Dict

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

from cowabunga_sdk import (
    Embedding,
    EmbeddingRequest,
    EmbeddingResponse,
    GrpcContext,
    serve,
)

logging.basicConfig(
    level=os.getenv("COWABUNGA_LOG_LEVEL", logging.INFO),
    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
)
logger = logging.getLogger(__name__)

# Model files arrive via zarf dataInjection into COWABUNGA_MODEL_PATH.
model_dir = os.environ.get("COWABUNGA_MODEL_PATH", ".model")
model_path = os.path.join(model_dir, "model.onnx")
tokenizer_path = os.path.join(model_dir, "tokenizer.json")

if not os.path.exists(model_path):
    raise FileNotFoundError(f"ONNX model not found at {model_path} (_ONNX_MODEL_MISSING)")
if not os.path.exists(tokenizer_path):
    raise FileNotFoundError(f"tokenizer.json not found at {tokenizer_path} (_TOKENIZER_MISSING)")

tokenizer = Tokenizer.from_file(tokenizer_path)

session_options = ort.SessionOptions()
session_options.intra_op_num_threads = int(os.environ.get("COWABUNGA_ORT_THREADS", "2"))
session = ort.InferenceSession(
    model_path, sess_options=session_options, providers=["CPUExecutionProvider"]
)
input_names = {x.name for x in session.get_inputs()}
max_len = int(os.environ.get("COWABUNGA_MAX_SEQ_LEN", "256"))

KV_CACHE: Dict[str, Any] = {}


def _encode_batch(texts):
    encodings = tokenizer.encode_batch(texts)
    input_ids = np.array([e.ids[:max_len] for e in encodings], dtype=np.int64)
    attention = np.array([e.attention_mask[:max_len] for e in encodings], dtype=np.int64)
    feed: Dict[str, np.ndarray] = {"input_ids": input_ids, "attention_mask": attention}
    if "token_type_ids" in input_names:
        feed["token_type_ids"] = np.zeros_like(input_ids, dtype=np.int64)

    output = session.run(None, feed)[0]

    # Mean-pool token embeddings into sentence embeddings (matches
    # sentence-transformers MiniLM pooling). If the export already pooled
    # (output ndim == 2 with last_hidden_state squeezed), this is a no-op
    # normalization.
    if output.ndim == 3:
        mask = attention[:, :, None].astype(np.float32)
        summed = (output * mask).sum(axis=1)
        counts = np.clip(mask.sum(axis=1), 1e-9, None)
        output = summed / counts
    return output


class TinyEmbedding:
    async def CreateEmbedding(self, request: EmbeddingRequest, context: GrpcContext):
        logger.info(
            f"processing CreateEmbedding request: char-length: {len(str(request.inputs))} word-count: {len(str(request.inputs).split())}"
        )

        # Run the CPU-intensive encoding in a separate thread
        vectors = await asyncio.to_thread(_encode_batch, request.inputs)
        embeddings = [Embedding(embedding=vec) for vec in vectors]

        logger.info(
            f"finished processing CreateEmbedding request, created {len(embeddings)} embeddings"
        )
        return EmbeddingResponse(embeddings=embeddings)


if __name__ == "__main__":
    asyncio.run(serve(TinyEmbedding()))
