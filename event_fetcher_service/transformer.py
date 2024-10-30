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
            
            transformed_events.append(transformed_event)
        return transformed_events
