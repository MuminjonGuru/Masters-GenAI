"""
GitHub Issue Creator
Creates support tickets as GitHub issues
"""

import os
from typing import Dict, Any, Optional
from github import Github, GithubException


class GitHubIssueCreator:
    """
    Creates GitHub issues for support tickets.
    """

    def __init__(self, token: Optional[str] = None, repo_name: Optional[str] = None):
        """
        Initialize GitHub issue creator.

        Args:
            token: GitHub personal access token (if None, reads from GITHUB_TOKEN env var)
            repo_name: Repository name in format "owner/repo" (if None, reads from GITHUB_REPO env var)
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.repo_name = repo_name or os.getenv("GITHUB_REPO")

        if not self.token:
            raise ValueError("GitHub token not provided. Set GITHUB_TOKEN environment variable.")

        if not self.repo_name:
            raise ValueError("GitHub repository not provided. Set GITHUB_REPO environment variable.")

        # Initialize GitHub client
        self.client = Github(self.token)
        self.repo = None

        # Validate repository access
        try:
            self.repo = self.client.get_repo(self.repo_name)
        except GithubException as e:
            raise ValueError(f"Unable to access repository '{self.repo_name}': {e.data.get('message', str(e))}")

    def create_issue(self, title: str, description: str, priority: str = "medium") -> Dict[str, Any]:
        """
        Create a GitHub issue.

        Args:
            title: Issue title
            description: Issue description/body
            priority: Priority level (low, medium, high, critical)

        Returns:
            Dictionary with issue creation result
        """
        try:
            # Add priority label and formatting
            labels = [f"priority:{priority}", "support-ticket", "automated"]

            # Format issue body with metadata
            issue_body = f"""## Support Request

{description}

---

**Priority**: {priority}
**Created by**: Northwind Chat Application
**Type**: Automated Support Ticket
"""

            # Create the issue
            issue = self.repo.create_issue(
                title=title,
                body=issue_body,
                labels=labels
            )

            return {
                "success": True,
                "ticket_url": issue.html_url,
                "ticket_number": issue.number,
                "message": f"Support ticket #{issue.number} created successfully"
            }

        except GithubException as e:
            error_message = e.data.get('message', str(e)) if hasattr(e, 'data') else str(e)
            return {
                "success": False,
                "error": f"GitHub API error: {error_message}",
                "ticket_url": None,
                "ticket_number": None
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "ticket_url": None,
                "ticket_number": None
            }

    def check_connection(self) -> Dict[str, Any]:
        """
        Check if GitHub connection is working.

        Returns:
            Dictionary with connection status
        """
        try:
            repo_info = {
                "name": self.repo.name,
                "full_name": self.repo.full_name,
                "private": self.repo.private,
                "has_issues": self.repo.has_issues
            }

            if not self.repo.has_issues:
                return {
                    "success": False,
                    "error": "Issues are disabled for this repository",
                    "repo_info": repo_info
                }

            return {
                "success": True,
                "message": "GitHub connection successful",
                "repo_info": repo_info
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Connection check failed: {str(e)}",
                "repo_info": None
            }


if __name__ == "__main__":
    # Test the GitHub issue creator
    from dotenv import load_dotenv
    load_dotenv()

    print("=" * 70)
    print("GITHUB ISSUE CREATOR TEST")
    print("=" * 70)
    print()

    try:
        # Initialize creator
        print("[1] Initializing GitHub client...")
        creator = GitHubIssueCreator()
        print(f"    Connected to: {creator.repo_name}")
        print()

        # Check connection
        print("[2] Checking connection...")
        status = creator.check_connection()
        if status['success']:
            print("    [OK] Connection successful")
            repo_info = status['repo_info']
            print(f"    Repository: {repo_info['full_name']}")
            print(f"    Private: {repo_info['private']}")
            print(f"    Issues enabled: {repo_info['has_issues']}")
        else:
            print(f"    [ERROR] {status['error']}")
            exit(1)
        print()

        # Create test issue
        print("[3] Creating test issue...")
        result = creator.create_issue(
            title="[TEST] Northwind Chat App - Support Ticket Test",
            description="This is a test support ticket created by the Northwind Chat Application.\n\nIf you see this, the GitHub integration is working correctly!",
            priority="low"
        )

        if result['success']:
            print("    [OK] Issue created successfully")
            print(f"    Issue #{result['ticket_number']}")
            print(f"    URL: {result['ticket_url']}")
        else:
            print(f"    [ERROR] {result['error']}")
        print()

        print("=" * 70)
        print("[SUCCESS] GitHub integration test completed!")
        print("=" * 70)

    except Exception as e:
        print(f"[ERROR] {e}")
        exit(1)
