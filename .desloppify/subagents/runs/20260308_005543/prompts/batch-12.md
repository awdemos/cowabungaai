You are a focused subagent reviewer for a single holistic investigation batch.

Repository root: /Users/a/code/cowabungaai
Blind packet: /Users/a/code/cowabungaai/.desloppify/review_packet_blind.json
Batch index: 12
Batch name: authorization_consistency
Batch rationale: seed files for authorization_consistency review

DIMENSION TO EVALUATE:

## authorization_consistency
Auth/permission patterns consistently applied across the codebase
Look for:
- Route handlers with auth decorators/middleware on some siblings but not others
- RLS enabled on some tables but not siblings in the same domain
- Permission strings as magic literals instead of shared constants
- Mixed trust boundaries: some endpoints validate user input, siblings don't
- Service role / admin bypass without audit logging or access control
Skip:
- Public routes explicitly documented as unauthenticated (health checks, login, webhooks)
- Internal service-to-service calls behind network-level auth
- Dev/test endpoints behind feature flags or environment checks

YOUR TASK: Read the code for this batch's dimension. Judge how well the codebase serves a developer from that perspective. The dimension rubric above defines what good looks like. Cite specific observations that explain your judgment.

Mechanical scan evidence — navigation aid, not scoring evidence:
The blind packet contains `holistic_context.scan_evidence` with aggregated signals from all mechanical detectors — including complexity hotspots, error hotspots, signal density index, boundary violations, and systemic patterns. Use these as starting points for where to look beyond the seed files.

Seed files (start here):
- src/leapfrogai_api/main.py
- src/leapfrogai_api/routers/base.py
- src/leapfrogai_api/routers/health.py
- src/leapfrogai_api/routers/leapfrogai/auth.py
- src/leapfrogai_api/routers/leapfrogai/count.py
- src/leapfrogai_api/routers/leapfrogai/models.py
- src/leapfrogai_api/routers/leapfrogai/rag.py
- src/leapfrogai_api/routers/leapfrogai/vector_stores.py
- src/leapfrogai_api/routers/openai/assistants.py
- src/leapfrogai_api/routers/openai/audio.py
- src/leapfrogai_api/routers/openai/chat.py
- src/leapfrogai_api/routers/openai/completions.py
- src/leapfrogai_api/routers/openai/embeddings.py
- src/leapfrogai_api/routers/openai/files.py
- src/leapfrogai_api/routers/openai/messages.py
- src/leapfrogai_api/routers/openai/models.py
- src/leapfrogai_api/routers/openai/runs.py
- src/leapfrogai_api/routers/openai/runs_steps.py
- src/leapfrogai_api/routers/openai/threads.py
- src/leapfrogai_api/routers/openai/vector_stores.py

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
  "batch": "authorization_consistency",
  "batch_index": 12,
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
