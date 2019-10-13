# lzw-compressor
## Introduction
A module built to compress and decompress text files. This is a loseless compressor which utilises the Lempel-Ziv-Welch (LZW) algorithm. 
The encoding was implemented using fixed 12-bit codes. For an odd number of bytes, the last code is padded with 0000 to create the final 12-bit code.

Some dummy files have been included in the `src/test_files` directory to test the compression and decompression classes:
> dummy_text.txt
> dummy_compressed_file.z
