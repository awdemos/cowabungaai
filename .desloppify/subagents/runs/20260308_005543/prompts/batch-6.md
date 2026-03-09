You are a focused subagent reviewer for a single holistic investigation batch.

Repository root: /Users/a/code/cowabungaai
Blind packet: /Users/a/code/cowabungaai/.desloppify/review_packet_blind.json
Batch index: 6
Batch name: abstraction_fitness
Batch rationale: seed files for abstraction_fitness review

DIMENSION TO EVALUATE:

## abstraction_fitness
Python abstraction fitness: favor direct modules, explicit domain APIs, and bounded packages over indirection and generic helper surfaces.
Look for:
- Functions that only forward args/kwargs to another function without policy or translation
- Protocol/base-class abstractions with one concrete implementation and no extension pressure
- Cross-module wrapper chains where calls hop through helper layers before reaching real logic
- Project-wide reliance on generic helper modules instead of bounded domain packages
- Over-broad dict/config/context parameters used as implicit parameter bags
Skip:
- Django/FastAPI/SQLAlchemy framework boundaries that require adapters or dependency hooks
- Wrappers that add retries, metrics, auth checks, caching, or tracing
- Intentional package facades used to stabilize public import paths
- Migration shims with active callers and clear sunset plan

YOUR TASK: Read the code for this batch's dimension. Judge how well the codebase serves a developer from that perspective. The dimension rubric above defines what good looks like. Cite specific observations that explain your judgment.

Mechanical scan evidence — navigation aid, not scoring evidence:
The blind packet contains `holistic_context.scan_evidence` with aggregated signals from all mechanical detectors — including complexity hotspots, error hotspots, signal density index, boundary violations, and systemic patterns. Use these as starting points for where to look beyond the seed files.

Seed files (start here):
- src/leapfrogai_api/backend/helpers.py
- src/leapfrogai_sdk/utils.py
- src/leapfrogai_api/typedef/common.py
- packages/repeater/main.py
- packages/whisper/main.py
- src/leapfrogai_api/typedef/audio/audio_types.py
- packages/vllm/src/main.py
- src/leapfrogai_api/main.py
- src/leapfrogai_api/routers/leapfrogai/models.py
- src/leapfrogai_api/typedef/files/file_types.py
- src/leapfrogai_evals/runners/niah_runner.py
- src/leapfrogai_evals/runners/qa_runner.py
- src/leapfrogai_api/backend/rag/index.py
- src/leapfrogai_api/typedef/runs/run_create_base.py
- src/leapfrogai_api/backend/converters.py
- src/leapfrogai_api/typedef/threads/thread_create.py
- src/leapfrogai_api/typedef/runs/run_create.py
- src/leapfrogai_api/routers/openai/runs_steps.py
- src/leapfrogai_api/typedef/messages/message_types.py
- src/leapfrogai_evals/models/lfai.py
- src/leapfrogai_api/typedef/chat/chat_types.py
- src/leapfrogai_api/backend/composer.py
- src/leapfrogai_api/typedef/assistants/assistant_types.py
- src/leapfrogai_api/routers/openai/files.py
- src/leapfrogai_api/typedef/threads/thread_run_create_params_request.py
- src/leapfrogai_api/backend/rag/query.py
- src/leapfrogai_api/routers/openai/vector_stores.py
- src/leapfrogai_api/data/crud_api_key.py
- src/leapfrogai_api/routers/openai/runs.py
- src/leapfrogai_api/routers/supabase_session.py
- .github/scripts/uds_verification_report.py
- src/leapfrogai_sdk/llm.py
- src/leapfrogai_api/backend/rag/leapfrogai_embeddings.py
- src/leapfrogai_evals/main.py
- src/leapfrogai_api/typedef/assistants/__init__.py
- src/leapfrogai_api/typedef/audio/__init__.py
- src/leapfrogai_api/typedef/chat/__init__.py
- src/leapfrogai_api/typedef/completion/__init__.py
- src/leapfrogai_api/typedef/embeddings/__init__.py
- src/leapfrogai_api/typedef/models/__init__.py
- src/leapfrogai_api/typedef/runs/__init__.py
- src/leapfrogai_api/typedef/threads/__init__.py
- src/leapfrogai_api/typedef/vectorstores/__init__.py
- src/leapfrogai_evals/evals/__init__.py
- src/leapfrogai_evals/metrics/__init__.py
- src/leapfrogai_sdk/__init__.py
- src/leapfrogai_sdk/serve.py

Task requirements:
1. Read the blind packet's `system_prompt` — it contains scoring rules and calibration.
2. Start from the seed files, then freely explore the repository to build your understanding.
3. Keep issues and scoring scoped to this batch's dimension.
4. Respect scope controls: do not include files/directories marked by `exclude`, `suppress`, or non-production zone overrides.
5. Return 0-10 issues for this batch (empty array allowed).
6. For abstraction_fitness, use evidence from `holistic_context.abstractions`:
7. - `delegation_heavy_classes`: classes where most methods forward to an inner object — entries include class_name, delegate_target, sample_methods, and line number.
8. - `facade_modules`: re-export-only modules with high re_export_ratio — entries include samples (re-exported names) and loc.
9. - `typed_dict_violations`: TypedDict fields accessed via .get()/.setdefault()/.pop() — entries include typed_dict_name, violation_type, field, and line number.
10. - `complexity_hotspots`: files where mechanical analysis found extreme parameter counts, deep nesting, or disconnected responsibility clusters.
11. Include `delegation_density`, `definition_directness`, and `type_discipline` alongside existing sub-axes in dimension_notes when evidence supports it.
12. Do not edit repository files.
13. Return ONLY valid JSON, no markdown fences.

Scope enums:
- impact_scope: "local" | "module" | "subsystem" | "codebase"
- fix_scope: "single_edit" | "multi_file_refactor" | "architectural_change"

Output schema:
{
  "batch": "abstraction_fitness",
  "batch_index": 6,
  "assessments": {"<dimension>": <0-100 with one decimal place>},
  "dimension_notes": {
    "<dimension>": {
      "evidence": ["specific code observations"],
      "impact_scope": "local|module|subsystem|codebase",
      "fix_scope": "single_edit|multi_file_refactor|architectural_change",
      "confidence": "high|medium|low",
      "issues_preventing_higher_score": "required when score >85.0",
      "sub_axes": {"abstraction_leverage": 0-100, "indirection_cost": 0-100, "interface_honesty": 0-100, "delegation_density": 0-100, "definition_directness": 0-100, "type_discipline": 0-100}  // required for abstraction_fitness when evidence supports it; all one decimal place
    }
  },
  "issues": [{
    "dimension": "<dimension>",
    "identifier": "short_id",
    "summary": "one-line defect summary",
    "related_files": ["relative/path.py"],
    "evidence": ["specific code observation"],
    "suggestion": "concrete fix recommendation",
    "confidence": "high|medium|low",
    "impact_scope": "local|module|subsystem|codebase",
    "fix_scope": "single_edit|multi_file_refactor|architectural_change",
    "root_cause_cluster": "optional_cluster_name_when_supported_by_history"
  }],
  "retrospective": {
    "root_causes": ["optional: concise root-cause hypotheses"],
    "likely_symptoms": ["optional: identifiers that look symptom-level"],
    "possible_false_positives": ["optional: prior concept keys likely mis-scoped"]
  }
}
