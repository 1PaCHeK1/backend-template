import abc
from typing import Protocol

from result import Result


class WorkerProtocol[TInput, TResult, TError](Protocol):
    @abc.abstractmethod
    async def process(self, message: TInput) -> Result[TResult, TError]: ...
