# lzw-compressor
## Introduction
A module built to compress and decompress text files. This is a loseless compressor which utilises the Lempel-Ziv-Welch (LZW) algorithm. 
The encoding was implemented using fixed 12-bit codes. For an odd number of bytes, the last code is padded with 0000 to create the final 12-bit code.

## Using the Compressor class

Initialise the Compressor class with the filepath to the text file. This module currently only supports the first 256 unicode characters `Decimal: 0 - 255`.
```
compressor_object = Compressor(<filepath to .txt file>)
```
To return the 12-bit encoded text as a list of intergers use:
```
compressor_object.encoded_text
```
The compression ratio is a measure of the reduction in data needed to represent the text after the LZW compression. It is calculated as the `uncompressed number of bytes / compressed number of bytes`. 
```
compressor_object.compression_ratio
```
The compressed text can be encoded as bytes and saved to a binary `.z` file using the `save_file` method.
```
compressor_object.save_file(<save filepath for the .z file>)
```

## Using the Decompressor class

The Decompressor class can be used to decompress LZW compressed binary files. Initialise the Decompressor class with the filepath to the binary file.
```
decompressor_object = Decompressor(<filepath to .z file>)
```
To return the decoded text as a string use:
```
decompressor_object.decoded_string
```
To save the decoded text in a `.txt` file use:
```
decompressor_object.save_text(<save filepath for the .txt file>)
```

## Testing

Some dummy files have been included in the `src/test_files` directory to test the compression and decompression classes.
```
dummy_text.txt
dummy_compressed_file.z
```
