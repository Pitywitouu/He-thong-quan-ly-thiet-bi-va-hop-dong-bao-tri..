from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class INetworkable(ABC):
    @property
    @abstractmethod
    def ip_address(self) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        pass

    @abstractmethod
    def connect(self, ip_address: str) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass
