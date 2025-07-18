import subprocess
import pathlib
import datetime

def ocr_pdf():
    """Runs OCR on the reference PDF and creates a searchable PDF and a text sidecar."""
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    pdf_path = base_dir / 'data' / 'raw' / 'Al-Muhaddithat.pdf'
    ocr_dir = base_dir / 'data' / 'ocr'
    ocr_dir.mkdir(exist_ok=True)

    output_pdf = ocr_dir / 'Al-Muhaddithat-ocr.pdf'
    log_file = ocr_dir / 'Al-Muhaddithat-ocr.log'

    if not pdf_path.exists():
        print(f"Error: Input PDF not found at {pdf_path}")
        print("Please run the download script first.")
        return

    print(f"Starting OCR on {pdf_path}...")

    # Construct the absolute path to the ocrmypdf executable within the venv
    ocrmypdf_exe = base_dir / '.venv' / 'Scripts' / 'ocrmypdf.exe'

    if not ocrmypdf_exe.exists():
        print(f"Error: ocrmypdf.exe not found at {ocrmypdf_exe}")
        print("Please ensure the virtual environment is set up correctly.")
        return

    try:
        subprocess.run([
            str(ocrmypdf_exe),
            '--output-type', 'pdf',
            '--sidecar', str(output_pdf.with_suffix('.txt')),
            '--tesseract-timeout', '0',
            str(pdf_path), str(output_pdf)
        ], check=True)

        log_message = f"OCR completed successfully on {datetime.datetime.utcnow().isoformat()}\n"
        log_file.write_text(log_message)
        print(log_message)
        print(f"Searchable PDF saved to: {output_pdf}")
        print(f"Text sidecar saved to: {output_pdf.with_suffix('.txt')}")

    except FileNotFoundError:
        print("Error: 'ocrmypdf' command not found.")
        print("Please ensure ocrmypdf and its dependencies (tesseract, ghostscript) are installed and in your system's PATH.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during OCR processing: {e}")

if __name__ == '__main__':
    ocr_pdf()
