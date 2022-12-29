import asyncio
import concurrent.futures
import functools
import time


def partition(data: list, chunk_size: int) -> list:
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def map_frequencies(chunk: list[str]) -> dict[str, int]:
    counter: dict = {}
    for line in chunk:
        word, _, count, _ = line.split('\t')
        if counter.get(word):
            counter[word] = counter[word] + int(count)
        else:
            counter[word] = int(count)
    return counter


def merge_dictionaries(first: dict[str, int], second: dict[str, int]) -> dict[str, int]:
    merged = first
    for key in second:
        if merged.get(key):
            merged[key] = merged[key] + second[key]
        else:
            merged[key] = second[key]
    return merged


async def reduce(loop, pool, counters, chunk_size) -> dict[str, int]:
    chunks: list[list[dict]] = list(partition(counters, chunk_size))
    reducers: list = []
    while len(chunks[0]) > 1:
        for chunk in chunks:
            reduce = functools.partial(functools.reduce, merge_dictionaries, chunk)
            reducers.append(loop.run_in_executor(pool, reduce))
        reduce_chunks = await asyncio.gather(*reducers)
        chunks = list(partition(reduce_chunks, chunk_size))
        reducers.clear()
    return chunks[0][0]


async def main(partition_size: int):
    with open('googlebooks', encoding='utf-8') as f:
        content = f.readlines()
        loop = asyncio.get_running_loop()
        tasks: list = []

        with concurrent.futures.ProcessPoolExecutor() as pool:
            start = time.time()
            for chunk in partition(content, partition_size):
                tasks.append(loop.run_in_executor(pool, functools.partial(map_frequencies, chunk)))

            intermediate_results = await asyncio.gather(*tasks)
            final_result = await reduce(loop, pool, intermediate_results, 500)

            print(f"Aardvark has appeared {final_result['Aardvark']} times.")
        end = time.time()
        print(f'Time run: {end-start}')


if __name__ == '__main__':
    asyncio.run(main(partition_size=60_000))
