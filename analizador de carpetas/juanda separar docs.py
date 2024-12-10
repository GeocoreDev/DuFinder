import regex
import olefile

def open_doc_as_text(file_path):
    try:
        with olefile.OleFileIO(file_path) as ole:
            # Extract text from Word document and handle decoding errors
            text_stream = ole.openstream('WordDocument').read()
            text = text_stream.decode('utf-8', errors='replace')
            return text
    except Exception as e:
        print(f"Error opening the document: {e}")
        return None

def find_words_in_text(text, pattern):
    matches = regex.findall(pattern, text)
    return matches

# Replace the file path with the path to your specific document
document_path = "D:/1998/GYC 0298-0414 Perforaciones mobil 194 autonorte/GYC014-98 CARTA REMISIÓN MUESTRAS-LAB.doc"

# Open the Word document as text
document_text = open_doc_as_text(document_path)

if document_text:
    # Define a regular expression pattern for finding words in Spanish
    # This pattern includes letters with diacritics (accents) commonly used in Spanish
    word_pattern = r'\b\p{L}+\b'

    # Find words in the document text
    found_words = find_words_in_text(document_text, word_pattern)

    # Delete single-lettered words
    filtered_words = [word for word in found_words if len(word) > 1]

    # Print the filtered words
    print("Filtered Words in Spanish (without single-lettered words):")
    print(filtered_words)
