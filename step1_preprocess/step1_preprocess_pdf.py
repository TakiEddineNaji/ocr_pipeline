# =====================================================
# STEP 1 — CV PREPROCESSING (PDF → PAGE IMAGES)
# =====================================================
# Purpose:
# - Convert a CV PDF into page-level PNG images
# - Apply minimal preprocessing suitable for OCR
# - Preserve page order and layout
# =====================================================

import os
import sys
import cv2
from pdf2image import convert_from_path


# -------------------------------
# PDF → PNG conversion
# -------------------------------
def pdf_to_images(pdf_path, output_dir="pages", dpi=300, poppler_path=None):
    """
    Converts each page of a PDF into a PNG image.

    Args:
        pdf_path (str): Path to input PDF
        output_dir (str): Directory to save page images
        dpi (int): Resolution for PDF rendering
        poppler_path (str or None): Path to Poppler binaries (Windows)
    """
    os.makedirs(output_dir, exist_ok=True)

    pages = convert_from_path(
        pdf_path,
        dpi=dpi,
        poppler_path=poppler_path
    )

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
def main(pdf_path, output_dir="pages", poppler_path=None):
    """
    Main callable pipeline (Notebook + Script safe)
    """
    pages = pdf_to_images(
        pdf_path=pdf_path,
        output_dir=output_dir,
        poppler_path=poppler_path
    )

    for i, page in enumerate(pages):
        out_path = os.path.join(output_dir, f"processed_{i+1}.png")
        preprocess_image(page, out_path)

    print(f"[STEP 1] Processed {len(pages)} pages → {output_dir}")


# -------------------------------
# CLI entry point
# -------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python step1_preprocess_pdf.py <cv.pdf> [output_dir]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "pages"

    # WINDOWS: set Poppler path here if not in PATH
    POPPLER_PATH = r"C:\poppler\Library\bin"  # change if needed

    main(
        pdf_path=pdf_path,
        output_dir=output_dir,
        poppler_path=POPPLER_PATH
    )
