import abc
from typing import Protocol

from result import Result


class WorkerProtocol[TInput](Protocol):
    @abc.abstractmethod
    async def process(self, message: TInput) -> Result[None, Exception]: ...
