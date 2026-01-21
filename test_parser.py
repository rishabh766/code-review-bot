from app.github.diff_parser import DiffParser

# Mock data mimicking the GitHub API response
mock_files_json = [
    {"filename": "app/main.py", "status": "modified", "patch": "print('hello')"},
    {"filename": "app/deleted_file.py", "status": "removed", "patch": "some code"},
    {"filename": "README.md", "status": "modified", "patch": "# Title"},
    {"filename": "poetry.lock", "status": "modified", "patch": "hash..."},
    {"filename": "app/migrations/001_initial.py", "status": "added", "patch": "class Migration..."}
]

print("--- 🧪 Testing File Filtering Logic ---")
parser = DiffParser()
valid_files = parser.filter_files(mock_files_json)

print(f"Input: {len(mock_files_json)} files.")
print(f"Output: {len(valid_files)} valid files.\n")

for f in valid_files:
    print(f"✅ Keeping: {f['filename']} ({f['status']})")

# Validation Logic
filenames = [f['filename'] for f in valid_files]
if "app/deleted_file.py" in filenames:
    print("\n❌ FAIL: Did not filter deleted file.")
elif "README.md" in filenames:
    print("\n❌ FAIL: Did not filter Markdown.")
elif "app/migrations/001_initial.py" in filenames:
    print("\n❌ FAIL: Did not filter migration.")
else:
    print("\n✨ PASS: Filtering logic is correct.")