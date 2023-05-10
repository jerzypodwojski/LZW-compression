def encoder(data):
    maximum_table_size = 10000
    dictionary_size = 256

    dictionary = ({chr(i): i for i in range(0x0, 0x10ffff)})

    string = ""
    compressed_data = []

    for symbol in data:
        string_plus_symbol = string + symbol
        if string_plus_symbol in dictionary:
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if len(dictionary) <= maximum_table_size:
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = symbol

    if string in dictionary:
        compressed_data.append(dictionary[string])

    binary_data = ""
    max_bin_len = len(bin(max(compressed_data))[2:])
    if len(bin(max_bin_len)[2:]) < 8:
        binary_data += "0" * (8 - len(bin(max_bin_len)[2:])) + bin(max_bin_len)[2:]
    else:
        binary_data += bin(max_bin_len)[2:]

    for i in range(len(compressed_data)):
        binary_num = bin(compressed_data[i])[2:]
        if len(binary_num) < max_bin_len:
            binary_data += "0" * (max_bin_len - len(binary_num))
        binary_data += binary_num
    binary_data = bytearray(int(binary_data[i:i + 8], 2) for i in range(0, len(binary_data), 8))

    output_file = open("compressed_data.beka", "wb")
    output_file.write(binary_data)


def decoder(data, maxsize):
    dictionary_size = 256
    maximum_table_size = 10000

    dictionary = ({chr(i): i for i in range(0x0, 0x10ffff)})

    binary_data = ''.join(format(i, '08b') for i in data)

    data_array = []
    for i in range(0, len(binary_data), maxsize):
        binary = binary_data[i:i + maxsize]
        decimal = 0
        for digit in binary:
            decimal = decimal * 2 + int(digit)
        data_array.append(decimal)

    decompressed_data = ""
    string = ""

    dictionary = {v: k for k, v in dictionary.items()}
    for index in data_array:
        if index in dictionary:  # .values():
            entry = dictionary[index]
        elif index == dictionary_size:
            entry = string + string[0]
        else:
            raise ValueError("Invalid compressed data")
        decompressed_data += entry

        if len(string) > 0 and dictionary_size < maximum_table_size:
            dictionary[dictionary_size] = string + entry[0]
            dictionary_size += 1
        string = entry

    output_file = open("decompressed_data.txt", "w", encoding="utf-8")
    output_file.write(decompressed_data)


if __name__ == '__main__':
    open_file = open("pan-tadeusz.txt", encoding="utf-8")
    file_data = open_file.read()
    encoder(file_data)

    open_file = open("compressed_data.beka", "rb")
    bits_size = ord(open_file.read(1))
    file_data = open_file.read()
    decoder(file_data, bits_size)
