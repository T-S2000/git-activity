import requests
import argparse
import sys

BASE_URL = "https://api.github.com"

def git_act(username , limit=10 , event_type=None):

    headers={}

    if not username:
        print("❌ Username required if no token provided.")
        sys.exit(1)
    
    url = f"{BASE_URL}/users/{username}/events"

    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        print("user not found!")
        sys.exit(1)

    elif response.status_code != 200:
        print("Error!",response.status_code,response.text)
        sys.exit(1)
    
    events = response.json()

    if not events:
        print("No recent public activity.")
        return
    
    print(f"\nRecent Public Activity for '{username}':\n")

    count = 0

    for event in events[:10]:
        if event_type and event["type"] != event_type:
            continue

        repo_name=event.get("repo",{}).get("name")
        created_at=event.get("created_at")

        print(f"{event['type']} | {repo_name} | {created_at}")

        count += 1
        if count >= limit:
            break

def main():
    parser = argparse.ArgumentParser(description="Fetch github user activity")

    parser.add_argument("-u", "--username", help="GitHub username")
    parser.add_argument("-l", "--limit", type=int, default=10,
                        help="Number of events to display (default: 10)")
    parser.add_argument("-e", "--event", help="Filter by event type (e.g., PushEvent)")

    args = parser.parse_args()

    git_act(username=args.username,limit=args.limit, event_type=args.event)

if __name__ == "__main__":
    main()