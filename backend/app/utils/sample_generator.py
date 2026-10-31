"""
CLAIMSIGHT AI - Sample Evidence Image Generator
Generates realistic inspection cards, damage diagrams, and document previews
saved in backend/storage/uploads/ for demonstration.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def ensure_storage_dir():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    storage_dir = os.path.join(base_dir, "storage", "uploads")
    os.makedirs(storage_dir, exist_ok=True)
    return storage_dir

def create_sample_damage_image(filename: str, title: str, vehicle_info: str, damage_notes: list, color=(240, 245, 250)):
    storage_dir = ensure_storage_dir()
    filepath = os.path.join(storage_dir, filename)
    if os.path.exists(filepath):
        return filepath

    # Create image
    img = Image.new("RGB", (800, 600), color=color)
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (800, 70)], fill=(15, 23, 42))
    draw.text((25, 22), "CLAIMSIGHT AI - VEHICLE EVIDENCE INSPECTION", fill=(255, 255, 255))
    draw.text((560, 25), "FORENSIC COPY", fill=(239, 68, 68))

    # Watermark box
    draw.rectangle([(25, 90), (775, 140)], fill=(226, 232, 240), outline=(203, 213, 225))
    draw.text((40, 105), f"VEHICLE: {vehicle_info} | REF: {filename}", fill=(30, 41, 59))

    # Car schematic silhouette
    draw.rectangle([(150, 180), (650, 420)], outline=(51, 65, 85), width=3)
    # Windshield / roof
    draw.polygon([(260, 180), (320, 240), (480, 240), (540, 180)], outline=(100, 116, 139), width=2)
    # Wheels
    draw.ellipse([(200, 400), (270, 470)], fill=(30, 41, 59))
    draw.ellipse([(530, 400), (600, 470)], fill=(30, 41, 59))

    # Damage annotations
    y_offset = 480
    draw.text((40, y_offset), "OBSERVED DAMAGE / EVIDENCE POINTS:", fill=(15, 23, 42))
    y_offset += 25
    for note in damage_notes:
        draw.text((60, y_offset), f"• {note}", fill=(185, 28, 28))
        y_offset += 22

    # Draw target reticle on damage zone
    draw.ellipse([(520, 310), (620, 390)], outline=(220, 38, 38), width=3)
    draw.line([(570, 290), (570, 410)], fill=(220, 38, 38), width=2)
    draw.line([(500, 350), (640, 350)], fill=(220, 38, 38), width=2)
    draw.text((630, 340), "IMPACT ZONE", fill=(220, 38, 38))

    # Metadata stamp footer
    draw.rectangle([(0, 560), (800, 600)], fill=(241, 245, 249))
    draw.text((25, 572), "AUTHENTICATED FORENSIC METADATA RECORDED | SHA-256 VERIFIED", fill=(100, 116, 139))

    img.save(filepath, "JPEG", quality=90)
    return filepath

def create_sample_document_image(filename: str, doc_type: str, details: list):
    storage_dir = ensure_storage_dir()
    filepath = os.path.join(storage_dir, filename)
    if os.path.exists(filepath):
        return filepath

    img = Image.new("RGB", (700, 900), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Document border
    draw.rectangle([(20, 20), (680, 880)], outline=(203, 213, 225), width=2)

    # Header
    draw.rectangle([(20, 20), (680, 90)], fill=(30, 58, 138))
    draw.text((40, 35), "OFFICIAL EVIDENCE ARCHIVE - CLAIMSIGHT AI", fill=(255, 255, 255))
    draw.text((40, 60), f"TYPE: {doc_type.upper()}", fill=(191, 219, 254))

    # Content
    y = 120
    for key, val in details:
        draw.text((50, y), f"{key}:", fill=(71, 85, 105))
        draw.text((220, y), str(val), fill=(15, 23, 42))
        draw.line([(50, y + 25), (650, y + 25)], fill=(241, 245, 249), width=1)
        y += 42

    # Verification stamp
    draw.rectangle([(420, 750), (640, 840)], outline=(16, 185, 129), width=3)
    draw.text((440, 770), "DIGITALLY VERIFIED", fill=(16, 185, 129))
    draw.text((440, 795), "SYSTEM INTAKE RECORD", fill=(5, 150, 105))

    img.save(filepath, "JPEG", quality=90)
    return filepath
