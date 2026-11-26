import unittest

from CORE.neuro_symbolic.verifier import (
    verify_claims,
    verify_response_claims,
)


class TestNeuroSymbolic(unittest.TestCase):

    def test_consistent_claims(self):
        result = verify_claims([
            {"proposition": "rain", "value": True},
            {"proposition": "wind", "value": False},
        ])
        self.assertTrue(result["accepted"])
        self.assertEqual(result["status"], "CONSISTENT")

    def test_contradiction(self):
        result = verify_claims([
            {"proposition": "door_open", "value": True},
            {"proposition": "door_open", "value": False},
        ])
        self.assertFalse(result["accepted"])
        self.assertEqual(result["status"], "CONTRADICTION")
        self.assertTrue(result["conflicts"])

    def test_empty_claims(self):
        result = verify_claims([])
        self.assertFalse(result["accepted"])
        self.assertEqual(result["status"], "UNVERIFIED_EMPTY")

    def test_invalid_claim(self):
        result = verify_claims([
            {"proposition": "p", "value": 123},
        ])
        self.assertFalse(result["accepted"])

    def test_duplicate_consistent_claims(self):
        result = verify_claims([
            {"proposition": "p", "value": True},
            {"proposition": "p", "value": True},
        ])
        self.assertTrue(result["accepted"])

    def test_response_evidence(self):
        answer = "The earth orbits the sun."
        result = verify_response_claims(answer, [
            {
                "proposition": "earth_orbits_sun",
                "value": True,
                "evidence": "The earth orbits the sun.",
            }
        ])
        self.assertTrue(result["accepted"])

    def test_missing_evidence(self):
        result = verify_response_claims(
            "The sky is blue.",
            [{
                "proposition": "sky_is_blue",
                "value": True,
                "evidence": "The ocean is blue.",
            }],
        )
        self.assertFalse(result["accepted"])
        self.assertEqual(result["status"], "INVALID_EVIDENCE")

    def test_response_contradiction(self):
        result = verify_response_claims(
            "The door is open. The door is not open.",
            [
                {
                    "proposition": "door_open",
                    "value": True,
                    "evidence": "The door is open.",
                },
                {
                    "proposition": "door_open",
                    "value": False,
                    "evidence": "The door is not open.",
                },
            ],
        )
        self.assertFalse(result["accepted"])
        self.assertEqual(result["status"], "CONTRADICTION")


if __name__ == "__main__":
    unittest.main()
