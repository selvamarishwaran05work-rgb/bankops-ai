import json
from pathlib import Path

FEEDBACK_FILE = Path("data/feedback.json")


class FeedbackService:

    def __init__(self):
        FEEDBACK_FILE.parent.mkdir(exist_ok=True)

        if not FEEDBACK_FILE.exists():
            FEEDBACK_FILE.write_text("[]")

    def add_feedback(self, feedback):

        data = json.loads(FEEDBACK_FILE.read_text())

        data.append(feedback)

        FEEDBACK_FILE.write_text(
            json.dumps(data, indent=2)
        )

    def get_recent_feedback(self):

        return json.loads(
            FEEDBACK_FILE.read_text()
        )


feedback_service = FeedbackService()