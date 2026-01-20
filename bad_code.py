import os

def bad_function():
    # Ruff Error F841: assigned to variable but never used
    x = 1 
    
    # Semgrep Error: Hardcoded password
    password = "super_secret_password"
    
    # Ruff Error E401: Multiple imports on one line
    import sys, json

    eval("print('hacking your system')")