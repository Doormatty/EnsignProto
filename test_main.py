import random

import pytest

from main import Ensign


def create_random_data(max_elements=16):
    retval = []
    for element in range(random.randint(1, max_elements)):
        bit_width = random.randint(1, 10)
        if random.randint(0, 1):
            retval.append(([random.getrandbits(bit_width) for _ in range(random.randint(1, max_elements))], bit_width))
        else:
            retval.append((random.getrandbits(bit_width), bit_width))
    return retval


def decode_test(data: list[tuple[int | list, int]], encoded_data: str) -> list[tuple[int | list, int]]:
    retval = []
    ensign = Ensign()
    ensign.load_data(encoded_data)

    for element in data:
        if isinstance(element[0], int):
            # Decode an integer with the specified bit width
            decoded_value = ensign.decode_int(element[1])
            retval.append((decoded_value, element[1]))
        elif isinstance(element[0], list):
            # Decode a list with the specified bit width per item
            decoded_list = ensign.decode_list(len(element[0]), element[1])
            retval.append((decoded_list, element[1]))
    return retval


@pytest.mark.parametrize("data", [create_random_data() for _ in range(50)], ids=lambda x: f"{Ensign.encode(x)}")
def test_random_encode_decode(data):
    ensign = Ensign()
    result = decode_test(data=data, encoded_data=ensign.encode(data))
    assert data == result

@pytest.mark.parametrize("data", [
    ([(321, 8), ([5, 2, 3, 4], 4)]),
    ([(0, 8), ([1, 2, 3, 4, 3, 2, -1, 2, 3, 4, 3, 2, 1], 4)]),
    ([(2, 1), ([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1], 1)]),
], ids=lambda x: f"{x}")
def test_invalid_data(data):
    ensign = Ensign()
    with pytest.raises(ValueError):
        ensign.encode(data=data)