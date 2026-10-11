"""
MSSV: 202418985
Họ tên: Nguyễn Phú Thái
"""

from __future__ import annotations

from models.device import DeviceStatus
from models.computer import Computer
from models.printer import Printer, NetworkPrinter
from models.projector import Projector
from models.lab_room import LabRoom


def main():
    # 1. Khởi tạo các thiết bị
    computer1 = Computer("C01", "Dell OptiPlex 7010", 2021, 18000000, 16, "Intel Core i7", True)
    computer2 = Computer("C02", "HP ProDesk 400", 2019, 12000000, 8, "Intel Core i5", False)
    computer3 = Computer("C03", "Lenovo ThinkCentre M70", 2023, 15000000, 16, "AMD Ryzen 5", False)

    printer1 = Printer("P01", "HP LaserJet Pro M404", 2022, 5000000, "laser", 80000, False)
    printer2 = Printer("P02", "Canon PIXMA G3010", 2020, 4000000, "phun", 120000, True)

    net_printer = NetworkPrinter("NP01", "Epson WorkForce Pro WF-4820", 2021, 7000000, "phun", 110000, True)

    projector1 = Projector("PR01", "Panasonic PT-VMZ51", 2022, 20000000, 5200, 1200)
    projector2 = Projector("PR02", "Sony VPL-EX455", 2018, 16000000, 4000, 3500)

    print("              HỆ THỐNG QUẢN LÝ THIẾT BỊ PHÒNG THỰC HÀNH")

    # 2. Tạo hai phòng thực hành
    room_a = LabRoom("LA01", "Phòng Lab A - Lập trình", 30)
    room_b = LabRoom("LB01", "Phòng Lab B - Thiết kế mô phỏng", 25)

    print(f"\n[Khởi tạo] {room_a}")
    print(f"[Khởi tạo] {room_b}")

    # 3. Thêm thiết bị vào phòng
    room_a.add_device(computer1)
    room_a.add_device(computer2)
    room_a.add_device(printer1)
    room_a.add_device(net_printer)

    room_b.add_device(computer3)
    room_b.add_device(printer2)
    room_b.add_device(projector1)
    room_b.add_device(projector2)

    print(f"\n[Thêm thiết bị] {room_a}")
    print(f"[Thêm thiết bị] {room_b}")

    # 4. Kiểm tra mã thiết bị trùng
    print("\n--- Kiểm tra thêm thiết bị trùng mã ---")
    duplicate = Computer("C01", "Thiết bị trùng", 2024, 10000000, 8, "Intel Core i3", False)
    try:
        room_a.add_device(duplicate)
    except ValueError as e:
        print(f"[Lỗi dự kiến] {e}")

    # 5. In danh sách thiết bị
    print(f"\n--- Danh sách thiết bị trong {room_a.room_name} ---")
    for device in room_a.devices:
        print(f"  {device}")

    print(f"\n--- Danh sách thiết bị trong {room_b.room_name} ---")
    for device in room_b.devices:
        print(f"  {device}")

    # 6. Tính chi phí bảo trì
    print("\n--- Chi phí bảo trì hàng năm ---")
    cost_a = room_a.calculate_annual_maintenance_cost()
    cost_b = room_b.calculate_annual_maintenance_cost()
    print(f"  {room_a.room_name}: {cost_a:,.0f} VND")
    print(f"  {room_b.room_name}: {cost_b:,.0f} VND")
    print(f"  Tổng cộng (toàn trường): {cost_a + cost_b:,.0f} VND")

    # 7. Liệt kê thiết bị cần bảo trì
    print("\n--- Thiết bị cần bảo trì (dùng > 5 năm hoặc đang bảo trì) ---")
    computer2.status = DeviceStatus.UNDER_MAINTENANCE

    for room in [room_a, room_b]:
        needs_maintenance = room.get_devices_requiring_maintenance()
        if needs_maintenance:
            print(f"  [{room.room_name}]")
            for device in needs_maintenance:
                print(f"    - {device}")
        else:
            print(f"  [{room.room_name}]: Không có thiết bị nào cần bảo trì.")

    # 8. Kiểm tra kết nối mạng
    print("\n--- Kiểm tra kết nối mạng ---")

    computer1.connect("192.168.1.101")
    print(f"  Kết nối: {computer1.device_id} → IP: {computer1.ip_address}, Đã kết nối: {computer1.is_connected}")

    net_printer.connect("192.168.1.201")
    print(f"  Kết nối: {net_printer.device_id} → IP: {net_printer.ip_address}, Đã kết nối: {net_printer.is_connected}")

    try:
        computer1.connect("192.168.1.199")
    except ValueError as e:
        print(f"  [Lỗi dự kiến] {e}")

    computer1.disconnect()
    print(f"  Ngắt kết nối: {computer1.device_id} → Đã kết nối: {computer1.is_connected}")

    print("\n")
    print("              CHƯƠNG TRÌNH KẾT THÚC")


if __name__ == "__main__":
    main()
