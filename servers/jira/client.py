import os
import requests
from requests.auth import HTTPBasicAuth

JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL", "").rstrip("/")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "")


def _adf_to_text(adf: object) -> str | None:
    if not isinstance(adf, dict):
        return None

    parts: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            node_type = node.get("type")
            if node_type == "text":
                text = node.get("text")
                if isinstance(text, str) and text:
                    parts.append(text)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(adf)
    text = "".join(parts).strip()
    return text or None


def _get_auth() -> HTTPBasicAuth:
    if not (JIRA_BASE_URL and JIRA_EMAIL and JIRA_API_TOKEN):
        raise ValueError(
            "Missing Jira configuration. Set JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN."
        )
    return HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def _text_to_adf(text: str) -> dict:
    # Jira Cloud expects Atlassian Document Format (ADF) for comment bodies.
    # A single text node containing newline characters is often rejected as invalid.
    # Convert a simple plain-text comment into multiple ADF blocks:
    # - normal lines -> paragraphs
    # - consecutive "- " lines -> bulletList
    lines = text.splitlines()

    def paragraph(line: str) -> dict:
        return {
            "type": "paragraph",
            "content": [
                {
                    "type": "text",
                    "text": line,
                }
            ],
        }

    def bullet_list(items: list[str]) -> dict:
        return {
            "type": "bulletList",
            "content": [
                {
                    "type": "listItem",
                    "content": [paragraph(item)],
                }
                for item in items
            ],
        }

    content: list[dict] = []
    pending_bullets: list[str] = []

    def flush_bullets() -> None:
        nonlocal pending_bullets
        if pending_bullets:
            content.append(bullet_list(pending_bullets))
            pending_bullets = []

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            # blank line: end any active bullet list and do not add empty paragraphs
            flush_bullets()
            continue

        if line.lstrip().startswith("- "):
            pending_bullets.append(line.lstrip()[2:].strip())
            continue

        flush_bullets()
        content.append(paragraph(line.strip()))

    flush_bullets()

    # Fallback to an empty paragraph if the comment is empty/whitespace.
    if not content:
        content = [paragraph("")]

    return {
        "type": "doc",
        "version": 1,
        "content": content,
    }


def get_projects(
    start_at: int = 0,
    max_results: int = 50,
    order_by: str = "lastIssueUpdatedDate",
    query: str | None = None,
    status: str | None = None,
):
    url = f"{JIRA_BASE_URL}/rest/api/3/project/search"
    params: dict[str, object] = {
        "startAt": start_at,
        "maxResults": max_results,
        "orderBy": order_by,
    }
    if query:
        params["query"] = query
    if status:
        params["status"] = status

    resp = requests.get(url, headers=HEADERS, auth=_get_auth(), params=params)
    resp.raise_for_status()

    data = resp.json()
    return [
        {
            "id": p["id"],
            "key": p["key"],
            "name": p["name"],
            "projectTypeKey": p.get("projectTypeKey"),
            "simplified": p.get("simplified"),
            "style": p.get("style"),
            "isPrivate": p.get("isPrivate"),
            "url": p.get("self"),
        }
        for p in data.get("values", [])
    ]


def get_issue(issue_key: str):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    resp = requests.get(url, headers=HEADERS, auth=_get_auth())
    resp.raise_for_status()

    issue = resp.json()
    fields = issue["fields"]
    description = fields.get("description")
    return {
        "key": issue["key"],
        "summary": fields["summary"],
        "description": description,
        "description_text": _adf_to_text(description),
        "status": fields["status"]["name"],
        "project": fields["project"]["key"]
    }

def add_comment_to_issue(input: str | dict, issue_key: str):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"

    body: object
    if isinstance(input, str):
        body = _text_to_adf(input)
    elif isinstance(input, dict):
        body = input
    else:
        raise TypeError("Comment must be a string or an ADF dict")

    payload = {"body": body}

    response = requests.post(url, json=payload, auth=_get_auth(), headers=HEADERS)

    if response.status_code not in (200, 201):
        raise RuntimeError(
            f"Failed to add comment: {response.status_code} - {response.text}"
        )

    return {
        "status": "success",
        "issue_key": issue_key,
        "comment_id": response.json().get("id")
    }

