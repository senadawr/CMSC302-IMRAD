# download_shakespeare.py

import urllib.request

def download_shakespeare_works():
    url = "https://www.gutenberg.org/cache/epub/100/pg100.txt"
    output_file = "shakespeare_complete.txt"

    try:
        print("Downloading Shakespeare's complete works...")
        urllib.request.urlretrieve(url, output_file)
        print(f"Download complete! Saved as '{output_file}'")
    except Exception as e:
        print("Download failed:", e)

if __name__ == "__main__":
    download_shakespeare_works()