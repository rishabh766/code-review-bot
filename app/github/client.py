import requests

class GitHubClient:
    def __init__(self, token : str = None):
        self.token = token
        self.base_url = "https://api.github.com"

    def _get_headers(self):
        return{
            "Accept" : "application/vnd.github.v3+json",
            "Authorization" : f"Bearer {self.token}" if self.token else None,
            "User-Agent" : "CodeReviewBot"
        }

    def get_pr_files(self, owner:str, repo:str, pr_number:int) -> list:
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self._get_headers())

        if response.status_code != 200:
            print(f"Error fetching files: {response.status_code}")
            return []
        
        return response.json()
    
    def get_pr_diff(self, diff_url : str) -> str:
        headers = self._get_headers()
        headers['Accept'] = "application/vnd.github.v3.diff"
        response = requests.get(diff_url, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching the diff: {response.status_code}")
            return ""
        
        return response.text
    
    