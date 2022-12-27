from multiprocessing import Process
import time


def simple_count(num: int) -> None:
    start = time.time()
    print('simple_count run')
    ct: int = 0
    while ct < num:
        ct += 1
    print('simple_count end: ', time.time() - start)


def main():
    start = time.time()
    print('run main')
    t1 = Process(target=simple_count, args=(100_000_000,))
    t2 = Process(target=simple_count, args=(100_000_000,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print('END MAIN: ', time.time() - start)


if __name__ == '__main__':
    main()