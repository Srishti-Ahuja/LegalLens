#!/usr/bin/env python3
import os
import sys
import subprocess

def run_command(command, cwd=None, description=""):
    print(f"\n==================================================")
    print(f" Running: {description}")
    print(f" Directory: {cwd or os.getcwd()}")
    print(f" Command: {' '.join(command)}")
    print(f"==================================================\n")
    
    is_windows = os.name == 'nt'
    result = subprocess.run(command, cwd=cwd, shell=is_windows)
    return result.returncode

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    backend_tests_dir = os.path.join(root_dir, 'tests', 'backend')
    frontend_tests_dir = os.path.join(root_dir, 'tests', 'frontend')

    print("\n--------------------------------------------------")
    print(" LegalLens Unified Test Suite Runner")
    print("--------------------------------------------------")

    # Determine backend test runner (pytest if installed, else python -m unittest)
    try:
        import pytest
        backend_cmd = [sys.executable, "-m", "pytest", "-v"]
    except ImportError:
        backend_cmd = [sys.executable, "-m", "unittest", "discover", "-v"]

    # 1. Run Backend Test Suite
    backend_rc = run_command(backend_cmd, cwd=backend_tests_dir, description="Backend Test Suite")

    # 2. Run Frontend Vitest Suite
    npx_cmd = "npx.cmd" if os.name == "nt" else "npx"
    frontend_cmd = [npx_cmd, "vitest", "run"]
    frontend_rc = run_command(frontend_cmd, cwd=frontend_tests_dir, description="Frontend Vitest Suite")

    # Summary report
    print("\n==================================================")
    print(" SUMMARY OF TEST RESULTS")
    print("==================================================")
    print(f" Backend Test Suite:  {'PASSED' if backend_rc == 0 else 'FAILED'}")
    print(f" Frontend Test Suite: {'PASSED' if frontend_rc == 0 else 'FAILED'}")
    print("==================================================\n")

    if backend_rc != 0 or frontend_rc != 0:
        print("❌ One or more test suites failed.")
        sys.exit(1)
    else:
        print("✅ All backend and frontend test suites passed successfully!")
        sys.exit(0)

if __name__ == '__main__':
    main()
