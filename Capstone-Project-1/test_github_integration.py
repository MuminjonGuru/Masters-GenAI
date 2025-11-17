"""
Test GitHub Integration
Verifies that the GitHub issue creation is working
"""

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

print("=" * 70)
print("GITHUB INTEGRATION TEST")
print("=" * 70)
print()

# Check environment variables
print("[1] Checking environment variables...")
github_token = os.getenv("GITHUB_TOKEN")
github_repo = os.getenv("GITHUB_REPO")

if not github_token or github_token == "your_github_personal_access_token_here":
    print("    [ERROR] GITHUB_TOKEN not set in .env file")
    print("    Please add your GitHub Personal Access Token to .env")
    print()
    print("    Steps:")
    print("    1. Go to https://github.com/settings/tokens")
    print("    2. Generate new token (classic)")
    print("    3. Select 'repo' scope")
    print("    4. Copy the token and add to .env file")
    exit(1)

if not github_repo:
    print("    [ERROR] GITHUB_REPO not set in .env file")
    exit(1)

print(f"    [OK] GITHUB_TOKEN: {'*' * 20}{github_token[-4:]}")
print(f"    [OK] GITHUB_REPO: {github_repo}")
print()

# Test GitHub connection
print("[2] Testing GitHub connection...")
try:
    from src.github_integration.issue_creator import GitHubIssueCreator

    creator = GitHubIssueCreator()
    print(f"    [OK] Connected to repository: {creator.repo_name}")
    print()

    # Check connection
    print("[3] Verifying repository access...")
    status = creator.check_connection()

    if status['success']:
        print("    [OK] Repository access verified")
        repo_info = status['repo_info']
        print(f"    Repository: {repo_info['full_name']}")
        print(f"    Private: {repo_info['private']}")
        print(f"    Issues enabled: {repo_info['has_issues']}")
    else:
        print(f"    [ERROR] {status['error']}")
        exit(1)
    print()

    # Ask if user wants to create a test issue
    print("[4] Test issue creation")
    print("    Do you want to create a test issue? (y/n): ", end="")
    response = input().strip().lower()

    if response == 'y':
        print()
        print("    Creating test issue...")
        result = creator.create_issue(
            title="[TEST] Northwind Chat App - GitHub Integration Test",
            description="""This is a test support ticket created by the Northwind Chat Application.

**Purpose**: Verify that the GitHub integration is working correctly.

**What was tested**:
- GitHub API authentication
- Repository access
- Issue creation with labels
- Automated support ticket system

If you see this issue, the integration is working perfectly! ✓

You can close this issue safely.""",
            priority="low"
        )

        if result['success']:
            print(f"    [OK] Test issue created successfully!")
            print(f"    Issue #{result['ticket_number']}")
            print(f"    URL: {result['ticket_url']}")
            print()
            print("    You can view and close this test issue on GitHub.")
        else:
            print(f"    [ERROR] {result['error']}")
            exit(1)
    else:
        print("    [SKIP] Test issue creation skipped")

    print()
    print("=" * 70)
    print("[SUCCESS] GitHub integration is working correctly!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. The support ticket feature is now fully functional")
    print("2. Users can create support tickets through the chat interface")
    print("3. Tickets will be created as GitHub issues in your repository")

except Exception as e:
    print(f"    [ERROR] {e}")
    import traceback
    traceback.print_exc()
    exit(1)
