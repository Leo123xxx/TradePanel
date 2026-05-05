"""
scheduler/jobs.py — Native-mode scheduler entry point.

This module is intentionally a thin shim.  All job logic lives in
docker_jobs.py (the canonical source of truth).  Importing from there
ensures fixes and improvements only need to be made in one place.

Usage (native / non-Docker):
    python -m scheduler.jobs

Usage (Docker):
    python -m scheduler.docker_jobs
"""

from scheduler.docker_jobs import TradingScheduler  # noqa: F401  (re-export)

if __name__ == "__main__":
    import time

    scheduler = TradingScheduler()
    scheduler.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
