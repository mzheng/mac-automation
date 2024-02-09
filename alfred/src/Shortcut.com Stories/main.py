import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))

import requests
import json

def fetch_shortcut_tasks():
    # Retrieve environment variables
    token = os.getenv('shortcut_api_token')
    owner = os.getenv('shortcut_user_name')
    
    # Construct the URL with the environment variables
    url = f"https://api.app.shortcut.com/api/v3/search?token={token}&query=owner:{owner}%20!is:done+and+is%3Astory"
    headers = {"Content-Type": "application/json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    tasks_json = fetch_shortcut_tasks()
    
    if tasks_json and 'stories' in tasks_json and 'data' in tasks_json['stories']:
        tasks = tasks_json['stories']['data']
        alfred_items = {"items": []}
        
        for task in tasks:
            title = "[" + str(task["id"]) + "] " + task["name"]
            alfred_item = {
                "uid": task["id"],
                "title": title,
                # "subtitle": task.get("description", "No description provided."),
                "arg": task["app_url"],
                "mods": {
                    "cmd": {
                        "valid": True,
                        "arg": task["id"],
                        "subtitle": "Press Enter to copy the shortcut ID."
                    }
                },
                "autocomplete": task["name"],
                "quicklookurl": task["app_url"]
                # "icon": {"path": "icon.png"}  # Assuming you have an icon.png in your workflow folder
            }
            alfred_items["items"].append(alfred_item)
        
        print(json.dumps(alfred_items))
    else:
        print(json.dumps({"items": [{"title": "No tasks found or failed to fetch tasks."}]}))

if __name__ == "__main__":
    main()
