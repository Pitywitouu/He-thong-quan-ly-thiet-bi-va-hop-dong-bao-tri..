import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.networkable import INetworkable
from models.computer import Computer
from models.printer import NetworkPrinter


class TestComputerNetwork(unittest.TestCase):
    def setUp(self):
        self.computer = Computer("C01", "PC Test", 2022, 10000000, 8, "Intel i5", False)

    def test_initial_state(self):
        self.assertFalse(self.computer.is_connected)
        self.assertIsNone(self.computer.ip_address)

    def test_connect_sets_ip(self):
        self.computer.connect("192.168.1.10")
        self.assertEqual(self.computer.ip_address, "192.168.1.10")

    def test_connect_sets_is_connected_true(self):
        self.computer.connect("192.168.1.10")
        self.assertTrue(self.computer.is_connected)

    def test_connect_strips_whitespace_ip(self):
        self.computer.connect("  192.168.1.10  ")
        self.assertEqual(self.computer.ip_address, "192.168.1.10")

    def test_disconnect_clears_ip(self):
        self.computer.connect("192.168.1.10")
        self.computer.disconnect()
        self.assertIsNone(self.computer.ip_address)

    def test_disconnect_sets_is_connected_false(self):
        self.computer.connect("192.168.1.10")
        self.computer.disconnect()
        self.assertFalse(self.computer.is_connected)

    def test_reconnect_after_disconnect(self):
        self.computer.connect("192.168.1.10")
        self.computer.disconnect()
        self.computer.connect("192.168.1.20")
        self.assertEqual(self.computer.ip_address, "192.168.1.20")
        self.assertTrue(self.computer.is_connected)

    def test_connect_empty_ip_raises(self):
        with self.assertRaises(ValueError):
            self.computer.connect("")

    def test_connect_whitespace_ip_raises(self):
        with self.assertRaises(ValueError):
            self.computer.connect("   ")

    def test_connect_when_already_connected_raises(self):
        self.computer.connect("192.168.1.10")
        with self.assertRaises(ValueError):
            self.computer.connect("192.168.1.99")

    def test_disconnect_when_not_connected(self):
        try:
            self.computer.disconnect()
        except Exception:
            self.fail("disconnect() raised exception khi chưa kết nối")


class TestNetworkPrinterNetwork(unittest.TestCase):
    def setUp(self):
        self.np = NetworkPrinter("NP01", "Epson", 2022, 7000000, "phun", 50000, False)

    def test_initial_state(self):
        self.assertFalse(self.np.is_connected)
        self.assertIsNone(self.np.ip_address)

    def test_connect_sets_ip(self):
        self.np.connect("10.0.0.50")
        self.assertEqual(self.np.ip_address, "10.0.0.50")
        self.assertTrue(self.np.is_connected)

    def test_disconnect_resets_state(self):
        self.np.connect("10.0.0.50")
        self.np.disconnect()
        self.assertFalse(self.np.is_connected)
        self.assertIsNone(self.np.ip_address)

    def test_double_connect_raises(self):
        self.np.connect("10.0.0.50")
        with self.assertRaises(ValueError):
            self.np.connect("10.0.0.51")

    def test_empty_ip_raises(self):
        with self.assertRaises(ValueError):
            self.np.connect("")


class TestINetworkableInterface(unittest.TestCase):
    def test_computer_is_instance_of_INetworkable(self):
        c = Computer("C01", "PC", 2022, 10000000, 8, "Intel i5", False)
        self.assertIsInstance(c, INetworkable)

    def test_network_printer_is_instance_of_INetworkable(self):
        np = NetworkPrinter("NP01", "Epson", 2022, 7000000, "phun", 50000, False)
        self.assertIsInstance(np, INetworkable)

    def test_INetworkable_is_abstract(self):
        with self.assertRaises(TypeError):
            INetworkable()


if __name__ == "__main__":
    unittest.main()
