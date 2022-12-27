from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process
import time


def simple_count(num: int) -> None:
    start = time.time()
    print('simple_count run')
    ct: int = 0
    while ct < num:
        ct += 1
    print('simple_count end: ', time.time() - start)
    return ct


def main():
    start = time.time()
    print('run main')
    with ProcessPoolExecutor() as pool:
        arr = [1, 3, 5, 10, 10_000_000]
        for result in pool.map(simple_count, arr):
            print(result)

    print('END MAIN: ', time.time() - start)


if __name__ == '__main__':
    main()