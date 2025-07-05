from features.history_tracker import fetch_world_history

def test_fetch_world_history_returns_data():
    data = fetch_world_history("New York")
    assert isinstance(data, dict)
    assert "temperature_2m_max" in data
    assert "time" in data
    assert len(data["temperature_2m_max"]) == 7
