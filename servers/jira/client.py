import os
import requests
from requests.auth import HTTPBasicAuth

JIRA_BASE_URL = os.environ.get("JIRA_BASE_URL", "").rstrip("/")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "")


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
    return {
        "key": issue["key"],
        "summary": issue["fields"]["summary"],
        "status": issue["fields"]["status"]["name"],
        "project": issue["fields"]["project"]["key"]
    }
