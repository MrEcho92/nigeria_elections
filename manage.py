#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from djangae.environment import is_production_environment


def main():
    """Run administrative tasks."""

    if is_production_environment():
        settings = "core.settings.production"
    else:
        if "test" in sys.argv:
            settings = "core.settings.test"
        else:
            settings = "core.settings.default"

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    from djangae.sandbox import start_emulators, stop_emulators

    try:
        # Start all emulators, persisting data if we're not testing
        start_emulators(persist_data="test" not in sys.argv)
        execute_from_command_line(sys.argv)
    finally:
        # Stop all emulators
        stop_emulators()


if __name__ == "__main__":
    main()
