import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial


def simple_count(num: int) -> int:
    print(f'simple_count run {num}')
    ct: int = 0
    while ct < num:
        ct += 1
    print(f'simple_count {num} end')
    return ct


async def main():
    print('run main')
    with ProcessPoolExecutor() as pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        nums = [1, 3, 10_000_000, 5, 10]
        calls: list[partial[int]] = [partial(simple_count, num) for num in nums]
        call_coros: list = []

        for call in calls:
            call_coros.append(loop.run_in_executor(pool, call))

        # results = await asyncio.gather(*call_coros)
        # for res in results:
        #     print(res)
        results = asyncio.as_completed(call_coros)
        for res in results:
            print(await res)

    print('END MAIN')

if __name__ == '__main__':
    asyncio.run(main())
