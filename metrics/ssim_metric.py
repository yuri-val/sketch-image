"""Module for computing Structural Similarity Index (SSIM) between images."""

from typing import Tuple
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


class SSIMMetric:
    """
    **SSIM (Structural Similarity Index)**
    - **Опис**: Вимірює структурну схожість між двома зображеннями, враховуючи яскравість, контрастність і структуру.
    - **Діапазон значень**: Від 0 до 1.
      - **1**: Ідеальна структурна схожість (зображення ідентичні).
      - **0**: Відсутність структурної схожості.
    - **Трактування**:
      - **0.8–1.0**: Висока схожість між зображеннями.
      - **0.5–0.8**: Помітні структурні відмінності, але частково схожі.
      - **< 0.5**: Значна різниця в структурі зображень.
    """
    
    def __init__(self):
        """
        Initialize SSIMMetric with paths to two images.
        """

    @staticmethod
    def load_and_preprocess_image(image_path: str) -> np.ndarray:
        """
        Load and preprocess an image from the given path.

        Args:
            image_path (str): Path to the image file.

        Returns:
            np.ndarray: Grayscale image as a numpy array.
        """
        return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    @staticmethod
    def ensure_same_dimensions(image1: np.ndarray, image2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Ensure that both images have the same dimensions.

        Args:
            image1 (np.ndarray): First image.
            image2 (np.ndarray): Second image.

        Returns:
            Tuple[np.ndarray, np.ndarray]: Tuple of images with the same dimensions.
        """
        if image1.shape != image2.shape:
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
        return image1, image2

    def compute_ssim(self, image1_path: str, image2_path: str) -> float:
        """
        Compute the Structural Similarity Index (SSIM) between two images.

        Returns:
            float: SSIM score between the two images.
        """
        image1 = self.load_and_preprocess_image(image1_path)
        image2 = self.load_and_preprocess_image(image2_path)

        image1, image2 = self.ensure_same_dimensions(image1, image2)

        score, _ = ssim(image1, image2, full=True)
        return float(score)