import unittest
from monitor import vitals_ok

def mock_printer(msg): pass
def mock_blink(): pass

def make_vitals(temp, pulse, spo2):
    return [
        {"name": "temperature", "value": temp, "min": 95, "max": 102},
        {"name": "pulse", "value": pulse, "min": 60, "max": 100},
        {"name": "spo2", "value": spo2, "min": 90, "max": 100}
    ]

class MonitorTest(unittest.TestCase):
    def test_all_edge_and_boundary_conditions(self):
        test_cases = [
            # All vitals within range
            (True, make_vitals(95, 60, 90)),     # Lower bounds
            (True, make_vitals(102, 100, 100)),  # Upper bounds
            (True, make_vitals(98.6, 70, 98)),   # Normal values

            # Just below lower bound
            (False, make_vitals(94.9, 60, 90)),  # Temp too low
            (False, make_vitals(95, 59.9, 90)),  # Pulse too low
            (False, make_vitals(95, 60, 89.9)),  # SpO2 too low

            # Just above upper bound
            (False, make_vitals(102.1, 60, 90)),  # Temp too high
            (False, make_vitals(95, 100.1, 90)),  # Pulse too high
            (False, make_vitals(95, 60, 100.1)),  # SpO2 too high

            # Multiple out-of-range
            (False, make_vitals(103, 101, 89)),   # All fail
            (False, make_vitals(94, 55, 98)),     # Temp and Pulse fail
            (False, make_vitals(98, 70, 85)),     # SpO2 only fail
        ]

        for expected, vitals in test_cases:
            with self.subTest(vitals=vitals):
                result = vitals_ok(vitals, printer=mock_printer, blinker=mock_blink)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
