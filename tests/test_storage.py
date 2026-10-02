from pomodoro.core.storage import SessionStorage
from pomodoro.core.timer import SessionType


def test_session_storage(tmp_path):
    stats_file = tmp_path / "test_stats.json"
    storage = SessionStorage(data_path=stats_file)

    assert storage.get_today_work_sessions() == 0

    storage.record_session(SessionType.WORK, 1500)
    storage.record_session(SessionType.SHORT_BREAK, 300)
    storage.record_session(SessionType.WORK, 1500)

    assert storage.get_today_work_sessions() == 2
