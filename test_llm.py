from app.llm.reviewer import LLMReviewer

reviewer = LLMReviewer(api_key=None)

mock_diff = "some changed code..."

review = reviewer.review_diff(mock_diff)

print("\n---Mock AI review summary----")
print(review['summary'])
print("\n---Inline comments----")
for comment in review["comments"]:
    print(f"[File: {comment['file']} | Line {comment['line']}]")
    print(f"{comment['text']}\n")