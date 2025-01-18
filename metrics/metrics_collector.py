from typing import Dict, Callable
from .clip_similarity import CLIPSimilarity
from .object_detection_matching import ObjectDetectionMatching
from .fid_metric import FIDMetric
import os
from abc import ABC, abstractmethod

class MetricCalculator(ABC):
    @abstractmethod
    def compute(self, image_path: str, description: str) -> float:
        pass

class CLIPSimilarityCalculator(MetricCalculator):
    def __init__(self, clip_similarity: CLIPSimilarity):
        self.clip_similarity = clip_similarity

    def compute(self, image_path: str, description: str) -> float:
        return self.clip_similarity.compute_similarity(image_path, description)

class ObjectDetectionCalculator(MetricCalculator):
    def __init__(self, object_detection: ObjectDetectionMatching):
        self.object_detection = object_detection

    def compute(self, image_path: str, description: str) -> float:
        return self.object_detection.compute_object_match_score(image_path, description)

class FIDCalculator(MetricCalculator):
    def __init__(self, fid_metric: FIDMetric):
        self.fid_metric = fid_metric

    def compute(self, image_path: str, description: str) -> float:
        return self.fid_metric.compute_fid(image_path, description)

class MetricsCollector:
    """A class to collect and manage various metrics for image-text comparison."""

    def __init__(self, uuid: str):
        """Initialize the MetricsCollector with different metric calculators."""
        self.uuid = uuid
        clip_similarity = CLIPSimilarity()
        object_detection = ObjectDetectionMatching()
        fid_metric = FIDMetric()
        
        self.calculators = {
            'clip_similarity': CLIPSimilarityCalculator(clip_similarity),
            'object_match_score': ObjectDetectionCalculator(object_detection),
            'fid_score': FIDCalculator(fid_metric)
        }
        
        self.image_paths = {
            'original': os.path.join("storage", "data", uuid, "original.png"),
            'generated': os.path.join("storage", "data", uuid, "generated.png")
        }
        
        description_path = os.path.join("storage", "data", uuid, "description.txt")
        with open(description_path, "r") as f:
            self.description = f.read()

    def _compute_metric(self, calculator: MetricCalculator, image_path: str) -> float:
        try:
            return calculator.compute(image_path, self.description)
        except Exception as e:
            print(f"Error computing metric: {str(e)}")
            return 0.0

    def collect_metrics(self) -> Dict[str, float]:
        """Collect all metrics for the given images and description."""
        metrics = {}
        
        for image_type, image_path in self.image_paths.items():
            for metric_name, calculator in self.calculators.items():
                metric_key = f"{image_type}_{metric_name}"
                metrics[metric_key] = self._compute_metric(calculator, image_path)
        
        return metrics

    def print_metrics(self, metrics: Dict[str, float]):
        """Print the collected metrics in a formatted manner."""
        print("\n=== Image-Text Comparison Metrics ===")
        for metric_name, metric_value in metrics.items():
            print(f"{metric_name.replace('_', ' ').title()}: {metric_value:.2f}")
        print("=====================================\n")

    def analyze(self):
        """Analyze the images and description, collect metrics, and print the results."""
        metrics = self.collect_metrics()
        self.print_metrics(metrics)