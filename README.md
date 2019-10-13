# lzw-compressor
## Introduction
A module built to compress and decompress text files. This is a loseless compressor which utilises the Lempel-Ziv-Welch (LZW) algorithm. 
The encoding was implemented using fixed 12-bit codes. For an odd number of bytes, the last code is padded with 0000 to create the final 12-bit code.

## Using the Compressor class

Initialised the Compressor class with the filepath to the text file. This module currently only supports the first 256 unicode characters `Decimal: 0 - 255`.
```
compressor_object = Compressor(<filepath to .txt file>)
```
Use `compressor_object.encoded_text` to return the 12-bit encoded text as a list of integers.
Use `compressor_object.compression_ratio` to return the 



## Testing

Some dummy files have been included in the `src/test_files` directory to test the compression and decompression classes:
```
dummy_text.txt
dummy_compressed_file.z
```
