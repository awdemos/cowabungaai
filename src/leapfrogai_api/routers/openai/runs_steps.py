"""OpenAI Compliant Threads API Router."""

from fastapi import HTTPException, APIRouter
from openai.types.beta.threads import Run
from openai.types.beta.threads.runs import RunStep
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.data.crud_run import CRUDRun

router = APIRouter(prefix="/openai/v1/threads", tags=["openai/threads/run-steps"])


@router.post("/{thread_id}/runs/{run_id}/submit_tool_outputs")
async def submit_tool_outputs(thread_id: str, run_id: str, session: Session) -> Run:
    """Submit tool outputs for a run."""
    crud_run = CRUDRun(db=session)
    run = await crud_run.get(id_=run_id)

    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    # For now, return the existing run
    # TODO: Implement actual tool output submission logic
    return run


@router.post("/{thread_id}/runs/{run_id}/cancel")
async def cancel_run(thread_id: str, run_id: str, session: Session) -> Run:
    """Cancel a run."""
    crud_run = CRUDRun(db=session)
    run = await crud_run.get(id_=run_id)

    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    # For now, return the existing run without cancellation
    # TODO: Implement actual run cancellation logic
    return run


@router.get("/{thread_id}/runs/{run_id}/steps")
async def list_run_steps(
    thread_id: str, run_id: str, session: Session
) -> list[RunStep]:
    """List all the steps in a run."""
    crud_run = CRUDRun(db=session)
    run = await crud_run.get(id_=run_id)

    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    # For now, return empty list as run steps are not yet implemented
    # TODO: Implement actual run steps listing logic
    return []


@router.get("/{thread_id}/runs/{run_id}/steps/{step_id}")
async def retrieve_run_step(
    thread_id: str, run_id: str, step_id: str, session: Session
) -> RunStep:
    """Retrieve a step."""
    crud_run = CRUDRun(db=session)
    run = await crud_run.get(id_=run_id)

    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    # For now, raise 404 as run steps are not yet implemented
    # TODO: Implement actual run step retrieval logic
    raise HTTPException(status_code=404, detail="Run step not found")
