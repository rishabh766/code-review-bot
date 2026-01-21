import requests
import json 
import logging

logger = logging.getLogger("github_client")

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
    
    def post_comment(self, owner : str, repo : str, pr_number: int, body : str):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{pr_number}/comments"
        payload = {"body" : body}

        if not self.token:
            print(f"\n [MOCK POST] comment on PR #{pr_number} : \n {body} \n")
            return
        
        requests.post(url, json=payload, headers=self._get_headers())

    def post_batch_review(self, owner :str, repo :str, pr_number : int, commit_sha : str, comments :list):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{pr_number}/reviews"

        payload = {
            "commit_id" : commit_sha,
            "event" : "COMMENT",
            "comments" : comments
        }

        if not self.token:
            print("\n" + "="*40)
            print(f"[MOCK BATCH REVIEWS] on PR {pr_number} (SHA: {commit_sha[:7]})")
            print(f"Posting {len(comments)} inline comments")
            for c in comments:
                print(f"  -{c['path']} : {c['line']} -> {c['body']}")
            print("="*40)
            return
        
        response = requests.post(url, json=payload, headers=self._get_headers())
        if response.status_code == 200:
            logger.info("Batch Review passed ", len(comments), "comments.")
        else:
            logger.error(f"Failed to post the batch review comments, ", response.status_code)

            



    
    