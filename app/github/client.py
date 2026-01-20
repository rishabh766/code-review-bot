import requests

class GitHubClient:
    def __init__(self, token : str = None):
        self.token = token
        self.base_url = "https://api.github.com"

    def get_pr_diff(self, diff_url : str) -> str:
        headers = {
            "Accept" : "application/vnd.github.v3.diff",
            "Authorization" : f"Bearer {self.token}" if self.token else None,
            "User-Agent" : "CodeReviewBot"
        }
        response = requests.get(diff_url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching diff: {response.status_code}")
            return ""
        
        return response.text
    