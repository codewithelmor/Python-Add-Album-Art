# Audio Album Art Embedder

This Python script embeds a cover image (`.jpg`, `.jpeg`, or `.png`) directly into the metadata of audio files in a specified directory. It supports multiple popular audio formats and strips out existing artwork before applying the new cover.

## Features

* **Wide Format Support:** Works with `.mp3`, `.flac`, `.m4a`, and `.mp4` files.
* **Windows-Friendly MP3 Tagging:** Saves MP3 files using ID3v2.3 tags, ensuring that thumbnails and properties show up properly in Windows Explorer.
* **Smart Auto-Detection:** Automatically scans and picks the best image file (preferring names like `cover` or `folder`) if you don't explicitly pass one.

---

## Prerequisites & Setup

This script requires Python 3 and the `mutagen` audio tagging library. Follow these steps to set up an isolated Python virtual environment and install the required dependencies.

### 1. Clone or Copy the Files
Ensure `add_album_art.py`, `requirements.txt`, and your music files are ready in your working environment.

### 2. Create a Virtual Environment

Open your terminal or command prompt, navigate to the folder containing the script, and run the appropriate command for your operating system:

* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  ```
* **Windows:**
  ```cmd
  python -m venv venv
  ```

### 3. Activate the Virtual Environment

* **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```
* **Windows (Command Prompt):**
  ```cmd
  venv\Scripts\activate
  ```
* **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

### 4. Install Dependencies

With the virtual environment activated, install the required packages using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## Usage

You can run the script directly from your terminal. Make sure your virtual environment remains active while running these commands.

### Basic Execution (Auto-Detect)
If you place the script directly inside your album folder alongside a `cover.jpg` file, simply run:
```bash
python add_album_art.py
```
*The script will automatically detect the music files and pick the best image candidate.*

### Specify a Custom Image
To point the script to a specific image file:
```bash
python add_album_art.py --image path/to/art.png
```

### Target a Different Directory
To process music files located in a completely different folder:
```bash
python add_album_art.py --dir /path/to/music/album
```

### Combine Both Arguments
```bash
python add_album_art.py --image blueprints.jpg --dir /home/user/music/rock
```

---

## Technical Notes

* **Raw AAC Files:** Raw `.aac` files (ADTS streams) do not natively support embedded metadata art. If the script encounters a raw `.aac` file, it will advise you to convert it to an `.m4a` container first.
* **Deactivating the Environment:** When you are completely finished working, you can safely exit the virtual environment by typing:
  ```bash
  deactivate
  ```
