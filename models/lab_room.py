from __future__ import annotations

from typing import Optional

try:
    from .device import Device, DeviceStatus
except ImportError:
    from device import Device, DeviceStatus


class LabRoom:
    def __init__(
        self,
        room_id: str,
        room_name: str,
        capacity: int,
        devices: Optional[list[Device]] = None,
    ) -> None:
        if not isinstance(room_id, str) or not room_id.strip():
            raise ValueError("Mã phòng không được để trống.")
        self._room_id = room_id.strip()

        self.room_name = room_name
        self.capacity = capacity
        self._devices: list[Device] = []

        if devices:
            for device in devices:
                self.add_device(device)

    @property
    def room_id(self) -> str:
        return self._room_id

    @property
    def room_name(self) -> str:
        return self._room_name

    @room_name.setter
    def room_name(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Tên phòng không được để trống.")
        self._room_name = value.strip()

    @property
    def capacity(self) -> int:
        return self._capacity

    @capacity.setter
    def capacity(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Sức chứa phòng phải là số nguyên lớn hơn 0.")
        self._capacity = value

    @property
    def devices(self) -> list[Device]:
        return list(self._devices)

    def add_device(self, device: Device) -> None:
        if device is None or not isinstance(device, Device):
            raise ValueError("Không chấp nhận đối tượng thiết bị null hoặc không hợp lệ.")
        if self.find_device(device.device_id) is not None:
            raise ValueError(f"Thiết bị có mã '{device.device_id}' đã tồn tại trong phòng.")
        self._devices.append(device)

    def remove_device(self, device_id: str) -> bool:
        device = self.find_device(device_id)
        if device is not None:
            self._devices.remove(device)
            return True
        return False

    def find_device(self, device_id: str) -> Optional[Device]:
        for device in self._devices:
            if device.device_id == device_id:
                return device
        return None

    def calculate_annual_maintenance_cost(self) -> float:
        return sum(device.calculate_annual_maintenance_cost() for device in self._devices)

    def get_devices_requiring_maintenance(self) -> list[Device]:
        return [
            device
            for device in self._devices
            if device.status == DeviceStatus.UNDER_MAINTENANCE or device.years_of_use > 5
        ]

    def __str__(self) -> str:
        return (
            f"LabRoom(Mã: '{self._room_id}', Tên: '{self._room_name}', "
            f"Sức chứa: {self._capacity}, Số thiết bị: {len(self._devices)})"
        )
