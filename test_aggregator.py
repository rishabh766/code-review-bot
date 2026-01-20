from app.analysis.aggregator import Aggregator

changed_files = [
    {"filename": "bad_code.py", "patch": "..."}
]

print("---Running Full PR Analysis---")
aggregator = Aggregator()
markdown_report = aggregator.analyze_pr(changed_files)

print("\n" + "="*40)
print(markdown_report)
print("="*40 + "\n")