import unittest
from monitor import vitals_ok

def mock_printer(msg):
    pass

def mock_blink():
    pass


class MonitorTest(unittest.TestCase):

    def test_all_vital_conditions(self):
        test_cases = [
            # All vitals in range → should be OK
            (True, [
                {"name": "temperature", "value": 98.6, "min": 95, "max": 102},
                {"name": "pulse", "value": 70, "min": 60, "max": 100},
                {"name": "spo2", "value": 98, "min": 90, "max": 100}
            ]),

            # Temperature too low → should fail
            (False, [
                {"name": "temperature", "value": 94, "min": 95, "max": 102},
                {"name": "pulse", "value": 70, "min": 60, "max": 100},
                {"name": "spo2", "value": 98, "min": 90, "max": 100}
            ]),

            # Temperature too high → should fail
            (False, [
                {"name": "temperature", "value": 103, "min": 95, "max": 102},
                {"name": "pulse", "value": 70, "min": 60, "max": 100},
                {"name": "spo2", "value": 98, "min": 90, "max": 100}
            ]),

            # Pulse too low → should fail
            (False, [
                {"name": "temperature", "value": 98, "min": 95, "max": 102},
                {"name": "pulse", "value": 55, "min": 60, "max": 100},
                {"name": "spo2", "value": 98, "min": 90, "max": 100}
            ]),

            # Pulse too high → should fail
            (False, [
                {"name": "temperature", "value": 98, "min": 95, "max": 102},
                {"name": "pulse", "value": 101, "min": 60, "max": 100},
                {"name": "spo2", "value": 98, "min": 90, "max": 100}
            ]),

            # SpO2 too low → should fail
            (False, [
                {"name": "temperature", "value": 98, "min": 95, "max": 102},
                {"name": "pulse", "value": 70, "min": 60, "max": 100},
                {"name": "spo2", "value": 85, "min": 90, "max": 100}
            ])
        ]

        for expected, vitals in test_cases:
            with self.subTest(vitals=vitals):
                result = vitals_ok(vitals, printer=mock_printer, blinker=mock_blink)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
