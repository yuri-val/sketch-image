from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

class CLIPSimilarity:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def compute_similarity(self, image_path: str, description: str) -> float:
        """
        Compute the CLIP similarity score between an image and a text description.

        Args:
            image_path (str): Path to the image file.
            description (str): Text description to compare with the image.

        Returns:
            float: Similarity score between 0 and 100.
        """
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')

            # Truncate description to fit within CLIP's maximum sequence length
            max_length = self.processor.tokenizer.model_max_length
            truncated_description = self.processor.tokenizer.tokenize(description)[:max_length]
            truncated_description = self.processor.tokenizer.convert_tokens_to_string(truncated_description)

            # Prepare inputs
            inputs = self.processor(
                text=[truncated_description],
                images=image,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=max_length
            )

            # Compute similarity
            with torch.no_grad():
                outputs = self.model(**inputs)

            # Get the raw similarity score
            similarity = outputs.logits_per_image.item()

            return similarity
        except Exception as e:
            print(f"Error computing CLIP similarity: {str(e)}")
            return 0.0