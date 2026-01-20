from app.analysis.ruff_runner import RuffRunner
from app.analysis.semgrep_runner import SemgrepRunner
from app.analysis.bandit_runner import BanditRunner

target_file = "bad_code.py"

print(f"----analyzing {target_file} ----")

print("\n [Running Ruff]....")
ruff = RuffRunner()
ruff_results = ruff.analyze(target_file)
print(f"Found {len(ruff_results)} ruff issues...")
for issue in ruff_results:
    print(f"-Line {issue['location']['row']} : {issue['message']}")

print("\n[Running Bandit...]")
bandit = BanditRunner()
bandit_results = bandit.analyze(target_file)
print(f"Found {len(bandit_results)} Bandit issues.")
for issue in bandit_results:
    print(f" - Line {issue['line']} [{issue['severity']}]: {issue['message']}")

# print("\n[Running Semgrep...]")
# semgrep = SemgrepRunner()
# semgrep_results = semgrep.analyze(target_file)
# print(f"Found {len(semgrep_results)} Semgrep issues.")
# for issue in semgrep_results:
#     print(f" - Line {issue['start']['line']}: {issue['extra']['message']}")