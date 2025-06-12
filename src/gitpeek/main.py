import argparse
import json
import sys
from urllib import request, error

API_URL = "https://api.github.com/users/{username}/events"

def get_user_activity(username):
    """Fetches and returns the public activity for a given GitHub user."""
    url = API_URL.format(username=username)
    try:
        with request.urlopen(url) as response:
            if response.status == 200:
                return json.load(response)
            else:
                print(f"Error: Received status code {response.status}", file=sys.stderr)
                return None
    except error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User '{username}' not found.", file=sys.stderr)
        else:
            print(f"HTTP Error: {e.code} {e.reason}", file=sys.stderr)
        return None
    except error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        return None

def format_event(event):
    """Formats a single GitHub event into a human-readable string."""
    event_type = event['type']
    repo_name = event['repo']['name']
    payload = event.get('payload', {})

    if event_type == 'PushEvent':
        commit_count = len(payload.get('commits', []))
        if commit_count > 0:
            return f"- Pushed {commit_count} commit{'s' if commit_count > 1 else ''} to {repo_name}"
    elif event_type == 'IssuesEvent' and payload.get('action') == 'opened':
        return f"- Opened issue #{payload['issue']['number']} in {repo_name}"
    elif event_type == 'IssueCommentEvent' and payload.get('action') == 'created':
        return f"- Commented on issue #{payload['issue']['number']} in {repo_name}"
    elif event_type == 'WatchEvent' and payload.get('action') == 'started':
        return f"- Starred {repo_name}"
    elif event_type == 'PullRequestEvent' and payload.get('action') == 'opened':
        return f"- Opened pull request #{payload['pull_request']['number']} in {repo_name}"
    elif event_type == 'CreateEvent':
        ref_type = payload.get('ref_type')
        if ref_type == 'repository':
            return f"- Created a new repository: {repo_name}"
        elif ref_type == 'branch':
            return f"- Created branch '{payload['ref']}' in {repo_name}"
        elif ref_type == 'tag':
            return f"- Created tag '{payload['ref']}' in {repo_name}"
    elif event_type == 'DeleteEvent':
        return f"- Deleted {payload['ref_type']} '{payload['ref']}' from {repo_name}"
    elif event_type == 'ForkEvent':
        return f"- Forked {repo_name} to {payload['forkee']['full_name']}"
    elif event_type == 'PublicEvent':
        return f"- Made {repo_name} public"

    # Return None for unhandled event types so they are not printed
    return None

def main():
    parser = argparse.ArgumentParser(description="Fetch recent GitHub activity for a user.")
    parser.add_argument("username", help="The GitHub username to fetch activity for.")
    args = parser.parse_args()

    print(f"Fetching activity for {args.username}...")
    activity = get_user_activity(args.username)

    if activity:
        print(f"Found {len(activity)} recent events for {args.username}:")
        for event in activity:
            formatted_event = format_event(event)
            if formatted_event:
                print(formatted_event)

if __name__ == "__main__":
    main() 