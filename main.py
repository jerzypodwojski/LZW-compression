def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key


def encoder(data):
    dictionary_size = 256
    max_dictionary_size = 5000
    dictionary = dict({chr(i): i for i in range(0, dictionary_size)})

    string = ""
    compressed_data = []
    for symbol in data:
        string_plus_symbol = string + symbol
        if string_plus_symbol in dictionary:
            string = string_plus_symbol
        else:
            if dictionary_size < max_dictionary_size:
                dictionary_size += 1
                dictionary[string_plus_symbol] = dictionary_size
            compressed_data.append(dictionary[string_plus_symbol[:-1]])
            string = string_plus_symbol[-1]

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
    max_dictionary_size = 5000
    dictionary = ({chr(i): i for i in range(0, dictionary_size)})

    binary_data = ''.join(format(i, '08b') for i in data)

    data_array = []
    for i in range(0, len(binary_data), maxsize):
        binary = binary_data[i:i + maxsize]
        decimal = 0
        for digit in binary:
            decimal = decimal * 2 + int(digit)
        data_array.append(decimal)

    decompressed_data = ""
    second_num = data_array[0]
    for i in data_array:
        first_num = i
        if first_num in dictionary.values():
            new_entry = get_key(first_num, dictionary)
            new_entry2 = get_key(second_num, dictionary)
            decompressed_data += new_entry
            if dictionary_size < max_dictionary_size:
                dictionary[new_entry2 + new_entry[0]] = dictionary_size
                dictionary_size += 1
        else:
            new_entry = get_key(second_num, dictionary) + get_key(second_num, dictionary)[0]
            decompressed_data += new_entry
            if dictionary_size < max_dictionary_size:
                dictionary[new_entry] = dictionary_size
                dictionary_size += 1
        second_num = first_num

    decompressed_data = eval("b'" + decompressed_data + "'")
    output_file = open("decompressed_data.txt", "wb")
    output_file.write(decompressed_data)


if __name__ == '__main__':
    open_file = open("pan-tadeusz.txt", "rb")
    file_data = open_file.read()
    encoder(str(file_data)[2:-1])

    open_file = open("compressed_data.beka", "rb")
    bits_size = ord(open_file.read(1))
    file_data = open_file.read()
    decoder(file_data, bits_size)
