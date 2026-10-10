from __future__ import annotations

from typing import Union

try:
    from .device import Device, DeviceStatus
except ImportError:
    from device import Device, DeviceStatus


class Projector(Device):
    def __init__(
        self,
        device_id,
        name,
        year_in_use,
        purchase_price,
        brightness_lumens: int,
        lamp_hours_used: Union[float, int] = 0.0,
        status: DeviceStatus = DeviceStatus.ACTIVE,
    ) -> None:
        super().__init__(device_id, name, year_in_use, purchase_price, status)
        self.brightness_lumens = brightness_lumens
        self.lamp_hours_used = lamp_hours_used

    @property
    def brightness_lumens(self) -> int:
        return self._brightness_lumens

    @brightness_lumens.setter
    def brightness_lumens(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Độ sáng lumen phải là số nguyên lớn hơn 0.")
        self._brightness_lumens = value

    @property
    def lamp_hours_used(self) -> float:
        return self._lamp_hours_used

    @lamp_hours_used.setter
    def lamp_hours_used(self, value: Union[float, int]) -> None:
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Số giờ sử dụng bóng đèn phải là số không âm.")
        self._lamp_hours_used = float(value)

    def calculate_annual_maintenance_cost(self) -> float:
        base_cost = 0.03 * self.purchase_price
        if self.lamp_hours_used > 3000:
            lamp_extra = 1500000.0
        else:
            lamp_extra = 0.0
        return base_cost + lamp_extra

    def __str__(self) -> str:
        return (
            f"Projector(ID: {self._device_id}, Tên: '{self._name}', "
            f"Năm SD: {self._year_in_use}, Giá: {self._purchase_price:,.0f} VND, "
            f"Độ sáng: {self._brightness_lumens} lumens, Giờ đèn: {self._lamp_hours_used:,.1f}h, "
            f"Trạng thái: {self._status.value})"
        )
