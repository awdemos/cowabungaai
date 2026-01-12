"""OpenAI Compliant Threads API Router."""

import time
from typing import Any
from fastapi import HTTPException, APIRouter, status as http_status
from openai.types.beta.threads import Run
from openai.types.beta.threads.runs import RunStep
from leapfrogai_api.routers.supabase_session import Session
from leapfrogai_api.data.crud_run import CRUDRun

router = APIRouter(prefix="/openai/v1/threads", tags=["openai/threads/run-steps"])


@router.post("/{thread_id}/runs/{run_id}/submit_tool_outputs")
async def submit_tool_outputs(
    thread_id: str,
    run_id: str,
    tool_outputs: list[dict[str, Any]],
    session: Session,
) -> Run:
    """Submit tool outputs for a run.

    When a run has status: "requires_action" and required_action.type is
    "submit_tool_outputs", this endpoint submits outputs from tool calls.
    """
    crud_run = CRUDRun(db=session)
    run = await crud_run.get(id_=run_id)

    if not run:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Run not found",
        )

    # Validate that run is in requires_action state
    if run.status != "requires_action":
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Run is not in requires_action state, current status: {run.status}",
        )

    # Validate tool_outputs format
    if not tool_outputs:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="tool_outputs must not be empty",
        )

    for tool_output in tool_outputs:
        if "tool_call_id" not in tool_output:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Each tool output must include tool_call_id",
            )
        if "output" not in tool_output:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Each tool output must include output",
            )

    # Update run status to resume execution
    # Note: Full tool execution handling would require integration with Composer
    run_dict = run.model_dump()
    run_dict["status"] = "queued"

    updated_run = await crud_run.update(id_=run_id, object_=Run(**run_dict))

    if not updated_run:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update run",
        )

    return updated_run


@router.post("/{thread_id}/runs/{run_id}/cancel")
async def cancel_run(thread_id: str, run_id: str, session: Session) -> Run:
    """Cancel a run.

    Cancels a run that is in_progress or queued.
    """
    crud_run = CRUDRun(db=session)
    run = await crud_run.get(id_=run_id)

    if not run:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Run not found",
        )

    # Only allow cancellation of in_progress or queued runs
    if run.status not in ["in_progress", "queued"]:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel run with status: {run.status}",
        )

    # Update run status to cancelled with timestamp
    run_dict = run.model_dump()
    run_dict["status"] = "cancelled"
    run_dict["cancelled_at"] = int(time.time())

    updated_run = await crud_run.update(id_=run_id, object_=Run(**run_dict))

    if not updated_run:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel run",
        )

    return updated_run


@router.get("/{thread_id}/runs/{run_id}/steps")
async def list_run_steps(
    thread_id: str,
    run_id: str,
    session: Session,
    limit: int = 20,
    order: str = "desc",
) -> list[RunStep]:
    """List all of steps in a run.

    Note: Run steps tracking is not yet implemented in the database.
    Returns empty list for now.
    """
    crud_run = CRUDRun(db=session)
    run = await crud_run.get(id_=run_id)

    if not run:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Run not found",
        )

    # Run steps are not yet implemented in the database schema
    # This would require a run_steps table and tracking during run execution
    return []


@router.get("/{thread_id}/runs/{run_id}/steps/{step_id}")
async def retrieve_run_step(
    thread_id: str, run_id: str, step_id: str, session: Session
) -> RunStep:
    """Retrieve a step.

    Note: Run steps tracking is not yet implemented in the database.
    Returns 404 for now.
    """
    crud_run = CRUDRun(db=session)
    run = await crud_run.get(id_=run_id)

    if not run:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Run not found",
        )

    # Run steps are not yet implemented in the database schema
    # This would require a run_steps table and tracking during run execution
    raise HTTPException(
        status_code=http_status.HTTP_404_NOT_FOUND,
        detail="Run step not found - run steps not yet implemented",
    )
