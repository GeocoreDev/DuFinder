import regex
import olefile

def open_doc_as_text(file_path):
    try:
        with olefile.OleFileIO(file_path) as ole:
            # Extract text from Word document and handle decoding errors
            text_stream = ole.openstream('WordDocument').read()
            text = text_stream.decode('latin-1', errors='replace')
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
    # Exclude specific characters À, ÿ, and symbols initially
    initial_word_pattern = r'\b(?:[^\W\d_Àÿ]|[\d])+?\b'

    # Find words in the document text initially
    initial_found_words = find_words_in_text(document_text, initial_word_pattern)

    # Delete single-lettered words initially
    initial_filtered_words = [word for word in initial_found_words if len(word) > 1]

    # Define characters to be excluded after the first word
    additional_excluded_chars = 'ÕþåÀÿ'

    # Remove additional excluded characters from the words after the first one
    final_filtered_words = [initial_filtered_words[0]] + [word.translate(str.maketrans('', '', additional_excluded_chars)) for word in initial_filtered_words[1:]]

    # Convert the list to a string with elements separated by a space
    final_string = ' '.join(final_filtered_words)

    # Print the final string
    print("Final String:")
    print(final_string)
