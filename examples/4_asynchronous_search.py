"""Example of asynchronous search.

All Linkup entrypoints come with an asynchronous version. This snippet demonstrates how to run
multiple asynchronous searches concurrently, which decreases by a lot the total computation
duration.

To use this script, copy the `.env.example` file at the root of the repository inside a `.env`, and
fill the missing values, or pass a Linkup API key to the `LinkupClient` initialization.
"""

import asyncio
import time

import rich
from dotenv import load_dotenv

from linkup import LinkupClient

load_dotenv()
client = LinkupClient()

queries: list[str] = [
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
    print(f"{idx + 1}: {time.time() - t0:.3f}s")
    rich.print(response)
    print("-" * 100)


async def main() -> None:
    """Run multiple asynchronous searches concurrently."""
    coroutines = [search(idx=idx, query=query) for idx, query in enumerate(queries)]
    await asyncio.gather(*coroutines)
    print(f"Total time: {time.time() - t0:.3f}s")


asyncio.run(main())
