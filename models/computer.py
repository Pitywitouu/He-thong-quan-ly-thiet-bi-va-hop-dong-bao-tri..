from __future__ import annotations

from typing import Optional, Union

try:
    from .device import Device, DeviceStatus
    from .networkable import INetworkable
except ImportError:
    from device import Device, DeviceStatus
    from networkable import INetworkable


class Computer(Device, INetworkable):
    def __init__(
        self,
        device_id,
        name,
        year_in_use,
        purchase_price,
        ram: Union[float, int],
        processor_type: str,
        has_discrete_gpu: bool,
        status: DeviceStatus = DeviceStatus.ACTIVE,
    ) -> None:
        super().__init__(device_id, name, year_in_use, purchase_price, status)
        self.ram = ram
        self.processor_type = processor_type
        self.has_discrete_gpu = has_discrete_gpu
        self._ip_address: Optional[str] = None
        self._is_connected: bool = False

    @property
    def ram(self) -> float:
        return self._ram

    @ram.setter
    def ram(self, value: Union[float, int]) -> None:
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Dung lượng RAM phải là số lớn hơn 0.")
        self._ram = float(value)

    @property
    def ram_capacity(self) -> float:
        return self._ram

    @ram_capacity.setter
    def ram_capacity(self, value: Union[float, int]) -> None:
        self.ram = value

    @property
    def processor_type(self) -> str:
        return self._processor_type

    @processor_type.setter
    def processor_type(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Loại bộ xử lý không được để trống.")
        self._processor_type = value.strip()

    @property
    def has_discrete_gpu(self) -> bool:
        return self._has_discrete_gpu

    @has_discrete_gpu.setter
    def has_discrete_gpu(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("has_discrete_gpu phải là giá trị boolean.")
        self._has_discrete_gpu = value

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

    def calculate_annual_maintenance_cost(self) -> float:
        base_rate = 0.05
        if self.has_discrete_gpu:
            gpu_rate = 0.02
        else:
            gpu_rate = 0.0

        if self.years_of_use > 5:
            age_rate = 0.01
        else:
            age_rate = 0.0
        return self.purchase_price * (base_rate + gpu_rate + age_rate)

    def __str__(self) -> str:
        if self._has_discrete_gpu:
            gpu_str = "Có GPU rời"
        else:
            gpu_str = "Không GPU rời"
        if self._is_connected:
            net_str = f"IP: {self._ip_address}"
        else:
            net_str = "Chưa kết nối"
        return (
            f"Computer(ID: {self._device_id}, Tên: '{self._name}', "
            f"Năm SD: {self._year_in_use}, Giá: {self._purchase_price:,.0f} VND, "
            f"RAM: {self._ram}GB, CPU: '{self._processor_type}', {gpu_str}, "
            f"Mạng: {net_str}, Trạng thái: {self._status.value})"
        )
