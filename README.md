# iPhone Photo & Video Organizer

Automatically organize your iPhone photos and videos into folders by year, month, and media type with duplicate detection.

---

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

## Features

✨ **Smart Organization**
- Organize photos/videos into `YYYY/MM/Category/` folder structure
- Automatic extraction of EXIF data for accurate date information
- Fallback to file modification date if EXIF data unavailable

🔐 **Duplicate Detection**
- SHA256 hash-based duplicate detection
- Detailed duplicate logging
- Optional duplicate checking (can be disabled for faster processing)

⚙️ **Flexible Operations**
- **Copy mode**: Keep original files in source directory
- **Move mode**: Transfer files to destination and remove originals
- **Dry-run mode**: Preview changes without modifying files

📊 **User-Friendly**
- Progress bar display with TQDM
- Summary statistics after execution
- Detailed duplicate logging for review

---

## Requirements

- **Python 3.7+**
- **Pillow** (for EXIF data extraction)
- **tqdm** (for progress bar)

---

## Installation

### 1. Clone or download the project

```bash
cd organize-iphone-photos
```

### 2. Install dependencies

```bash
pip install pillow tqdm
```

### 3. Configure the script

Edit `config.ini` with your source and destination paths.

---

## Configuration

Edit `config.ini` to customize behavior:

```ini
[PATHS]
# Source directory containing iPhone photos/videos
source_dir = E:\iPhone

# Destination directory where organized media will be placed
dest_dir   = E:\iPhone_Organized

[MODE]
# Choose operation: 'copy' or 'move'
# - copy: Keep originals in source directory
# - move: Transfer files and remove from source
operation = copy

# Test mode: preview changes without modifying files
# - true: Show what would happen (no actual changes)
# - false: Actually perform the operation
dry_run   = false

[FEATURES]
# Enable duplicate detection using SHA256 hashing
# - true: Check for duplicates and log them
# - false: Skip duplicate checking (faster)
enable_duplicate_check = false

# Log file for duplicate entries (only used if duplicates detected)
duplicates_log = duplicates.log

[UI]
# Display progress bar during execution
# - true: Show TQDM progress bar
# - false: No progress indication
show_progress_bar = true

[FILES]
# File extensions to recognize as images (comma-separated, lowercase)
image_extensions = .jpg,.jpeg,.heic,.png,.webp

# File extensions to recognize as videos (comma-separated, lowercase)
video_extensions = .mov,.mp4
```

### Configuration Sections Explained

| Section | Key | Purpose |
|---------|-----|---------|
| PATHS | source_dir | Where your original iPhone media is stored |
| PATHS | dest_dir | Where organized media will be placed |
| MODE | operation | copy (safe) or move (removes originals) |
| MODE | dry_run | Preview without changes (true/false) |
| FEATURES | enable_duplicate_check | Detect duplicates (slower but safer) |
| FEATURES | duplicates_log | File to log duplicate entries |
| UI | show_progress_bar | Display progress during execution |
| FILES | image_extensions | Image file types to process |
| FILES | video_extensions | Video file types to process |

---

## Usage

### Basic Usage

```bash
python main.py
```

### Workflow Examples

#### 1. Preview Changes (Safe First Run)
```ini
# config.ini
dry_run = false
show_progress_bar = true
enable_duplicate_check = true
operation = copy
```

Run the script and review the output and generated `duplicates.log` if duplicates were found.

#### 2. Organize Without Duplicates (Fast)
```ini
dry_run = false
enable_duplicate_check = false
operation = copy
```

#### 3. Move Files (Removes Originals)
```ini
dry_run = false
enable_duplicate_check = true
operation = move
```

⚠️ **Warning**: Move mode deletes original files. Always enable `enable_duplicate_check` before using move mode.

---

## How It Works

### 1. File Discovery
- Scans `source_dir` for files matching configured extensions
- Skips directories (only processes files)

### 2. Date Extraction
- **For Photos**: Extracts EXIF `DateTimeOriginal` tag if available
- **For Videos**: Uses file modification date
- **Fallback**: Uses file modification date if EXIF unavailable

### 3. Organization
- Creates folder structure: `dest_dir/YEAR/MONTH/Category/`
  - Year: 4-digit year (e.g., `2024`)
  - Month: 2-digit month (e.g., `03`, `12`)
  - Category: `Photos` or `Videos`

### 4. Duplicate Detection (Optional)
- Calculates SHA256 hash of each file
- Compares against previously indexed files
- Logs duplicates to `duplicates.log`
- Skips duplicate files during transfer

### 5. File Transfer
- **Copy**: Duplicates files to destination
- **Move**: Transfers files and removes originals
- Respects dry-run mode (no actual changes when enabled)

---

## Examples

### Example 1: Organize Backup Without Duplicates
```bash
# config.ini settings
source_dir = D:\iPhone_Backup
dest_dir = E:\iPhone_Organized
operation = copy
dry_run = false
enable_duplicate_check = false
show_progress_bar = true
```

```bash
python organize_media.py
```

**Output:**
```
Organizing media: 100%|████████| 1500/1500 [00:45<00:00, 33.33it/s]

──────── SUMMARY ────────
Photos              : 1200
Videos              : 150
Duplicates skipped  : 0
Files copied/moved  : 1350
Mode                : COPY
Dry run             : False
────────────────────────
✅ Done.
```

### Example 2: Find Duplicates Before Cleanup
```bash
# config.ini settings
enable_duplicate_check = true
dry_run = true
operation = move
```

```bash
python organize_media.py
```

Review `duplicates.log` to see which files are duplicates, then:
1. Delete duplicates manually if needed
2. Run again with `dry_run = false`

### Example 3: Move Files (Remove Originals)
```bash
# config.ini settings
source_dir = /Volumes/iPhone
dest_dir = /Users/username/Pictures/iPhone_Organized
operation = move
enable_duplicate_check = true
dry_run = false
```

```bash
python organize_media.py
```

Files will be moved from source to organized destination structure.

---

## Output Structure

Files are organized as follows:

```
dest_dir/
├── 2024/
│   ├── 01/
│   │   ├── Photos/
│   │   │   ├── IMG_0001.jpg
│   │   │   ├── IMG_0002.heic
│   │   │   └── ...
│   │   └── Videos/
│   │       ├── VID_0001.mov
│   │       └── ...
│   ├── 02/
│   │   ├── Photos/
│   │   └── Videos/
│   └── ...
├── 2023/
│   ├── 01/
│   └── ...
└── ...
```

---

## Duplicate Log Format

When duplicates are detected, they're logged to `duplicates.log`:

```
DUPLICATE: IMG_5678.jpg
ORIGINAL : /path/to/organized/2024/03/Photos/IMG_5678.jpg
SKIPPED  : /source/path/IMG_5678.jpg

DUPLICATE: VID_1234.mov
ORIGINAL : /path/to/organized/2024/02/Videos/VID_1234.mov
SKIPPED  : /source/path/VID_1234.mov
```

---

## Troubleshooting

### Issue: "No module named 'PIL'"
**Solution**: Install Pillow
```bash
pip install pillow
```

### Issue: "No module named 'tqdm'"
**Solution**: Install tqdm
```bash
pip install tqdm
```

### Issue: EXIF data not being read
- Some photos may not have EXIF data
- Script automatically falls back to file modification date
- Check file modification dates in file explorer

### Issue: No files are being processed
- Verify `source_dir` exists and contains files
- Check that file extensions match `image_extensions` and `video_extensions` config
- Ensure files are not hidden or read-only
- Run with `dry_run = true` first to see what the script detects

### Issue: "Permission denied" errors
- Ensure script has read/write permissions to both directories
- Close any programs accessing the files
- Run terminal as Administrator (Windows) or with `sudo` (macOS/Linux)

### Issue: Slow performance with duplicate checking
- Disable `enable_duplicate_check` if you're confident there are no duplicates
- Hash calculation is I/O intensive on large files
- Consider running on local drive instead of network drive

### Issue: Duplicate detection not working
- File sizes must be identical for true duplicates
- Same content = same SHA256 hash
- Verify you actually have duplicate files before reporting an issue

---

## Tips & Best Practices

💡 **Before First Run**
1. Backup your iPhone photos
2. Test with a small `source_dir` first
3. Use `dry_run = true` to preview changes
4. Start with `operation = copy` (safer than move)

💡 **For Large Libraries**
1. Disable `enable_duplicate_check` initially (faster)
2. Use `show_progress_bar = true` for visibility
3. Consider running overnight
4. Monitor free disk space on destination drive

💡 **Regular Maintenance**
1. Keep original source backup
2. Run periodically on new iPhone backups
3. Review `duplicates.log` periodically
4. Verify destination folder structure matches expectations

---

## Performance Metrics

Estimated processing speeds (single-threaded):

| Operation | Speed | Notes |
|-----------|-------|-------|
| Scan files | ~500 files/sec | Depends on filesystem |
| Read EXIF | ~100 files/sec | Variable by photo format |
| Copy files | ~50 MB/sec | Depends on disk speed |
| Move files | ~50 MB/sec | Plus deletion time |
| Hash (SHA256) | ~200 MB/sec | For duplicate detection |

---

## License

Specify your project license here.

---

## Version History

- **v1.0** (2026-04) - Initial release
  - Basic file organization
  - EXIF date extraction
  - Duplicate detection
  - Copy/move operations
  - Dry-run mode

---

**Last Updated:** April 2026
