from .progress_tracker import TestProgressTracker


def test_08_coursework_summary():
    passed = TestProgressTracker.passed_count()
    points = TestProgressTracker.points_earned()
    print(f"{passed} tests passed, {points:.0f}/20 CW2 obtained (3 points for reports).")
