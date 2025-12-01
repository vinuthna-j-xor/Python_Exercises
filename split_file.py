import os
from threading import Thread


CHUNK_SIZE = 1 * 1024 * 1024  # 1 MB
INPUT_FILE = "10mb-examplefile-com.txt"
CHUNK_FOLDER = "chunks"
MERGED_FILE = "merged.txt"


def split_file():
    os.makedirs(CHUNK_FOLDER, exist_ok=True)
    with open(INPUT_FILE, "rb") as f:
        chunk_num = 0
        while True:
            chunk_data = f.read(CHUNK_SIZE)
            if not chunk_data:
                break
            chunk_path = os.path.join(CHUNK_FOLDER, f"chunk_{chunk_num}.txt")
            with open(chunk_path, "wb") as chunk_file:
                chunk_file.write(chunk_data)
            chunk_num += 1
    print(f"Split into {chunk_num} chunks.")


def write_chunk(chunk_path, file_handle):
    with open(chunk_path, "rb") as f:
        file_handle.write(f.read())


def merge_chunks():
    chunk_files = sorted(os.listdir(CHUNK_FOLDER), key=lambda x: int(x.split("_")[1].split(".")[0]))
    with open(MERGED_FILE, "wb") as merged:
        for chunk in chunk_files:
            with open(os.path.join(CHUNK_FOLDER, chunk), "rb") as f:
                merged.write(f.read())
    print("Chunks merged into", MERGED_FILE)



def verify_files():
    with open(INPUT_FILE, "rb") as original, open(MERGED_FILE, "rb") as merged:
        if original.read() == merged.read():
            print("Verification successful: files are identical!")
        else:
            print("Verification failed: files are different.")
split_file()
merge_chunks()
verify_files()
