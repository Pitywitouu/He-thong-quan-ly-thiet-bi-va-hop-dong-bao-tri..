import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.device import DeviceStatus
from models.computer import Computer
from models.printer import Printer, NetworkPrinter
from models.projector import Projector
from models.lab_room import LabRoom


class TestComputerMaintenanceCost(unittest.TestCase):
    def test_no_gpu_no_age(self):
        # G=0, T=0: C = P * 0.05
        c = Computer("C01", "PC", 2024, 10000000, 8, "Intel i5", False)
        self.assertAlmostEqual(c.calculate_annual_maintenance_cost(), 500000.0)

    def test_with_gpu_no_age(self):
        # G=1, T=0: C = P * 0.07
        c = Computer("C02", "PC", 2024, 10000000, 8, "Intel i7", True)
        self.assertAlmostEqual(c.calculate_annual_maintenance_cost(), 700000.0)

    def test_no_gpu_with_age(self):
        # G=0, T=1 (dùng > 5 năm): C = P * 0.06
        c = Computer("C03", "PC", 2018, 10000000, 8, "Intel i5", False)
        self.assertAlmostEqual(c.calculate_annual_maintenance_cost(), 600000.0)

    def test_with_gpu_with_age(self):
        # G=1, T=1: C = P * 0.08
        c = Computer("C04", "PC", 2018, 10000000, 8, "Intel i7", True)
        self.assertAlmostEqual(c.calculate_annual_maintenance_cost(), 800000.0)

    def test_exactly_5_years_no_age_bonus(self):
        from datetime import datetime
        year_5_ago = datetime.now().year - 5
        c = Computer("C05", "PC", year_5_ago, 10000000, 8, "Intel i5", False)
        self.assertAlmostEqual(c.calculate_annual_maintenance_cost(), 500000.0)

    def test_6_years_triggers_age_bonus(self):
        from datetime import datetime
        year_6_ago = datetime.now().year - 6
        c = Computer("C06", "PC", year_6_ago, 10000000, 8, "Intel i5", False)
        self.assertAlmostEqual(c.calculate_annual_maintenance_cost(), 600000.0)


class TestPrinterMaintenanceCost(unittest.TestCase):
    def test_base_cost_only(self):
        # Ip=0, Ic=0: C = 0.04 * 5,000,000 = 200,000
        p = Printer("P01", "HP", 2022, 5000000, "laser", 50000, False)
        self.assertAlmostEqual(p.calculate_annual_maintenance_cost(), 200000.0)

    def test_pages_extra(self):
        # Ip=1 (>100000 trang), Ic=0: C = 200,000 + 500,000 = 700,000
        p = Printer("P02", "HP", 2022, 5000000, "laser", 150000, False)
        self.assertAlmostEqual(p.calculate_annual_maintenance_cost(), 700000.0)

    def test_color_extra(self):
        # Ip=0, Ic=1: C = 200,000 + 300,000 = 500,000
        p = Printer("P03", "Canon", 2022, 5000000, "phun", 50000, True)
        self.assertAlmostEqual(p.calculate_annual_maintenance_cost(), 500000.0)

    def test_pages_and_color_extra(self):
        # Ip=1, Ic=1: C = 200,000 + 500,000 + 300,000 = 1,000,000
        p = Printer("P04", "Epson", 2022, 5000000, "phun", 150000, True)
        self.assertAlmostEqual(p.calculate_annual_maintenance_cost(), 1000000.0)

    def test_exactly_100000_pages_no_extra(self):
        # Đúng 100,000 trang không tính thêm (điều kiện > 100000)
        p = Printer("P05", "HP", 2022, 5000000, "laser", 100000, False)
        self.assertAlmostEqual(p.calculate_annual_maintenance_cost(), 200000.0)

    def test_network_printer_inherits_cost_formula(self):
        np = NetworkPrinter("NP01", "Epson", 2022, 5000000, "phun", 150000, True)
        self.assertAlmostEqual(np.calculate_annual_maintenance_cost(), 1000000.0)


class TestProjectorMaintenanceCost(unittest.TestCase):
    def test_base_cost_only(self):
        # Il=0 (<= 3000 giờ): C = 0.03 * 10,000,000 = 300,000
        pr = Projector("PR01", "Sony", 2022, 10000000, 3000, 1500)
        self.assertAlmostEqual(pr.calculate_annual_maintenance_cost(), 300000.0)

    def test_lamp_extra(self):
        # Il=1 (> 3000 giờ): C = 300,000 + 1,500,000 = 1,800,000
        pr = Projector("PR02", "Panasonic", 2022, 10000000, 4000, 3500)
        self.assertAlmostEqual(pr.calculate_annual_maintenance_cost(), 1800000.0)

    def test_exactly_3000_hours_no_extra(self):
        pr = Projector("PR03", "Sony", 2022, 10000000, 3500, 3000)
        self.assertAlmostEqual(pr.calculate_annual_maintenance_cost(), 300000.0)

    def test_3001_hours_triggers_extra(self):
        pr = Projector("PR04", "Sony", 2022, 10000000, 3500, 3001)
        self.assertAlmostEqual(pr.calculate_annual_maintenance_cost(), 1800000.0)


class TestLabRoomMaintenanceCost(unittest.TestCase):
    def test_empty_room_cost_is_zero(self):
        room = LabRoom("R01", "Phòng A", 30)
        self.assertAlmostEqual(room.calculate_annual_maintenance_cost(), 0.0)

    def test_total_is_sum_of_devices(self):
        room = LabRoom("R01", "Phòng A", 30)
        c = Computer("C01", "PC", 2024, 10000000, 8, "Intel i5", False)  
        p = Printer("P01", "HP", 2022, 5000000, "laser", 50000, False)   
        room.add_device(p)
        expected = c.calculate_annual_maintenance_cost() + p.calculate_annual_maintenance_cost()
        self.assertAlmostEqual(room.calculate_annual_maintenance_cost(), expected)


class TestGetDevicesRequiringMaintenance(unittest.TestCase):
    def setUp(self):
        self.room = LabRoom("R01", "Phòng A", 30)

    def test_empty_room_returns_empty(self):
        result = self.room.get_devices_requiring_maintenance()
        self.assertEqual(result, [])

    def test_active_new_device_not_included(self):
        c = Computer("C01", "PC", 2024, 10000000, 8, "Intel i5", False)
        self.room.add_device(c)
        result = self.room.get_devices_requiring_maintenance()
        self.assertEqual(result, [])

    def test_device_with_under_maintenance_status_included(self):
        c = Computer("C01", "PC", 2024, 10000000, 8, "Intel i5", False)
        c.status = DeviceStatus.UNDER_MAINTENANCE
        self.room.add_device(c)
        result = self.room.get_devices_requiring_maintenance()
        self.assertIn(c, result)

    def test_device_older_than_5_years_included(self):
        c = Computer("C01", "PC", 2018, 10000000, 8, "Intel i5", False)
        self.room.add_device(c)
        result = self.room.get_devices_requiring_maintenance()
        self.assertIn(c, result)

    def test_device_exactly_5_years_not_included(self):
        from datetime import datetime
        year_5_ago = datetime.now().year - 5
        c = Computer("C01", "PC", year_5_ago, 10000000, 8, "Intel i5", False)
        self.room.add_device(c)
        result = self.room.get_devices_requiring_maintenance()
        self.assertNotIn(c, result)

    def test_retired_active_device_not_included(self):
        c = Computer("C01", "PC", 2024, 10000000, 8, "Intel i5", False)
        c.status = DeviceStatus.RETIRED
        self.room.add_device(c)
        result = self.room.get_devices_requiring_maintenance()
        self.assertNotIn(c, result)

    def test_mixed_devices(self):
        old_pc = Computer("C01", "Old PC", 2018, 10000000, 8, "Intel i5", False)
        new_pc = Computer("C02", "New PC", 2024, 10000000, 8, "Intel i5", False)
        broken = Printer("P01", "Broken Printer", 2023, 5000000, "laser", 0, False)
        broken.status = DeviceStatus.UNDER_MAINTENANCE

        self.room.add_device(old_pc)
        self.room.add_device(new_pc)
        self.room.add_device(broken)

        result = self.room.get_devices_requiring_maintenance()
        self.assertIn(old_pc, result)
        self.assertIn(broken, result)
        self.assertNotIn(new_pc, result)


if __name__ == "__main__":
    unittest.main()
