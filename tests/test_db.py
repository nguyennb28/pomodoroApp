from pomodoro.core.db import Database
from pomodoro.core.timer import TimerConfig


def test_database_tasks(tmp_path):
    db_file = tmp_path / "test.db"
    db = Database(db_path=db_file)

    assert db.get_tasks() == []

    # Add tasks
    task1_id = db.add_task("Write unit tests")
    task2_id = db.add_task("Design UI")
    assert task1_id > 0
    assert task2_id > 0

    tasks = db.get_tasks()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Design UI"  # Ordered desc by id

    # Increment pomodoros
    db.increment_task_pomodoro(task1_id)
    db.increment_task_pomodoro(task1_id)
    updated_tasks = {t["id"]: t for t in db.get_tasks()}
    assert updated_tasks[task1_id]["pomodoros_spent"] == 2

    # Toggle complete
    is_done = db.toggle_task(task1_id)
    assert is_done is True
    updated_tasks = {t["id"]: t for t in db.get_tasks()}
    assert updated_tasks[task1_id]["is_completed"] == 1

    # Delete task
    db.delete_task(task2_id)
    assert len(db.get_tasks()) == 1


def test_database_settings(tmp_path):
    db_file = tmp_path / "test.db"
    db = Database(db_path=db_file)

    cfg = TimerConfig(work_duration=3000, short_break_duration=600, long_break_duration=1200)
    db.save_timer_config(cfg)

    loaded = db.load_timer_config()
    assert loaded.work_duration == 3000
    assert loaded.short_break_duration == 600
    assert loaded.long_break_duration == 1200


def test_database_sessions(tmp_path):
    db_file = tmp_path / "test.db"
    db = Database(db_path=db_file)

    assert db.get_today_sessions_count() == 0
    db.record_session("work", 1500)
    db.record_session("short_break", 300)
    db.record_session("work", 1500)

    assert db.get_today_sessions_count() == 2
