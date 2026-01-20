from app.github.diff_parser import DiffParser

mock_diff = """
diff --git a/app/main.py b/app/main.py
index 83c5a9..b4d210 100644
--- a/app/main.py
+++ b/app/main.py
@@ -1,4 +1,4 @@
 def hello():
-    print("Hi")
+    print("Hello World")
     return True
 
diff --git a/README.md b/README.md
index 99a3d..12b4c 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,2 @@
 # Code Review Bot
+Now with AI!
"""

parser = DiffParser()
files = parser.parse(mock_diff)

print(f"Found {len(files)} relevant files.")

for f in files:
    print(f"Fil : {f['filename']}")
    print(f"----Patch Start-----\n {f['patch'][:50]}....\n ----Patch End----")
    