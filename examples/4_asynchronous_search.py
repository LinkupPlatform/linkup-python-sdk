"""
All Linkup entrypoints come with an asynchronous version. This snippet demonstrates how to run
multiple asynchronous searches concurrently, which decreases by a lot the total computation
duration.
"""

import asyncio
import time
from typing import List

from linkup import LinkupClient

client = LinkupClient()

queries: List[str] = [
    "What are the 3 major events in the life of Abraham Lincoln?",
    "What are the 3 major events in the life of George Washington?",
]

t0: float = time.time()


async def search(idx: int, query: str) -> None:
    """Run an asynchronous search and display its results and the duration from the beginning."""
    response = await client.async_search(
        query=query,
        depth="standard",  # or "deep"
        output_type="searchResults",  # or "sourcedAnswer" or "structured"
    )
    print(f"{idx+1}: {time.time() - t0:.3f}s")
    print(response)
    print("-" * 100)


async def main() -> None:
    """Run multiple asynchronous searches concurrently."""
    coroutines = [search(idx=idx, query=query) for idx, query in enumerate(queries)]
    await asyncio.gather(*coroutines)
    print(f"Total time: {time.time() - t0:.3f}s")


asyncio.run(main())
