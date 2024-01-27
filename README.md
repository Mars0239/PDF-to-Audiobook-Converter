# PDF to Audiobook Converter

This Python script enables the conversion of PDF documents into audiobooks using Optical Character Recognition (OCR) and Google Cloud Text-to-Speech API.

## Description

The `pdf_to_audiobook.py` script takes a PDF file as input, extracts the text, and uses the Google Cloud Text-to-Speech API to convert the text into an MP3 audio file. It can handle both standard and scanned (image-based) PDF documents.

## Features

- Extract text from standard PDF files.
- Perform OCR on scanned PDFs to extract text.
- Convert extracted text to natural-sounding speech.
- Save the speech as an MP3 audio file.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or above is installed.
- Required Python libraries are installed: `PyPDF2`, `pytesseract`, `Pillow`, `google-cloud-texttospeech`, `pdf2image`, `tqdm`.
- Google Cloud account with the Text-to-Speech API enabled.
- Service account key from Google Cloud for API authentication.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/PDF-to-Audiobook-Converter/pdf-to-audiobook.git
2. Navigate to the project directory:
   ```sh
   cd pdf-to-audiobook
3. Install the required packages:
   ```sh
   pip install -r requirements.txt

## Usage

To use the PDF to Audiobook converter, follow these steps:
1. Set your Google Cloud service account JSON key file path in the script:
   ```sh
   os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account-file.json"
2. Run the script with the required arguments:
   ```sh
   python pdf_to_audiobook.py <path_to_pdf> <output_audio_file> <language_code>

   ## Replace <path_to_pdf>, <output_audio_file>, and <language_code> with your PDF's path, desired output audio file's name, and language code respectively.

## Contributing

Contributions to the project are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact

If you have any questions or feedback, please reach out to me.
Thank you for trying out the PDF to Audiobook converter!



