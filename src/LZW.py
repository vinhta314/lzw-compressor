import math


class Compressor:
    """
    Compresses text files using the LZW algorithm.
    Maximum code table size is set to the 4096 entries (12 bit codes).
    """
    def __init__(self, text_filepath):
        self._code_table = None
        self._next_code = None
        self._max_code = 4096
        self._text = self._read_file(text_filepath)
        self.encoded_text = self._lzw_compress()
        self.compression_ratio = self._calculate_compression_ratio()

    def save_file(self, save_filepath):
        """
        Converts the 12 bit encoded text to a byte stream and save to a compressed file (.z type).
        """
        encoded_bytes = self._encode_to_bytes()

        assert save_filepath.lower().endswith('.z'), 'Saved file must have the file extension *.z'

        with open(save_filepath, 'w+b') as file:
            file.write(encoded_bytes)

    def _lzw_compress(self):
        """
        Encodes the text using the LZW algorithm.
        """
        self._initialise_code_table()

        encoded_text = []

        i = 0
        output_word = self._text[0]

        while i < len(self._text):
            next_char = self._get_next_char(i)
            if output_word + next_char in self._code_table:
                output_word = output_word + next_char
                if i == len(self._text) - 1:
                    encoded_text.append(self._code_table[output_word])
            else:
                encoded_text.append(self._code_table[output_word])
                self._add_codeword(output_word + next_char)
                output_word = next_char
            i += 1

        return encoded_text

    def _calculate_compression_ratio(self):
        """
        Calculates the memory saved from the compression. The encoded text is represented by 12 bit codes instead of
        8 bit codes.
        """
        compressed_bytes = math.ceil(len(self.encoded_text) * 12 / 8)
        uncompressed_bytes = len(self._text)

        return uncompressed_bytes / compressed_bytes

    def _initialise_code_table(self):
        """
        Initializes a code dictionary with 256 entries. Maps unicode character strings to their code [0 to 255].
        Resets the next string_table code to 256.
        """
        self._code_table = {chr(i): i for i in range(256)}
        self._next_code = 256

    def _add_codeword(self, word):
        """
        Adds a string to the code table. If the code table is full, (max capacity 4096 entries), the code
        table is re-initialised with 256 entries.
        """
        if self._next_code == self._max_code:
            self._initialise_code_table()

        self._code_table[word] = self._next_code
        self._next_code += 1

    def _encode_to_bytes(self):
        """
        Converts the 12 bit codes to an stream of byte objects. The last code, where there is an odd number, is padded
        with 4 0 bits (e.g. 0000) to create the final byte.
        """

        twelve_bit_codes = self.encoded_text.copy()
        encoded_bytes = b''

        while True:
            if not twelve_bit_codes:
                break
            if len(twelve_bit_codes) > 1:
                first_code = twelve_bit_codes.pop(0)
                second_code = twelve_bit_codes.pop(0)
                bytes = self._convert_to_bytes(first_code, second_code)
            else:
                code = twelve_bit_codes.pop(0)
                bytes = self._padded_convert_to_bytes(code)

            encoded_bytes += bytes

        return encoded_bytes

    def _get_next_char(self, index):
        """
        Returns the next character in the text, given an index. If no next character exists, returns an empty string.
        """
        try:
            return self._text[index + 1]
        except IndexError:
            return ''

    @staticmethod
    def _read_file(filepath):
        """
        Returns the text from a text file.
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def _convert_to_bytes(first_code, second_code):
        """
        :param first_code: An integer that represents a 12-bit code
        :param second_code: The subsequent 12 bit code
        :return: A byte object containing 3 bytes created from the 2 12-bit codes.
        """
        bit_string = format(first_code, '012b') + format(second_code, '012b')
        return int(bit_string, 2).to_bytes(3, byteorder='big')

    @staticmethod
    def _padded_convert_to_bytes(code):
        """
        :param code: An integer that represents a 12-bit code
        :return: A byte object containing 2 bytes created from the 12-bit codes. The final byte is padded with 0000.
        """
        padded_bits = '0000'
        bit_string = format(code, '012b') + padded_bits
        return int(bit_string, 2).to_bytes(2, byteorder='big')


class Decompressor:
    """
    Decodes a LZW compressed file.
    Maximum code table size is set to the 4096 entries (12 bit codes).
    """
    def __init__(self, compressed_filepath):
        self._string_table = None
        self._next_code = None
        self._max_code = 4096
        self.decoded_text = self._decompress_file(compressed_filepath)

    def save_text(self, save_filepath):
        """
        Saves the decompressed text as a .txt file.
        """
        assert save_filepath.lower().endswith('.txt'), 'Saved file must have the file extension *.txt'

        with open(save_filepath, 'w+', encoding='utf-8') as file:
            file.write(self.decoded_text)

    def _decompress_file(self, compressed_filepath):
        """
        Initialises the string table, and converts the bytes from the file into 12-bit codes and decoded using the
        LZW algorithm. Returns a the decoded text as a string.
        """
        self._initialise_string_table()
        with open(compressed_filepath, 'r+b') as compressed_file:
            twelve_bit_codes = self._twelve_bit_read(compressed_file)

        return self._lzw_decompress(twelve_bit_codes)

    def _initialise_string_table(self):
        """
        Initializes a string dictionary with 256 entries. Maps unicode [0 to 255] to single character strings.
        Resets the next string_table code with 256.
        """
        self._next_code = 256
        self._string_table = {i: chr(i) for i in range(256)}

    def _twelve_bit_read(self, compressed_file):
        """
        Generates a list of 12-bit integers from a binary file
        """
        encoded_12_bits = []

        while True:
            bytes = compressed_file.read(3)

            if not bytes:
                break
            if len(bytes) == 2:
                twelve_bit_code = self._process_padded_bytes(bytes)
                encoded_12_bits.append(twelve_bit_code)
            else:
                twelve_bit_codes = self._process_bytes(bytes)
                encoded_12_bits.extend(twelve_bit_codes)

        return encoded_12_bits

    def _lzw_decompress(self, twelve_bit_codes):
        """
        Decompresses the twelve bit code stream using the LZW algorithm.
        """
        decoded_strings = []
        old_string = self._string_table[twelve_bit_codes[0]]
        decoded_strings.append(old_string)

        for code in twelve_bit_codes[1:]:

            if code not in self._string_table:
                current_string = old_string + char
            else:
                current_string = self._string_table[code]

            decoded_strings.append(current_string)
            char = current_string[0]
            self._add_to_string_table(old_string + char)
            old_string = current_string

        return ''.join(decoded_strings)

    def _add_to_string_table(self, string):
        """
        Adds a string to the string code table. If the string table is full, (max capacity 4096 entries), the string
        table is re-initialised to 256 entries.
        """
        if self._next_code == self._max_code:
            self._initialise_string_table()

        self._string_table[self._next_code] = string
        self._next_code += 1

    @staticmethod
    def _process_bytes(bytes):
        """
        :param bytes: a 24-bit byte object (3 bytes)
        :return: A list containing 2 12-bit integers. The first code using the leading 12-bits of the byte object,
        the second code using the trailing 12-bits.
        """
        byte_int = int.from_bytes(bytes, byteorder='big')
        max_12_bit_byte = 0xfff

        first_code = byte_int >> 12
        second_code = byte_int & max_12_bit_byte

        return [first_code, second_code]

    @staticmethod
    def _process_padded_bytes(bytes):
        """
        :param bytes: a 16-bit byte object (2 bytes). Used to encode a 12-bit code, where the trailing 4 zeros are
        padding bits.
        :return: A 12-bit integer. The code uses the leading 12-bits of the byte object. The 4-bits used for padding
        are disregarded.
        """
        byte_int = int.from_bytes(bytes, byteorder='big')

        return byte_int >> 4
