import functools


def map_frequency(text: str) -> dict[str, int]:
    words: list[str] = text.split(' ')
    frequency: dict = {}
    for word in words:
        if word in frequency:
            frequency[word] = frequency[word] + 1
        else:
            frequency[word] = 1
    return frequency


def merge_dictionaries(first: dict, second: dict) -> dict[str, int]:
    merged = first
    for key in second:
        if key in merged:
            merged[key] = merged[key] + second[key]
        else:
            merged[key] = second[key]
    return merged


if __name__ == '__main__':
    arr = ["I know what I know.",
           "I know that I know.",
           "I don't know that much.",
           "They don't know much."]

    mapped_result = [map_frequency(item) for item in arr]
    result = functools.reduce(merge_dictionaries, mapped_result)
    print(result)
