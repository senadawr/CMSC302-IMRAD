import os
import subprocess
import time
import glob
import statistics


RUNS = 50
OUTLIER_PERCENT = 0.1
RESULTS_FILE = 'benchmark_results.txt'
COMPRESS_EXT = '.huff'

def remove_outliers(data, percent):
    n = int(len(data) * percent)
    if n == 0:
        return data
    data_sorted = sorted(data)
    return data_sorted[n:-n]

def benchmark_file(txt_file):
    compress_times = []
    decompress_times = []
    compressed_file = txt_file + COMPRESS_EXT
    decompressed_file = 'restored_' + os.path.basename(txt_file)
    original_size = os.path.getsize(txt_file)
    compressed_size = None
    runs = 5 if os.path.basename(txt_file) == 'superlarge.txt' else RUNS
    print(f"Benchmarking {txt_file} for {runs} runs...")
    for i in range(runs):
        start = time.perf_counter()
        subprocess.run(['python', 'huffmantrees.py', 'compress', txt_file, compressed_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        compress_times.append((time.perf_counter() - start) * 1000)
        if compressed_size is None:
            compressed_size = os.path.getsize(compressed_file)
        start = time.perf_counter()
        subprocess.run(['python', 'huffmantrees.py', 'decompress', compressed_file, decompressed_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        decompress_times.append((time.perf_counter() - start) * 1000)
    compress_times = remove_outliers(compress_times, OUTLIER_PERCENT)
    decompress_times = remove_outliers(decompress_times, OUTLIER_PERCENT)
    avg_compress = statistics.mean(compress_times)
    avg_decompress = statistics.mean(decompress_times)
    compression_ratio = original_size / compressed_size if compressed_size else 0
    if os.path.exists(compressed_file):
        os.remove(compressed_file)
    if os.path.exists(decompressed_file):
        os.remove(decompressed_file)
    with open(RESULTS_FILE, 'a') as f:
        f.write(f"File: {txt_file}\n")
        f.write(f"Original size: {original_size} bytes\n")
        f.write(f"Compressed size: {compressed_size} bytes\n")
        f.write(f"Compression ratio: {compression_ratio:.2f}\n")
        f.write(f"Average encoding time: {avg_compress:.2f} ms\n")
        f.write(f"Average decoding time: {avg_decompress:.2f} ms\n")
        f.write("-"*40 + "\n")

if __name__ == '__main__':
    with open(RESULTS_FILE, 'w') as f:
        f.write('Huffman Compression Benchmark Results\n')
        f.write('='*40 + '\n')
    txt_files = ['small.txt', 'medium.txt', 'large.txt', 'superlarge.txt']
    for txt_file in txt_files:
        if os.path.exists(txt_file):
            benchmark_file(txt_file)
        else:
            with open(RESULTS_FILE, 'a') as f:
                f.write(f"File: {txt_file} not found. Skipping.\n")
                f.write("-"*40 + "\n")
    print(f"Benchmark complete. Results saved to {RESULTS_FILE}")
    print("\nAll benchmarks finished! You can now check 'benchmark_results.txt' for details.") 
