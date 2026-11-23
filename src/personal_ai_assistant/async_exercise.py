import asyncio
import time

async def fetch_response(model_name: str, delay: float) -> str:
    print(f"Starting {model_name}")

    await asyncio.sleep(delay)

    print(f"Finished {model_name}")
    return f"{model_name} response ready"


async def main() -> None:
    start = time.perf_counter()

    try:
        async with asyncio.timeout(2):
            response = await fetch_response("OpenAI", 5)
            print(response)

    except TimeoutError:
        print("OpenAI request timed out")

    elapsed = time.perf_counter() - start
    print(f"Total time: {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
