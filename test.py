import requests

def git_act(username, token=None):
    url=f"https://api.github.com/users/{username}/events"

    headers={}
    if token:
        headers["Authorization"]=f"Bearer {token}"

    response = requests.get(url, headers= headers)

    if response.status_code == 404:
        print("user not found!")
        return
    elif response.status_code != 200:
        print("Error!",response.status_code,response.text)
        return
    
    events = response.json()

    if not events:
        print("No recent public activity.")
        return
    
    print(f"\nRecent Public Activity for '{username}':\n")

    for event in events[:10]:
        event_type=event.get("type")
        repo_name=event.get("repo",{}).get("name")
        created_at=event.get("created_at")

        print(f"{event_type} | {repo_name} | {created_at}")

if __name__ == "__main__":
    username = input("enter Github username:")

    git_act(username)
