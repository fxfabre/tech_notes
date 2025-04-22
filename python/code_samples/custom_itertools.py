from typing import Iterable, List, TypeVar

T = TypeVar("T")


class TakeChunk:
    def __init__(self, iterable: Iterable[T], chunk_size: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.iterator = iter(iterable)
        self.chunk_size = chunk_size
        if self.chunk_size < 1:
            raise ValueError("chunk size must be >= 1")

    def __iter__(self) -> Iterable[List[T]]:
        finished = False
        while not finished:
            chunk = []
            for _ in range(self.chunk_size):
                try:
                    item = next(self.iterator)
                    chunk.append(item)
                except StopIteration:
                    finished = True
                    break
            if len(chunk) > 0:
                yield chunk


def take_chunk(iterable: Iterable[T], chunk_size: int = 1) -> TakeChunk:
    return TakeChunk(iterable, chunk_size)
