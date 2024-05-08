import base64


class Ensign:
    def __init__(self):
        self.buffer = bytearray()
        self.bit_pos = 0  # Used for decoding

    def encode_int(self, value, bits):
        if bits < 1 or bits > 16:
            raise ValueError("Bits must be between 1 and 16.")
        max_value = (1 << bits) - 1
        if value < 0 or value > max_value:
            raise ValueError(f"Value must be between 0 and {max_value}")

        bits_remaining = bits
        while bits_remaining > 0:
            byte_index = self.bit_pos // 8
            bit_index = self.bit_pos % 8
            if byte_index >= len(self.buffer):  # Ensure the buffer is large enough
                self.buffer.append(0)

            bits_in_this_byte = min(bits_remaining, 8 - bit_index)
            mask = (1 << bits_in_this_byte) - 1
            bits_to_store = (value >> (bits_remaining - bits_in_this_byte)) & mask

            self.buffer[byte_index] |= bits_to_store << (8 - bit_index - bits_in_this_byte)
            self.bit_pos += bits_in_this_byte
            bits_remaining -= bits_in_this_byte

    def encode_list(self, lst, bits_per_item):
        for item in lst:
            self.encode_int(item, bits_per_item)

    def get_encoded_data(self):
        return base64.b85encode(self.buffer).decode('ascii')

    def load_data(self, encoded_data):
        self.buffer = bytearray(base64.b85decode(encoded_data))
        self.bit_pos = 0

    def decode_int(self, bits):
        value = 0
        bits_collected = 0

        while bits_collected < bits:
            byte_pos = self.bit_pos // 8
            bit_offset = self.bit_pos % 8
            bits_left_in_byte = 8 - bit_offset

            bits_to_read = min(bits - bits_collected, bits_left_in_byte)
            mask = (1 << bits_to_read) - 1
            shifted_bits = self.buffer[byte_pos] >> (bits_left_in_byte - bits_to_read)
            extracted_bits = shifted_bits & mask

            value = (value << bits_to_read) | extracted_bits
            self.bit_pos += bits_to_read
            bits_collected += bits_to_read

            if bit_offset + bits_to_read == 8 and bits_collected < bits:
                self.bit_pos = (byte_pos + 1) * 8  # Move to the next byte

        return value

    def decode_list(self, length, bits_per_item):
        return [self.decode_int(bits_per_item) for _ in range(length)]

    @staticmethod
    def encode(data: list[tuple[int | list, int]]) -> str:
        ensign = Ensign()
        for element in data:
            if isinstance(element[0], int):
                ensign.encode_int(element[0], element[1])
            elif isinstance(element[0], list):
                ensign.encode_list(element[0], element[1])
        return ensign.get_encoded_data()



if __name__ == "__main__":
    example = [(128, 8), ([1, 2, 3, 4], 4)]
    x = encode(example)
    y = decode(example, x)
    assert example == y
