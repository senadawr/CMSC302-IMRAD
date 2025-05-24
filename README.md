# CMSC302-IMRAD
Algorithm Analysis of Huffman Trees and Codes

# Huffman Coding Compression & Decompression

This project implements file compression and decompression using Huffman coding in Python. It includes benchmarking tools to measure the efficiency of the compression algorithm.

## Features
- Compress text files using Huffman coding
- Decompress files back to their original text
- Benchmark compression and decompression speed and ratio

## Files
- `huffmantrees.py`: Main script for compressing and decompressing files using Huffman coding.
- `benchmark_huffman.py`: Script to benchmark the performance of the Huffman coding implementation.
- `benchmark_results.txt`: Output file containing benchmark results.
- Example input files: `small.txt`, `medium.txt`, `large.txt`, `superlarge.txt`

## Usage

### Compression
```
python huffmantrees.py compress <input_file.txt> <output_file.huff>
```

### Decompression
```
python huffmantrees.py decompress <input_file.huff> <output_file.txt>
```

### Benchmarking
To run benchmarks on the provided example files:
```
python benchmark_huffman.py
```
Results will be saved in `benchmark_results.txt`.

## Requirements
- Python 3.x

## How It Works
- The compressor reads the input file, builds a Huffman tree, and encodes the text.
- The codebook and compressed data are saved using Python's `pickle` module.
- The decompressor reads the codebook and compressed data, reconstructs the original text, and writes it to the output file.

## License
This project is provided for educational purposes. 
