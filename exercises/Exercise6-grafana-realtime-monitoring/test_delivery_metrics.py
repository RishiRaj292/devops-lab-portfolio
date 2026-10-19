import unittest
from unittest.mock import patch
import delivery_metrics as metrics


class DeliveryMetricsTests(unittest.TestCase):
    @patch("delivery_metrics.random.uniform", return_value=25.0)
    @patch("delivery_metrics.random.randint", side_effect=[12, 7, 40])
    def test_simulate_delivery_updates_metrics(self, _randint, _uniform):
        metrics.simulate_delivery()
        self.assertEqual(metrics.total_deliveries._value.get(), 59)
        self.assertEqual(metrics.pending_deliveries._value.get(), 12)
        self.assertEqual(metrics.on_the_way_deliveries._value.get(), 7)


if __name__ == "__main__":
    unittest.main()
