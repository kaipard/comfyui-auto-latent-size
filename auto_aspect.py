import torch

class AutoAspectLatent:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "use_aspect_ratio": (["true", "false"],),
                "aspect_ratio": (
                    ["1:1", "4:3", "16:9", "9:16", "3:4", "2:3", "3:2", "1:2", "2:1"],
                ),
                "height_value": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 99}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)

    FUNCTION = "generate_latent"
    CATEGORY = "latent/generator"

    def generate_latent(
        self,
        width,
        use_aspect_ratio,
        aspect_ratio,
        height_value,
        batch_size
    ):
        ratio_map = {
            "1:1": 1.0,
            "4:3": 3 / 4,
            "16:9": 9 / 16,
            "9:16": 16 / 9,
            "3:4": 1.0,
            "2:3": 1.5,
            "3:2": 2 / 3,
            "1:2": 2.0,
            "2:1": 1 / 2
        }

        if use_aspect_ratio == "true":
            height = int(width * ratio_map.get(aspect_ratio, 1.0))
        else:
            height = height_value

        latent_w = width // 8
        latent_h = height // 8

        latent = torch.zeros([batch_size, 4, latent_h, latent_w], dtype=torch.float32)
        return ({"samples": latent},)
    def __init__(self):
        print("Loaded node class:", self.__class__.__name__)
