import os
import sys
import PyPDF2
import pytesseract
import concurrent.futures
from tqdm import tqdm
from PIL import Image
from google.cloud import texttospeech
from pdf2image import convert_from_path

# Set up Google Cloud credentials
# Make sure to replace 'path_to_your_service_account_json' with the actual path to your JSON key file.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_service_account_json"

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a regular PDF file using PyPDF2.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_scanned_pdf(pdf_path):
    """
    Extracts text from scanned PDF files using OCR (Optical Character Recognition).
    Converts PDF pages to images and then uses pytesseract to extract text from these images.
    """
    text = ""
    try:
        images = convert_from_path(pdf_path)
        for image in images:
            text += pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Error processing scanned PDF: {e}")
    return text

def text_to_speech(text, output_audio_file, language_code='en-US'):
    """
    Converts text to speech using Google Cloud Text-to-Speech API and saves the audio to an MP3 file.
    """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    if not text.strip():
        print("No text to synthesize")
        return

    try:
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        if response.audio_content:
            with open(output_audio_file, 'wb') as out:
                out.write(response.audio_content)
                print(f"Audio content written to file {output_audio_file}")
        else:
            print("No audio content received from the API.")
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")

def process_pdf_concurrently(pdf_path, output_audio_file, language_code):
    """
    Processes the given PDF file and generates an audiobook.
    It first tries to extract text directly from the PDF and if it fails (e.g., if the PDF is a scanned document),
    it attempts to use OCR. It then converts the extracted text to speech using Google's Text-to-Speech API.
    """
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("PDF appears to be scanned, attempting OCR...")
        text = extract_text_from_scanned_pdf(pdf_path)

    if not text:
        print("No text could be extracted from the PDF.")
        return

    max_chunk_size = 5000  # Adjust as needed based on API limits and memory constraints
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

    # Using ThreadPoolExecutor to process multiple chunks in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(text_to_speech, chunk, output_audio_file, language_code)
                   for chunk in chunks]
        # tqdm is used to display a progress bar for the audio conversion process
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(chunks), desc="Processing PDF"):
            pass  # We just need to iterate through the futures to make the progress bar work properly

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <path_to_pdf> <output_audio_file> <language_code>")
        sys.exit(1)

    # Command line arguments
    pdf_path = sys.argv[1]
    output_audio_file = sys.argv[2]
    language_code = sys.argv[3]

    process_pdf_concurrently(pdf_path, output_audio_file, language_code)
