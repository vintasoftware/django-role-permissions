#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    import coverage
    coverage.process_startup()
    os.environ["COVERAGE_PROCESS_START"] = ".coveragerc"

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testsettings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
