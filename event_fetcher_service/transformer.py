import requests

class Transformer:
    def transform(self, events):
        transformed_events = []
        for event in events:
            transformed_event = {
                "id": event["id"],
                "type": event["type"],
                "actor_id": event["actor"]["id"],
                "actor_login": event["actor"]["login"],
                "actor_avatar_url": event["actor"]["avatar_url"],
                "repo_id": event["repo"]["id"],
                "repo_name": event["repo"]["name"],
                "created_at": event["created_at"],
            }
            
            # Move this to a separate service

            # Add the repo stars 
            # print(f"Fetching stars for repo: {event["repo"]["name"]}")
            # transformed_event["repo_stars"] = self.fetch_repo_stars(event["repo"]["name"])
            # print(f"Stars: {transformed_event["repo_stars"]}")
            
            transformed_events.append(transformed_event)
        return transformed_events

    # def fetch_repo_stars(self, repo_name):
    #     response = requests.get(f"https://api.github.com/repos/{repo_name}")
    #     return response.json()["stargazers_count"]



