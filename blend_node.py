import torch
import numpy as np
from PIL import Image
from blend_modes import soft_light, lighten_only, dodge, addition, darken_only, multiply, hard_light, difference, subtract, grain_extract, grain_merge, divide, overlay, normal

class BlendImageNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_image": ("IMAGE", {"tooltip": "The base image to blend."}),
                "overlay_image": ("IMAGE", {"tooltip": "The overlay image."}),
                "blend_mode": ([
                    "soft_light", "lighten_only", "dodge", "addition", "darken_only",
                    "multiply", "hard_light", "difference", "subtract",
                    "grain_extract", "grain_merge", "divide", "overlay", "normal"
                ], {"default": "soft_light"}),
                "opacity": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "position": ([
                    "top_left", "top_center", "top_right",
                    "mid_left", "mid_center", "mid_right",
                    "bottom_left", "bottom_center", "bottom_right"
                ], {"default": "bottom_right", "tooltip": "Anchor point for placing the overlay."}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "blend_image"
    CATEGORY = "image"

    def pad_overlay_to_position(self, overlay, base_h, base_w, position):
        """Pad the overlay image to the full base image size, anchored according to position."""
        overlay_h, overlay_w, _ = overlay.shape
        pad_top, pad_bottom = 0, base_h - overlay_h
        pad_left, pad_right = 0, base_w - overlay_w

        # Vertical alignment
        if "top" in position:
            pad_top = 0
            pad_bottom = base_h - overlay_h
        elif "mid" in position:
            pad_top = (base_h - overlay_h) // 2
            pad_bottom = base_h - overlay_h - pad_top
        elif "bottom" in position:
            pad_top = base_h - overlay_h
            pad_bottom = 0

        # Horizontal alignment
        if "left" in position:
            pad_left = 0
            pad_right = base_w - overlay_w
        elif "center" in position:
            pad_left = (base_w - overlay_w) // 2
            pad_right = base_w - overlay_w - pad_left
        elif "right" in position:
            pad_left = base_w - overlay_w
            pad_right = 0

        return np.pad(
            overlay,
            ((pad_top, pad_bottom), (pad_left, pad_right), (0, 0)),
            mode='constant',
            constant_values=0
        )

    def to_rgba(self, img):
        """Ensure a (H, W, 3) or (H, W, 4) float32 image [0.0–1.0] is converted to (H, W, 4) RGBA [0.0–255.0]"""
        h, w, c = img.shape
        if c == 3:
            alpha = np.ones((h, w, 1), dtype=np.float32)
            img = np.concatenate([img, alpha], axis=2)
        return (img * 255.0).astype(np.float32)

    def from_rgba(self, img):
        """Convert (H, W, 4) float32 [0–255] back to RGB [0–1]"""
        rgb = img[..., :3]
        return np.clip(rgb / 255.0, 0.0, 1.0)

    def blend_image(self, base_image, overlay_image, blend_mode, opacity, position):
        # Get blending function
        blend_functions = {
            "soft_light": soft_light,
            "lighten_only": lighten_only,
            "dodge": dodge,
            "addition": addition,
            "darken_only": darken_only,
            "multiply": multiply,
            "hard_light": hard_light,
            "difference": difference,
            "subtract": subtract,
            "grain_extract": grain_extract,
            "grain_merge": grain_merge,
            "divide": divide,
            "overlay": overlay,
            "normal": normal
        }
        blend_fn = blend_functions.get(blend_mode, soft_light)

        base_np = base_image[0].cpu().numpy()
        overlay_np = overlay_image[0].cpu().numpy()

        base_h, base_w, _ = base_np.shape
        overlay_h, overlay_w, _ = overlay_np.shape

        if overlay_h > base_h or overlay_w > base_w:
            raise ValueError("Overlay image must be smaller than or equal to base image dimensions.")

        base_rgba = self.to_rgba(base_np)
        overlay_rgba = self.to_rgba(overlay_np)

        padded_overlay = self.pad_overlay_to_position(overlay_rgba, base_h, base_w, position)

        blended = blend_fn(base_rgba, padded_overlay, opacity)
        blended_rgb = self.from_rgba(blended)
        blended_tensor = torch.from_numpy(blended_rgb).unsqueeze(0)

        return (blended_tensor,)

