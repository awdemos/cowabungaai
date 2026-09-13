You are a focused subagent reviewer for a single holistic investigation batch.

Repository root: /Users/a/code/cowabungaai
Blind packet: /Users/a/code/cowabungaai/.desloppify/review_packet_blind.json
Batch index: 7
Batch name: dependency_health
Batch rationale: seed files for dependency_health review

DIMENSION TO EVALUATE:

## dependency_health
Unused deps, version conflicts, multiple libs for same purpose, heavy deps
Look for:
- Multiple libraries for the same purpose (e.g. moment + dayjs, axios + fetch wrapper)
- Heavy dependencies pulled in for light use (e.g. lodash for one function)
- Circular dependency cycles visible in the import graph
- Unused dependencies in package.json/requirements.txt
- Version conflicts or pinning issues visible in lock files
Skip:
- Dev dependencies (test, build, lint tools)
- Peer dependencies required by frameworks

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
6. Do not edit repository files.
7. Return ONLY valid JSON, no markdown fences.

Scope enums:
- impact_scope: "local" | "module" | "subsystem" | "codebase"
- fix_scope: "single_edit" | "multi_file_refactor" | "architectural_change"

Output schema:
{
  "batch": "dependency_health",
  "batch_index": 7,
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
