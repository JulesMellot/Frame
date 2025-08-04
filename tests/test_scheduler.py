import time
from frame.scheduler import Scheduler


def test_scheduler_runs_periodic_tasks():
    calls: list[int] = []

    def task() -> None:
        calls.append(1)

    sched = Scheduler(0.05, task)
    sched.start()
    time.sleep(0.12)
    sched.stop()

    assert len(calls) >= 2
