import asyncio
from collections.abc import AsyncIterator

async def generate_words() -> AsyncIterator[str]:
    words = [
        "Hello",
        "from",
        "your",
        "AI",
        "assistant!",
    ]

    for word in words:
        await asyncio.sleep(0.3)
        yield word + " "


async def main() -> None:
    async for chunk in generate_words():
        print(chunk, end="", flush=True)

    print()


if __name__ == "__main__":
    asyncio.run(main())
