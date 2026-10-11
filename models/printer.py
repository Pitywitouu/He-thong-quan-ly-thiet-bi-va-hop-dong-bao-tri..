from __future__ import annotations

from typing import Optional, Union

try:
    from .device import Device, DeviceStatus
    from .networkable import INetworkable
except ImportError:
    from device import Device, DeviceStatus
    from networkable import INetworkable


class Printer(Device):
    def __init__(
        self,
        device_id,
        name,
        year_in_use,
        purchase_price,
        printer_type: str,
        pages_printed: int = 0,
        is_color: bool = False,
        status: DeviceStatus = DeviceStatus.ACTIVE,
    ) -> None:
        super().__init__(device_id, name, year_in_use, purchase_price, status)
        self.printer_type = printer_type
        self.pages_printed = pages_printed
        self.is_color = is_color

    @property
    def printer_type(self) -> str:
        return self._printer_type

    @printer_type.setter
    def printer_type(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Loại máy in không được để trống.")
        self._printer_type = value.strip()

    @property
    def pages_printed(self) -> int:
        return self._pages_printed

    @pages_printed.setter
    def pages_printed(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("Số trang đã in phải là số nguyên không âm.")
        self._pages_printed = value

    @property
    def is_color(self) -> bool:
        return self._is_color

    @is_color.setter
    def is_color(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("is_color phải là giá trị boolean.")
        self._is_color = value

    def calculate_annual_maintenance_cost(self) -> float:
        base_cost = 0.04 * self.purchase_price
        if self.pages_printed > 100000:
            pages_extra = 500000.0
        else:
            pages_extra = 0.0

        if self.is_color:
            color_extra = 300000.0
        else:
            color_extra = 0.0
        return base_cost + pages_extra + color_extra

    def __str__(self) -> str:
        if self._is_color:
            color_str = "In màu"
        else:
            color_str = "In trắng đen"
        return (
            f"Printer(ID: {self._device_id}, Tên: '{self._name}', "
            f"Năm SD: {self._year_in_use}, Giá: {self._purchase_price:,.0f} VND, "
            f"Loại: {self._printer_type}, Đã in: {self._pages_printed:,} trang, "
            f"{color_str}, Trạng thái: {self._status.value})"
        )


class NetworkPrinter(Printer, INetworkable):
    def __init__(
        self,
        device_id,
        name,
        year_in_use,
        purchase_price,
        printer_type,
        pages_printed,
        is_color,
        status: DeviceStatus = DeviceStatus.ACTIVE,
    ) -> None:
        super().__init__(device_id, name, year_in_use, purchase_price, printer_type, pages_printed, is_color, status)
        self._ip_address: Optional[str] = None
        self._is_connected: bool = False

    @property
    def ip_address(self) -> Optional[str]:
        return self._ip_address

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    def connect(self, ip_address: str) -> None:
        if not isinstance(ip_address, str) or not ip_address.strip():
            raise ValueError("Địa chỉ IP không được để trống.")
        if self._is_connected:
            raise ValueError("Không cho phép kết nối lại khi thiết bị đang kết nối.")
        self._ip_address = ip_address.strip()
        self._is_connected = True

    def disconnect(self) -> None:
        self._is_connected = False
        self._ip_address = None

    def __str__(self) -> str:
        if self._is_color:
            color_str = "In màu"
        else:
            color_str = "In trắng đen"
            
        if self._is_connected:
            net_str = f"IP: {self._ip_address}"
        else:
            net_str = "Chưa kết nối"
        return (
            f"NetworkPrinter(ID: {self._device_id}, Tên: '{self._name}', "
            f"Năm SD: {self._year_in_use}, Giá: {self._purchase_price:,.0f} VND, "
            f"Loại: {self._printer_type}, Đã in: {self._pages_printed:,} trang, "
            f"{color_str}, Mạng: {net_str}, Trạng thái: {self._status.value})"
        )
