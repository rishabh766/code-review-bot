import re

class DiffParser:
    def parse(self, diff_text : str):
        files = []
        raw_files = diff_text.split("diff --git")

        for raw in raw_files:
            if not raw.strip():
                continue

            filename_match = re.search(r"a/(.*?) b/(.*)", raw.split("\n")[0])

            filename = filename_match.group(2).strip()

            if not filename.endswith(".py"):
                continue

            files.append({
                "filename" : filename,
                "patch" : raw
            })

        return files
    
    def filter_files(self, files_json : list) -> list:
        valid_files = []
        IGNORED_DIRS = {"node_modules/", "venv/", "migrations/", "dist/", "build/"}
        IGNORED_EXTENTIONS = {".lock", ".json", ".md", ".txt", ".png", ".jpg", ".pyc"}

        for file in files_json:
            filename = file.get("filename", "")
            status = file.get("status", "")

            if status == 'removed':
                continue

            if not filename.endswith(".py"):
                continue 

            if any(ignored in filename for ignored in IGNORED_DIRS):
                continue 

            if any(filename.endswith(ext) for ext in IGNORED_EXTENTIONS):
                continue

            valid_files.append({
                "filename" : filename,
                "status": status,
                "patch" : file.get("patch", "")
            })

        return valid_files