import argparse
import json
import sys
from urllib import request, error
from datetime import datetime

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
    """Formats a single GitHub event into a dictionary with a hyperlink."""
    event_type = event['type']
    repo_name = event['repo']['name']
    payload = event.get('payload', {})
    
    # Parse timestamp
    created_at_str = event['created_at']
    created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
    date = created_at.strftime('%Y-%m-%d')
    time = created_at.strftime('%H:%M:%S')

    description = None
    url = None

    if event_type == 'PushEvent':
        commit_count = len(payload.get('commits', []))
        if commit_count > 0:
            description = f"Pushed {commit_count} commit{'s' if commit_count > 1 else ''} to {repo_name}"
            url = f"https://github.com/{repo_name}/compare/{payload['before']}...{payload['head']}"
    elif event_type == 'IssuesEvent' and payload.get('action') == 'opened':
        description = f"Opened issue #{payload['issue']['number']} in {repo_name}"
        url = payload.get('issue', {}).get('html_url')
    elif event_type == 'IssueCommentEvent' and payload.get('action') == 'created':
        description = f"Commented on issue #{payload['issue']['number']} in {repo_name}"
        url = payload.get('comment', {}).get('html_url')
    elif event_type == 'WatchEvent' and payload.get('action') == 'started':
        description = f"Starred {repo_name}"
        url = f"https://github.com/{repo_name}"
    elif event_type == 'PullRequestEvent' and payload.get('action') == 'opened':
        description = f"Opened pull request #{payload['pull_request']['number']} in {repo_name}"
        url = payload.get('pull_request', {}).get('html_url')
    elif event_type == 'CreateEvent':
        ref_type = payload.get('ref_type')
        if ref_type == 'repository':
            description = f"Created a new repository: {repo_name}"
            url = f"https://github.com/{repo_name}"
        elif ref_type == 'branch':
            description = f"Created branch '{payload['ref']}' in {repo_name}"
            url = f"https://github.com/{repo_name}/tree/{payload['ref']}"
        elif ref_type == 'tag':
            description = f"Created tag '{payload['ref']}' in {repo_name}"
            url = f"https://github.com/{repo_name}/releases/tag/{payload['ref']}"
    elif event_type == 'DeleteEvent':
        description = f"Deleted {payload['ref_type']} '{payload['ref']}' from {repo_name}"
        # No URL for deleted items
    elif event_type == 'ForkEvent':
        description = f"Forked {repo_name} to {payload['forkee']['full_name']}"
        url = payload.get('forkee', {}).get('html_url')
    elif event_type == 'PublicEvent':
        description = f"Made {repo_name} public"
        url = f"https://github.com/{repo_name}"

    if description:
        return {'date': date, 'time': time, 'description': description, 'url': url}
    
    return None

def main():
    parser = argparse.ArgumentParser(description="Fetch recent GitHub activity for a user.")
    parser.add_argument("username", help="The GitHub username to fetch activity for.")
    args = parser.parse_args()

    print(f"Fetching activity for {args.username}...")
    activity = get_user_activity(args.username)

    if activity:
        
        processed_events = []
        for event in activity:
            formatted_event = format_event(event)
            if formatted_event:
                processed_events.append(formatted_event)

        if not processed_events:
            print("No supported events found for this user.")
            return
            
        print(f"\nRecent activity for {args.username}:")
        print("-" * 60)
        print(f"{'Date':<12}{'Time':<10}{'Activity'}")
        print("-" * 60)

        for event in processed_events:
            if event['url']:
                # Embed hyperlink using ANSI escape sequence
                hyperlink = f"\x1b]8;;{event['url']}\x07{event['description']}\x1b]8;;\x07"
                print(f"{event['date']:<12}{event['time']:<10}{hyperlink}")
            else:
                print(f"{event['date']:<12}{event['time']:<10}{event['description']}")

if __name__ == "__main__":
    main() 