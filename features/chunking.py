# NLTK and Spacy download is done in docker env creation in the setup_nlp_resources.py file.
from nltk.tokenize import sent_tokenize
from spacy.vocab import Vocab
from spacy.tokens import Doc
from spacy.tokens import Token

# Splits a given body of text into chunks that are approximately of size 'chunk_size'
def chunk_text(text: str, chunk_size: int, nlp) -> list:

    if not text:
        raise ValueError("Text cannot be empty.")
    if chunk_size <= 0:
        raise ValueError("Chunk size must be a positive integer.")
    

    # Split text at sentence boundaries usint nltk sent_tokenize
    # documentation reference: https://www.nltk.org/api/nltk.tokenize.html#nltk.tokenize.sent_tokenize
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_chunk_length = 0  # Track the total length of the current chunk
    current_chunk_vector = None  # Store the semantic vector for the chunk
    similarity_threshold = 0.625
    buffer = int(0.2 * chunk_size)  # 20% buffer for flexibility

    for sentence in sentences:
        # Generate semantic representation for the sentence
        sentence_doc = nlp(sentence)
        sentence_length = len(sentence)

        # Check if the sentence fits within the chunk size
        fits_in_chunk = current_chunk_length + sentence_length <= chunk_size
        fits_in_chunk_with_buffer = current_chunk_length + sentence_length <= chunk_size + buffer

        # Calculate semantic similarity with the current chunk
        is_semantically_related = False
        if current_chunk_vector is not None:
            # Create a dummy Doc and assign the custom vector
            dummy_doc = Doc(nlp.vocab, words=["DUMMY"])
            dummy_doc.vector = current_chunk_vector
            similarity = dummy_doc.similarity(sentence_doc)
            # print(sentence)
            # print(similarity)
            is_semantically_related = similarity >= similarity_threshold
        else:
            # First sentence always starts the chunk
            is_semantically_related = True

        # Add sentence to the current chunk if it fits
        if fits_in_chunk or (fits_in_chunk_with_buffer and is_semantically_related):
            current_chunk.append(sentence)
            current_chunk_length += sentence_length + 1  # Account for the space
            # Update the chunk vector incrementally
            if current_chunk_vector is None:
                current_chunk_vector = sentence_doc.vector
            else:
                current_chunk_vector = (
                    (current_chunk_vector * (len(current_chunk) - 1) + sentence_doc.vector) / len(current_chunk)
                )
        else:
            # Finalize the current chunk and start a new one
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_chunk_length = sentence_length + 1  # Reset chunk length
            current_chunk_vector = sentence_doc.vector  # Reset chunk vector

    # Add any remaining sentences to the final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

    