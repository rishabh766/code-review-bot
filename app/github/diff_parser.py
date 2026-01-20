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