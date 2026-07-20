from typing import Optional

from pydantic import BaseModel


class ActionItem(BaseModel):
    title: str
    description: str
    assignee: str
    status: str
    issuetype: str
    project: Optional[str] = None
    due_date: Optional[str] = None
    start_date: Optional[str] = None
    priority: Optional[str] = None
    parent: Optional[str] = None
    children: Optional[list[str]] = None


class ActionItemsList(BaseModel):
    action_items: list[ActionItem]


class CreateIssuesResponse(BaseModel):
    action_items: list[ActionItem]
    error_messages: list[str]
    success_messages: list[str]
    text: str
