from typing import Set
from transformers import pipeline
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from ultralytics import YOLO

class ObjectDetectionMatching:
    """A class for matching objects detected in images with objects mentioned in text."""

    def __init__(self, model_path: str = "yolov8s.pt"):
        """
        Initialize the ObjectDetectionMatching class.

        Args:
            model_path (str): Path to the YOLO model file. Defaults to "yolov8s.pt".
        """
        self.detector = YOLO(model_path)
        self.nlp = pipeline("ner")

        # Download required NLTK data
        self._download_nltk_data()

        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def _download_nltk_data(self):
        """Download required NLTK data."""
        required_data = ['punkt', 'punkt_tab', 'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng', 'stopwords', 'wordnet']
        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}')
            except LookupError:
                print(f"Downloading {data}...")
                nltk.download(data, quiet=True)

    def extract_objects_from_text(self, description: str) -> Set[str]:
        """
        Extract objects from the given text description using NER and noun phrase extraction.

        Args:
            description (str): Text description to extract objects from.

        Returns:
            Set[str]: Set of extracted objects.
        """
        # Tokenize and POS tag the description
        tokens = word_tokenize(description.lower())
        pos_tags = pos_tag(tokens)

        # Extract named entities
        ner_entities = self.nlp(description)
        named_entities = {entity['word'].lower() for entity in ner_entities}

        # Extract noun phrases and single nouns
        noun_phrases = set()
        current_phrase = []
        for word, tag in pos_tags:
            if tag.startswith('NN'):
                current_phrase.append(word)
            elif current_phrase:
                noun_phrases.add(' '.join(current_phrase))
                current_phrase = []
        if current_phrase:
            noun_phrases.add(' '.join(current_phrase))

        # Combine and filter the results
        all_objects = named_entities.union(noun_phrases)
        filtered_objects = {
            self.lemmatizer.lemmatize(obj) for obj in all_objects
            if obj not in self.stop_words and len(obj) > 1
        }

        return filtered_objects

    def detect_objects_in_image(self, image_path: str) -> Set[str]:
        """
        Detect objects in the given image.

        Args:
            image_path (str): Path to the image file.

        Returns:
            Set[str]: Set of detected objects.
        """
        results = self.detector(image_path)
        return {
            result.names[int(box.cls)].lower()
            for result in results
            for box in result.boxes
        }

    def compute_object_match_score(self, image_path: str, description: str) -> float:
        """
        Compute the match score between objects in the image and text.

        Args:
            image_path (str): Path to the image file.
            description (str): Text description.

        Returns:
            float: Match score as a percentage.
        """
        try:
            text_objects = self.extract_objects_from_text(description)
            image_objects = self.detect_objects_in_image(image_path)

            print(f"Text objects: {text_objects}")
            print(f"Image objects: {image_objects}")

            if not text_objects or not image_objects:
                return 0.0

            matches = len(text_objects & image_objects)
            return (matches / len(text_objects)) * 100
        except Exception as e:
            print(f"Error computing object match score: {str(e)}")
            return 0.0