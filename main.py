#!/usr/bin/env python3
"""
add_album_art.py

Embeds a cover image as album art into all audio files in the current
directory (FLAC, MP3, M4A/MP4, AAC).

Usage:
    python add_album_art.py
    python add_album_art.py --image cover.jpg
    python add_album_art.py --image cover.png --dir /path/to/music

Requires:
    pip install mutagen
"""

import argparse
import os
import sys

try:
    from mutagen.flac import FLAC, Picture
    from mutagen.id3 import ID3, ID3NoHeaderError, APIC
    from mutagen.mp3 import MP3
    from mutagen.mp4 import MP4, MP4Cover
except ImportError:
    sys.exit("Missing dependency. Install it with:\n    pip install mutagen")

IMAGE_EXTS = (".jpg", ".jpeg", ".png")
AUDIO_EXTS = (".flac", ".mp3", ".m4a", ".mp4", ".aac")


def find_cover_image(directory):
    """Return the path of the first image file found in the directory."""
    candidates = []
    for name in os.listdir(directory):
        if name.lower().endswith(IMAGE_EXTS):
            candidates.append(name)
    if not candidates:
        return None
    # Prefer files literally named "cover" or "folder"
    for preferred in ("cover", "folder", "album", "art"):
        for name in candidates:
            if os.path.splitext(name)[0].lower() == preferred:
                return os.path.join(directory, name)
    return os.path.join(directory, sorted(candidates)[0])


def guess_mime(image_path):
    ext = os.path.splitext(image_path)[1].lower()
    if ext == ".png":
        return "image/png"
    return "image/jpeg"


def embed_flac(path, image_data, mime):
    audio = FLAC(path)
    audio.clear_pictures()
    pic = Picture()
    pic.data = image_data
    pic.type = 3  # front cover
    pic.mime = mime
    pic.desc = "Cover"
    audio.add_picture(pic)
    audio.save()


def embed_mp3(path, image_data, mime):
    try:
        audio = ID3(path)
    except ID3NoHeaderError:
        audio = ID3()
    # Remove existing cover art
    audio.delall("APIC")
    audio.add(
        APIC(
            encoding=1,       # UTF-16 (v2.3-safe; v2.4-only UTF-8 breaks Explorer)
            mime=mime,
            type=3,           # front cover
            desc="Cover",
            data=image_data,
        )
    )
    # Save as ID3v2.3 — Windows Explorer's thumbnail/property handler doesn't
    # reliably read ID3v2.4 (mutagen's default), so v2.3 keeps Explorer happy
    # while still working fine in VLC, foobar2000, etc.
    audio.save(path, v2_version=3)


def embed_mp4(path, image_data, mime):
    audio = MP4(path)
    fmt = MP4Cover.FORMAT_PNG if mime == "image/png" else MP4Cover.FORMAT_JPEG
    audio["covr"] = [MP4Cover(image_data, imageformat=fmt)]
    audio.save()


def embed_aac(path, image_data, mime):
    # Raw .aac (ADTS) streams generally do not support embedded tags/art.
    # Try treating it as MP4 container first; otherwise skip.
    try:
        embed_mp4(path, image_data, mime)
    except Exception:
        raise RuntimeError(
            "Raw .aac files (ADTS streams) don't support embedded album art. "
            "Convert to .m4a first if you need cover art."
        )


def process_file(path, image_data, mime):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".flac":
        embed_flac(path, image_data, mime)
    elif ext == ".mp3":
        embed_mp3(path, image_data, mime)
    elif ext in (".m4a", ".mp4"):
        embed_mp4(path, image_data, mime)
    elif ext == ".aac":
        embed_aac(path, image_data, mime)
    else:
        raise ValueError(f"Unsupported extension: {ext}")


def main():
    parser = argparse.ArgumentParser(description="Embed album art into audio files.")
    parser.add_argument(
        "--image", "-i",
        help="Path to the cover image (jpg/png). If omitted, the script "
             "auto-detects an image in the target directory.",
    )
    parser.add_argument(
        "--dir", "-d",
        default=".",
        help="Directory containing the audio files (default: current directory).",
    )
    args = parser.parse_args()

    directory = os.path.abspath(args.dir)

    image_path = args.image or find_cover_image(directory)
    if not image_path or not os.path.isfile(image_path):
        sys.exit(
            "No cover image found. Place a .jpg/.png file in the directory "
            "or pass one explicitly with --image."
        )

    with open(image_path, "rb") as f:
        image_data = f.read()
    mime = guess_mime(image_path)

    print(f"Using cover image: {image_path} ({mime})")

    audio_files = [
        f for f in os.listdir(directory)
        if f.lower().endswith(AUDIO_EXTS)
    ]

    if not audio_files:
        sys.exit("No audio files found in the directory.")

    ok, failed = 0, 0
    for name in sorted(audio_files):
        path = os.path.join(directory, name)
        try:
            process_file(path, image_data, mime)
            print(f"  [OK]   {name}")
            ok += 1
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            failed += 1

    print(f"\nDone. {ok} file(s) updated, {failed} failed.")


if __name__ == "__main__":
    main()
