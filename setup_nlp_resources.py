import nltk
import spacy

try:
    nltk.download("punkt_tab")
    spacy.cli.download("en_core_web_md")  # Use the medium-sized model for semantic tasks
except Exception as e:
        print(f"An error occurred while downloading NLP models: {e}")