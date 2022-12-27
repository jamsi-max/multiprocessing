import multiprocessing
from multiprocessing import Pool

def f(name):
    return f'Hello {name}'

def main():
    with Pool() as pool:
        j = pool.apply_async(f, args=('John',))
        l = pool.apply_async(f, args=('Liza',))
        print(j.get())
        print(l.get())


if __name__ == '__main__':
    main()
    # print(multiprocessing.get_context())