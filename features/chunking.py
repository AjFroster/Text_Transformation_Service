import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt_tab")
# nltk.data.path.append(r"../libraries/nltk_data/tokenizers")

# nltk.data.path.append(r'C:/Users/ajfos/AppData/Roaming/nltk_data')
# print("NLTK Data Paths: ", nltk.data.path)
# nltk.data.find('tokenizers/punkt')
def chunk_text(text: str, chunk_size: int)->list:
    # Splits a given body of text into chunks that are approximately of size 'chunk_size'
    
    if not text:
        raise ValueError("Text cannot be empty.")
    if chunk_size <= 0:
        raise ValueError("Chunk size must be a positive integer.")
    
    # Split text at sentence boundaries usint nltk sent_tokenize
    # documentation reference: https://www.nltk.org/api/nltk.tokenize.html#nltk.tokenize.sent_tokenize
    sentences = sent_tokenize(text)
    print("sentences: ", sentences)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # Check if adding the new sentence to the existing chunk  
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += (sentence + " ")
        else:
            # Append current chunk to list and start on new chunk
            # 
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
                
            current_chunk = sentence + " "
    
    # Ensure that if there is an existing chunk it is appended to chunks
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks