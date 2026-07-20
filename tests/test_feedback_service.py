import importlib


def test_feedback_service_tracks_comments_and_insights(tmp_path, monkeypatch):
    feedback_module = importlib.import_module("app.services.feedback_service")
    feedback_file = tmp_path / "feedback.json"
    monkeypatch.setattr(feedback_module, "FEEDBACK_FILE", feedback_file)

    service = feedback_module.FeedbackService()

    service.add_feedback({
        "rating": "positive",
        "customer": "C1001",
        "issue": "Fraud report",
        "comment": "The answer was clear and helpful.",
    })
    service.add_feedback({
        "rating": "negative",
        "customer": "C1002",
        "issue": "Chargeback dispute",
        "comment": "It was too verbose and missed the key action.",
    })

    insights = service.get_feedback_insights()

    assert insights["positive_count"] == 1
    assert insights["negative_count"] == 1
    assert any(entry["comment"] == "It was too verbose and missed the key action." for entry in insights["recent_comments"])
