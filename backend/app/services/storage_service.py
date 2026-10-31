"""
CLAIMSIGHT AI - Storage Service & Forensic Metadata Extraction
Handles file persistence, SHA-256 fingerprinting, EXIF extraction, and duplicate detection.
"""

import os
import hashlib
from PIL import Image, ExifTags
from app.core.config import settings, get_storage_path
from app.core.database import get_database

class StorageService:
    @staticmethod
    def get_upload_dir():
        return get_storage_path("uploads")

    @staticmethod
    def calculate_sha256(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    @staticmethod
    def extract_exif(filepath: str) -> dict:
        metadata = {
            "has_exif": False,
            "timestamp": None,
            "make": None,
            "model": None,
            "gps_latitude": None,
            "gps_longitude": None
        }
        try:
            with Image.open(filepath) as img:
                exif_data = img._getexif()
                if not exif_data:
                    return metadata
                
                metadata["has_exif"] = True
                for tag_id, value in exif_data.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    if tag == "DateTimeOriginal" or tag == "DateTime":
                        metadata["timestamp"] = str(value)
                    elif tag == "Make":
                        metadata["make"] = str(value)
                    elif tag == "Model":
                        metadata["model"] = str(value)
                    elif tag == "GPSInfo":
                        metadata["has_gps"] = True
        except Exception:
            pass
        return metadata

    @classmethod
    def save_file(cls, filename: str, content: bytes, claim_id: str, uploader: str) -> dict:
        sha256_hash = cls.calculate_sha256(content)
        db = get_database()

        # Check for duplicates across the database
        existing = db.evidence.find_one({"sha256_hash": sha256_hash})
        is_duplicate = existing is not None
        duplicate_of = existing.get("evidence_id") if is_duplicate else None

        upload_dir = cls.get_upload_dir()
        clean_filename = f"{claim_id}_{filename}"
        filepath = os.path.join(upload_dir, clean_filename)

        with open(filepath, "wb") as f:
            f.write(content)

        ext = os.path.splitext(filename)[1].lower()
        file_type = "image" if ext in [".jpg", ".jpeg", ".png", ".webp"] else "document"

        exif_info = {}
        if file_type == "image":
            exif_info = cls.extract_exif(filepath)

        return {
            "file_name": clean_filename,
            "original_name": filename,
            "file_type": file_type,
            "file_size": f"{len(content) / 1024:.1f} KB",
            "storage_path": f"storage/uploads/{clean_filename}",
            "sha256_hash": sha256_hash,
            "is_duplicate": is_duplicate,
            "duplicate_of": duplicate_of,
            "exif": exif_info
        }

