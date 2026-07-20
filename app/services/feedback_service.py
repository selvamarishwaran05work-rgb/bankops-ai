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
        FEEDBACK_FILE.write_text(json.dumps(data, indent=2))

    def get_recent_feedback(self):
        return json.loads(FEEDBACK_FILE.read_text())

    def get_feedback_insights(self):
        feedback = self.get_recent_feedback()
        positive = [item for item in feedback if item.get("rating") == "positive"]
        negative = [item for item in feedback if item.get("rating") == "negative"]
        recent_comments = [
            {
                "rating": item.get("rating"),
                "comment": item.get("comment") or "No comment provided",
                "customer": item.get("customer") or "-",
            }
            for item in feedback[-8:]
            if item.get("comment")
        ]
        return {
            "positive_count": len(positive),
            "negative_count": len(negative),
            "recent_comments": recent_comments,
            "adaptive_summary": (
                "The assistant should be more concise and action-oriented based on recent feedback."
                if len(negative) > len(positive)
                else "The assistant is performing well and should keep the current style."
            ),
        }


feedback_service = FeedbackService()