# =====================================================
# STEP 1 — CV PREPROCESSING (PDF + IMAGE → PAGE IMAGES)
# =====================================================
# Purpose:
# - Convert a CV PDF into page-level PNG images
# - Allow direct processing of PNG, JPG, JPEG images
# - Apply minimal preprocessing suitable for OCR
# - Preserve page order and layout
# =====================================================

import os
import sys
import cv2
from pathlib import Path
from pdf2image import convert_from_path


# -------------------------------
# PDF → PNG conversion
# -------------------------------
def pdf_to_images(pdf_path, output_dir="pages", dpi=300, poppler_path=None):
    """
    Converts each page of a PDF into a PNG image.
    """
    os.makedirs(output_dir, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
    image_paths = []
    for i, page in enumerate(pages):
        path = os.path.join(output_dir, f"page_{i+1}.png")
        page.save(path, "PNG")
        image_paths.append(path)
    return image_paths


# -------------------------------
# Minimal image preprocessing
# -------------------------------
def preprocess_image(image_path, save_path):
    """
    Minimal preprocessing for CV OCR:
    - Grayscale
    - Light denoising
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise RuntimeError(f"Failed to read image: {image_path}")
    img = cv2.medianBlur(img, 3)
    cv2.imwrite(save_path, img)


# -------------------------------
# Main pipeline function
# -------------------------------
def main(file_path, output_dir="pages", poppler_path=None):
    """
    Main callable pipeline (Notebook + Script safe)
    Supports PDF + single PNG/JPG/JPEG images
    """
    file_path = Path(file_path)
    os.makedirs(output_dir, exist_ok=True)

    # Determine input type
    if file_path.suffix.lower() == ".pdf":
        pages = pdf_to_images(str(file_path), output_dir=output_dir, poppler_path=poppler_path)
    elif file_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
        pages = [str(file_path)]  # treat single image like a page
    else:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")

    # Preprocess each page/image
    for i, page in enumerate(pages):
        out_path = os.path.join(output_dir, f"processed_{i+1}.png")
        preprocess_image(page, out_path)

    print(f"[STEP 1] Processed {len(pages)} pages → {output_dir}")


# -------------------------------
# CLI entry point
# -------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python step1_preprocess_pdf.py <file.pdf/png/jpg> [output_dir]")
        sys.exit(1)

    file_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "pages"

    # WINDOWS: set Poppler path here if not in PATH
    POPPLER_PATH = r"C:\poppler\Library\bin"  # change if needed

    main(file_path, output_dir, poppler_path=POPPLER_PATH)
