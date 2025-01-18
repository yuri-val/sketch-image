import numpy as np
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import traceback
from scipy.linalg import sqrtm  # Correct import


class FIDMetric:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def extract_features(self, image_path=None, text=None):
        inputs = None
        if image_path:
            image = Image.open(image_path).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt", padding=True)
        elif text:
            inputs = self.processor(text=[text], return_tensors="pt", padding=True, truncation=True)

        if inputs:
            with torch.no_grad():
                outputs = (
                    self.model.get_image_features(**inputs)
                    if image_path
                    else self.model.get_text_features(**inputs)
                )
            features = outputs.cpu().numpy()
            features = features / np.linalg.norm(features, axis=1, keepdims=True)  # Normalize
            return features  # Return full feature array
        else:
            raise ValueError("Either image_path or text must be provided.")

    def calculate_fid(self, features1, features2):
        if features1.shape != features2.shape:
            raise ValueError(f"Feature shapes do not match: {features1.shape} vs {features2.shape}")

        # Compute mean
        mu1, mu2 = np.mean(features1, axis=0), np.mean(features2, axis=0)

        # Handle covariance matrices
        if features1.shape[0] == 1 or features2.shape[0] == 1:
            # Fallback for single-sample case
            sigma1 = np.zeros((features1.shape[1], features1.shape[1]))
            sigma2 = np.zeros((features2.shape[1], features2.shape[1]))
        else:
            sigma1 = np.cov(features1, rowvar=False)
            sigma2 = np.cov(features2, rowvar=False)

        # Compute the FID score
        diff = mu1 - mu2
        covmean = sqrtm(sigma1 @ sigma2 + np.eye(sigma1.shape[0]) * 1e-6)  # Add small epsilon for stability

        # Handle numerical issues
        if np.iscomplexobj(covmean):
            covmean = covmean.real

        fid = diff.dot(diff) + np.trace(sigma1 + sigma2 - 2 * covmean)
        return fid

    def compute_fid(self, image_path: str, description: str) -> float:
        try:
            image_features = self.extract_features(image_path=image_path)
            text_features = self.extract_features(text=description)

            print(f"Image features shape: {image_features.shape}")
            print(f"Text features shape: {text_features.shape}")

            fid_score = self.calculate_fid(image_features, text_features)
            return fid_score
        except Exception as e:
            print(f"Error computing FID score: {str(e)}")
            print("Traceback:")
            print(traceback.format_exc())
            return float('inf')  # Return infinity for error cases
