import uuid
import pytest
from app.collaboration.schemas import CommentCreateRequest, PresenceUpdate, TaskAssignRequest
from app.collaboration.service import global_collaboration_service


def test_add_comment_and_mentions():
    author_id = uuid.uuid4()
    req = CommentCreateRequest(
        target_type="dashboard",
        target_id="dash_123",
        content="Hey @alice and @bob, please review revenue totals!",
    )
    comment = global_collaboration_service.add_comment(author_id, req)
    assert comment.target_id == "dash_123"
    assert "alice" in comment.mentions
    assert "bob" in comment.mentions


def test_assign_task_and_presence():
    u_id = uuid.uuid4()
    task_req = TaskAssignRequest(
        title="Approve Q2 Forecast Model",
        assignee_id=u_id,
        target_type="report",
        target_id="rep_99",
    )
    task = global_collaboration_service.assign_task(task_req)
    assert task.title == "Approve Q2 Forecast Model"
    assert task.status == "pending"

    presence = PresenceUpdate(
        user_id=u_id,
        user_name="Alice Specialist",
        active_resource_id="dash_123",
        status="editing",
    )
    active = global_collaboration_service.update_presence(presence)
    assert len(active) >= 1
