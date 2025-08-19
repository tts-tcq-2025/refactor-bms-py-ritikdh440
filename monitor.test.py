import unittest
from monitor import vitals_ok

printed = []
blinks = 0

def reset_mocks():
    global printed, blinks
    printed = []
    blinks = 0

def mock_printer(msg):
    global printed
    printed.append(msg)

def mock_blink():
    global blinks
    blinks += 1

def make_vitals(temp, pulse, spo2):
    return [
        {"name": "temperature", "value": temp, "min": 95, "max": 102},
        {"name": "pulse", "value": pulse, "min": 60, "max": 100},
        {"name": "spo2", "value": spo2, "min": 90, "max": 100}
    ]

class MonitorTest(unittest.TestCase):
    def test_all_edge_and_boundary_conditions(self):
        test_cases = [
            (True, make_vitals(95, 60, 90)),      # Lower bounds
            (True, make_vitals(102, 100, 100)),   # Upper bounds
            (True, make_vitals(98.6, 70, 98)),    # Normal values

            (False, make_vitals(94.9, 60, 90)),   # Temp too low
            (False, make_vitals(95, 59.9, 90)),   # Pulse too low
            (False, make_vitals(95, 60, 89.9)),   # SpO2 too low

            (False, make_vitals(102.1, 60, 90)),  # Temp too high
            (False, make_vitals(95, 100.1, 90)),  # Pulse too high
            (False, make_vitals(95, 60, 100.1)),  # SpO2 too high

            (False, make_vitals(103, 101, 89)),   # All fail
            (False, make_vitals(94, 55, 98)),     # Temp and Pulse fail
            (False, make_vitals(98, 70, 85)),     # SpO2 fail
        ]

        for expected, vitals in test_cases:
            with self.subTest(vitals=vitals):
                reset_mocks()
                result = vitals_ok(vitals, printer=mock_printer, blinker=mock_blink)
                self.assertEqual(result, expected)

    # --- New tests for Extension 1 (Early Warning) ---
    def test_warning_low_band(self):
        reset_mocks()
        vitals = make_vitals(95.5, 70, 95)
        ok = vitals_ok(vitals, printer=mock_printer, blinker=mock_blink)
        self.assertTrue(ok)
        self.assertTrue(any("Approaching low" in m for m in printed))
        self.assertEqual(blinks, 0)

    def test_warning_high_band(self):
        reset_mocks()
        vitals = make_vitals(101.0, 70, 95)
        ok = vitals_ok(vitals, printer=mock_printer, blinker=mock_blink)
        self.assertTrue(ok)
        self.assertTrue(any("Approaching high" in m for m in printed))
        self.assertEqual(blinks, 0)

    def test_critical_still_blinks(self):
        reset_mocks()
        vitals = make_vitals(102.1, 70, 95)
        ok = vitals_ok(vitals, printer=mock_printer, blinker=mock_blink)
        self.assertFalse(ok)
        self.assertTrue(any("CRITICAL" in m for m in printed))
        self.assertGreater(blinks, 0)

if __name__ == '__main__':
    unittest.main()
