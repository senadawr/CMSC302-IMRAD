import heapq
import os
import pickle
from collections import defaultdict, Counter
import time

class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(text):
    return Counter(text)

def build_huffman_tree(freq_table):
    heap = [HuffmanNode(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    return heap[0] if heap else None

def build_codes(node, prefix='', codebook=None):
    if codebook is None:
        codebook = {}
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        build_codes(node.left, prefix + '0', codebook)
        build_codes(node.right, prefix + '1', codebook)
    return codebook

def encode_text(text, codebook):
    return ''.join(codebook[char] for char in text)

def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    for i in range(extra_padding):
        encoded_text += "0"
    padded_info = "{0:08b}".format(extra_padding)
    return padded_info + encoded_text

def get_byte_array(padded_encoded_text):
    if len(padded_encoded_text) % 8 != 0:
        raise ValueError("Encoded text not padded properly")
    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        b.append(int(byte, 2))
    return b

def compress(input_path, output_path):
    start_time = time.time()
    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()
    freq_table = build_frequency_table(text)
    huffman_tree = build_huffman_tree(freq_table)
    codebook = build_codes(huffman_tree)
    encoded_text = encode_text(text, codebook)
    padded_encoded_text = pad_encoded_text(encoded_text)
    byte_array = get_byte_array(padded_encoded_text)
    with open(output_path, 'wb') as output:
        pickle.dump((codebook, byte_array), output)
    end_time = time.time()
    original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_path)
    compression_ratio = original_size / compressed_size if compressed_size != 0 else float('inf')
    print(f"File compressed and saved to {output_path}")
    print(f"Original size: {original_size} bytes")
    print(f"Compressed size: {compressed_size} bytes")
    print(f"Compression ratio: {compression_ratio:.2f}")
    print(f"Time taken to compress: {end_time - start_time:.4f} seconds")

def decompress(input_path, output_path):
    start_time = time.time()
    with open(input_path, 'rb') as file:
        codebook, byte_array = pickle.load(file)
    inverse_codebook = {v: k for k, v in codebook.items()}
    bit_string = ''
    for byte in byte_array:
        bit_string += f"{byte:08b}"
    padded_info = bit_string[:8]
    extra_padding = int(padded_info, 2)
    bit_string = bit_string[8:]
    encoded_text = bit_string[:-extra_padding] if extra_padding > 0 else bit_string
    current_code = ''
    decoded_text = ''
    for bit in encoded_text:
        current_code += bit
        if current_code in inverse_codebook:
            decoded_text += inverse_codebook[current_code]
            current_code = ''
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(decoded_text)
    end_time = time.time()
    compressed_size = os.path.getsize(input_path)
    decompressed_size = os.path.getsize(output_path)
    print(f"File decompressed and saved to {output_path}")
    print(f"Compressed size: {compressed_size} bytes")
    print(f"Decompressed size: {decompressed_size} bytes")
    print(f"Time taken to decompress: {end_time - start_time:.4f} seconds")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Compress or decompress a file using Huffman coding.')
    subparsers = parser.add_subparsers(dest='command', required=True)

    compress_parser = subparsers.add_parser('compress', help='Compress a text file')
    compress_parser.add_argument('input', help='Input text file to compress')
    compress_parser.add_argument('output', help='Output compressed file')

    decompress_parser = subparsers.add_parser('decompress', help='Decompress a .huff file')
    decompress_parser.add_argument('input', help='Input .huff file to decompress')
    decompress_parser.add_argument('output', help='Output text file')

    args = parser.parse_args()
    if args.command == 'compress':
        compress(args.input, args.output)
    elif args.command == 'decompress':
        decompress(args.input, args.output)

if __name__ == '__main__':
    main()
