import numpy as np
from pathlib import Path
from config.settings import settings


class AbnormalModel:
    def __init__(self, model_path: str | None = None):
        self.model_path = model_path or settings.MODEL_PATH
        self.model = None
        
        # 🎯 ADAPTIVE THRESHOLD INITIALIZATION
        self.adaptive_threshold = 0.161  # Original threshold
        
        # BASELINE CALIBRATION for domain adaptation
        self.baseline_confidence = 0.0
        self.baseline_samples = []
        self.baseline_collection_time = 5  # 5 seconds
        self.baseline_start_time = None
        self.is_calibrating = True
        
        self.abnormal_rate = 0.0
        self.prediction_count = 0
        self.abnormal_count = 0

    def load(self) -> bool:
        if self.model is not None:
            return True
        path = Path(self.model_path)
        if not path.exists():
            print(f"Model file not found at {path}")
            return False
        try:
            import tensorflow as tf
            from keras.layers import Layer

            class AttentionPooling(Layer):
                def call(self, inputs):
                    attn_out, attn_scores = inputs
                    weights = tf.nn.softmax(attn_scores, axis=1)
                    return tf.reduce_sum(attn_out * weights, axis=1)

                def compute_output_shape(self, input_shape):
                    return (input_shape[0][0], input_shape[0][-1])

            self.model = tf.keras.models.load_model(
                str(path),
                compile=False,
                custom_objects={'AttentionPooling': AttentionPooling}
            )
            print(f"✅ TensorFlow Model loaded successfully: {type(self.model)}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            return False

    def is_loaded(self) -> bool:
        return self.model is not None

    def start_baseline_calibration(self):
        """Start collecting baseline samples for domain adaptation"""
        import time
        self.baseline_start_time = time.time()
        self.baseline_samples = []
        self.is_calibrating = True
        print(f" [BASELINE] Starting calibration for {self.baseline_collection_time} seconds...")

    def add_baseline_sample(self, confidence):
        """Add confidence sample to baseline collection"""
        if self.is_calibrating:
            import time
            current_time = time.time()
            
            # Check if calibration period is over
            if current_time - self.baseline_start_time >= self.baseline_collection_time:
                self.finalize_baseline()
                return
            
            # Add sample
            self.baseline_samples.append(confidence)
            elapsed = current_time - self.baseline_start_time
            remaining = self.baseline_collection_time - elapsed
            print(f" [BASELINE] Collecting sample {len(self.baseline_samples)} - {remaining:.1f}s remaining")

    def finalize_baseline(self):
        """Calculate baseline from collected samples"""
        if self.baseline_samples:
            self.baseline_confidence = np.mean(self.baseline_samples)
            self.is_calibrating = False
            print(f" [BASELINE] Calibration complete!")
            print(f"    Samples collected: {len(self.baseline_samples)}")
            print(f"    Baseline confidence: {self.baseline_confidence:.3f}")
            print(f"    Ready for detection with bias removal")

    def apply_baseline_calibration(self, confidence):
        """Apply baseline calibration to remove domain bias"""
        if self.is_calibrating:
            self.add_baseline_sample(confidence)
            return 0.0  # Return 0 during calibration

        # Check if baseline is ready
        if self.baseline_confidence is None or self.baseline_confidence == 0:
            print(f" [BASELINE] Baseline not ready, using raw confidence: {confidence:.3f}")
            return confidence

        # Apply baseline subtraction
        calibrated_confidence = confidence - self.baseline_confidence
        calibrated_confidence = max(0, calibrated_confidence)  # Ensure non-negative

        print(f" [BASELINE] Raw: {confidence:.3f} -> Baseline: {self.baseline_confidence:.3f} -> Calibrated: {calibrated_confidence:.3f}")

        return calibrated_confidence

    def predict(self, frames_tensor):
        if not self.is_loaded():
            if not self.load():
                raise ValueError("Model not loaded.")

        # Ensure frames_tensor has batch dimension
        if len(frames_tensor.shape) == 4:
            frames_tensor = np.expand_dims(frames_tensor, axis=0)

        pred = self.model.predict(frames_tensor)
        logits = pred[0][0]
        
        # Convert logits to probability using sigmoid function
        confidence = float(1 / (1 + np.exp(-logits)))
        
        # Apply baseline calibration for domain adaptation
        calibrated_confidence = self.apply_baseline_calibration(confidence)

        return calibrated_confidence
