import os
import shutil
import hashlib
import configparser
from datetime import datetime
from PIL import Image, ExifTags
from tqdm import tqdm

# ---------- LOAD CONFIG ----------
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

SOURCE_DIR = config["PATHS"]["source_dir"]
DEST_DIR   = config["PATHS"]["dest_dir"]

MODE = config["MODE"]["operation"].lower()
DRY_RUN = config["MODE"].getboolean("dry_run")

ENABLE_DUP = config["FEATURES"].getboolean("enable_duplicate_check")
DUP_LOG = config["FEATURES"].get("duplicates_log", "duplicates.log")

SHOW_BAR = config["UI"].getboolean("show_progress_bar")

IMAGE_EXTS = set(e.strip() for e in config["FILES"]["image_extensions"].split(","))
VIDEO_EXTS = set(e.strip() for e in config["FILES"]["video_extensions"].split(","))

# ---------- STATE ----------
hash_index = {}

photos_count = 0
videos_count = 0
duplicates_skipped = 0
files_copied = 0

# ---------- HELPERS ----------
def sha256(path, chunk=1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while (data := f.read(chunk)):
            h.update(data)
    return h.hexdigest()

def get_photo_date(path):
    try:
        img = Image.open(path)
        exif = img._getexif()
        if not exif:
            return None
        for k, v in exif.items():
            if ExifTags.TAGS.get(k) == "DateTimeOriginal":
                return datetime.strptime(v, "%Y:%m:%d %H:%M:%S")
    except:
        pass
    return None

def get_file_date(path):
    return datetime.fromtimestamp(os.path.getmtime(path))

def ensure_dir(path):
    if not DRY_RUN:
        os.makedirs(path, exist_ok=True)

def log_duplicate(src, original):
    global duplicates_skipped
    duplicates_skipped += 1
    with open(DUP_LOG, "a", encoding="utf-8") as f:
        f.write(
            f"DUPLICATE: {os.path.basename(src)}\n"
            f"ORIGINAL : {original}\n"
            f"SKIPPED  : {src}\n\n"
        )

def is_duplicate(src, dst):
    file_hash = sha256(src)
    if file_hash in hash_index:
        log_duplicate(src, hash_index[file_hash])
        return True
    hash_index[file_hash] = dst
    return False

def transfer(src, dst):
    global files_copied
    if DRY_RUN:
        return
    if os.path.exists(dst):
        return
    if MODE == "copy":
        shutil.copy2(src, dst)
    else:
        shutil.move(src, dst)
    files_copied += 1

# ---------- START ----------
if ENABLE_DUP:
    open(DUP_LOG, "w").close()

iterator = os.listdir(SOURCE_DIR)
if SHOW_BAR:
    iterator = tqdm(iterator, desc="Organizing media")

for filename in iterator:
    src = os.path.join(SOURCE_DIR, filename)
    if not os.path.isfile(src):
        continue

    base, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext in IMAGE_EXTS:
        date = get_photo_date(src) or get_file_date(src)
        category = "Photos"
        photos_count += 1
    elif ext in VIDEO_EXTS:
        date = get_file_date(src)
        category = "Videos"
        videos_count += 1
    else:
        continue

    year = str(date.year)
    month = f"{date.month:02d}"
    target_dir = os.path.join(DEST_DIR, year, month, category)
    ensure_dir(target_dir)

    dst = os.path.join(target_dir, filename)

    if not ENABLE_DUP:
        transfer(src, dst)
    else:
        if not is_duplicate(src, dst):
            transfer(src, dst)

# ---------- SUMMARY ----------
print("\n──────── SUMMARY ────────")
print(f"Photos              : {photos_count}")
print(f"Videos              : {videos_count}")
print(f"Duplicates skipped  : {duplicates_skipped}")
print(f"Files copied/moved  : {files_copied}")
print(f"Mode                : {MODE.upper()}")
print(f"Dry run             : {DRY_RUN}")
print("────────────────────────")
print("Done.")
