import abc
from typing import Any, Protocol

from result import Err, Ok, Result


class MapperProtocol[TInput, TOutput, TError](Protocol):
    @abc.abstractmethod
    def decode(self, message: Any) -> TInput: ...  # noqa: ANN401

    async def validate(self, message: TInput) -> Result[None, TError]:  # noqa: ARG002
        return Ok(None)

    @abc.abstractmethod
    async def map(self, message: TInput) -> TOutput: ...

    async def process(self, message: Any) -> Result[TOutput, TError]:  # noqa: ANN401
        schema = self.decode(message)
        validation_result = await self.validate(schema)
        if isinstance(validation_result, Err):
            return validation_result
        return Ok(await self.map(schema))
