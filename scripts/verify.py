#! /usr/bin/env python

"""Script that runs all verification steps.
"""

import argparse

import os
import shutil
import subprocess
from subprocess import check_output
from subprocess import run
from subprocess import CalledProcessError
import sys

def check_for_java() -> bool:
    java_version = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)
    if 'version' in java_version.decode():
        return True
    else:
        raise RuntimeError('Java is not installed.')

def main(checks):
    try:
        check_for_java()

        print("Verifying with " + str(checks))
        if "pytest" in checks:
            print("Tests (pytest):", flush=True)
            run("pytest -v --color=yes", shell=True, check=True)

        if "pylint" in checks:
            print("Linter (pylint):", flush=True)
            run("pylint -d locally-disabled,locally-enabled -f colorized allennlp", shell=True, check=True)
            print("pylint checks passed")

        if "mypy" in checks:
            print("Typechecker (mypy):", flush=True)
            run("mypy allennlp --ignore-missing-imports", shell=True, check=True)
            print("mypy checks passed")

        if "build-docs" in checks:
            print("Documentation (build):", flush=True)
            run("cd doc; make html-strict", shell=True, check=True)

        if "check-docs" in checks:
            print("Documentation (check):", flush=True)
            run("./scripts/check_docs.py", shell=True, check=True)
            print("check docs passed")

        if "check-links" in checks:
            print("Checking links in Markdown files:", flush=True)
            run("./scripts/check_links.py", shell=True, check=True)
            print("check links passed")

        if "check-requirements" in checks:
            print("Checking requirements.txt against setup.py", flush=True)
            run("./scripts/check_requirements_and_setup.py")
            print("check requirements passed")

    except CalledProcessError:
        # squelch the exception stacktrace
        sys.exit(1)

if __name__ == "__main__":
    checks = ['pytest', 'pylint', 'mypy', 'build-docs', 'check-docs', 'check-links', 'check-requirements']

    parser = argparse.ArgumentParser()
    parser.add_argument('--checks', type=str, required=False, nargs='+', choices=checks)

    args = parser.parse_args()

    if args.checks:
        run_checks = args.checks
    else:
        run_checks = checks

    main(run_checks)
