import unittest
from monitor import vitals_ok

def mock_printer(msg):
    pass

def mock_blink():
    pass

class MonitorTest(unittest.TestCase):

    def test_all_vitals_normal_should_pass(self):
        vitals = [
            {"name": "temperature", "value": 98.6, "min": 95, "max": 102},
            {"name": "pulse", "value": 70, "min": 60, "max": 100},
            {"name": "spo2", "value": 98, "min": 90, "max": 100}
        ]
        self.assertTrue(vitals_ok(vitals, printer=mock_printer, blinker=mock_blink))

    def test_temperature_too_low_should_fail(self):
        vitals = [
            {"name": "temperature", "value": 94, "min": 95, "max": 102},
            {"name": "pulse", "value": 70, "min": 60, "max": 100},
            {"name": "spo2", "value": 98, "min": 90, "max": 100}
        ]
        self.assertFalse(vitals_ok(vitals, printer=mock_printer, blinker=mock_blink))

    def test_temperature_too_high_should_fail(self):
        vitals = [
            {"name": "temperature", "value": 104, "min": 95, "max": 102},
            {"name": "pulse", "value": 70, "min": 60, "max": 100},
            {"name": "spo2", "value": 98, "min": 90, "max": 100}
        ]
        self.assertFalse(vitals_ok(vitals, printer=mock_printer, blinker=mock_blink))

    def test_pulse_too_low_should_fail(self):
        vitals = [
            {"name": "temperature", "value": 98.6, "min": 95, "max": 102},
            {"name": "pulse", "value": 50, "min": 60, "max": 100},
            {"name": "spo2", "value": 98, "min": 90, "max": 100}
        ]
        self.assertFalse(vitals_ok(vitals, printer=mock_printer, blinker=mock_blink))

    def test_pulse_too_high_should_fail(self):
        vitals = [
            {"name": "temperature", "value": 98.6, "min": 95, "max": 102},
            {"name": "pulse", "value": 105, "min": 60, "max": 100},
            {"name": "spo2", "value": 98, "min": 90, "max": 100}
        ]
        self.assertFalse(vitals_ok(vitals, printer=mock_printer, blinker=mock_blink))

    def test_spo2_too_low_should_fail(self):
        vitals = [
            {"name": "temperature", "value": 98.6, "min": 95, "max": 102},
            {"name": "pulse", "value": 70, "min": 60, "max": 100},
            {"name": "spo2", "value": 85, "min": 90, "max": 100}
        ]
        self.assertFalse(vitals_ok(vitals, printer=mock_printer, blinker=mock_blink))

    def test_multiple_vitals_out_of_range_should_fail(self):
        vitals = [
            {"name": "temperature", "value": 104, "min": 95, "max": 102},
            {"name": "pulse", "value": 50, "min": 60, "max": 100},
            {"name": "spo2", "value": 85, "min": 90, "max": 100}
        ]
        self.assertFalse(vitals_ok(vitals, printer=mock_printer, blinker=mock_blink))

    def test_boundary_values_should_pass(self):
        vitals = [
            {"name": "temperature", "value": 95, "min": 95, "max": 102},
            {"name": "pulse", "value": 60, "min": 60, "max": 100},
            {"name": "spo2", "value": 90, "min": 90, "max": 100}
        ]
        self.assertTrue(vitals_ok(vitals, printer=mock_printer, blinker=mock_blink))

if __name__ == '__main__':
    unittest.main()
