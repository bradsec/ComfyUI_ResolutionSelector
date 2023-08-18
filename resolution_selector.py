
# Define resolution presets
# Resolutions which appear to work well for SDXL as used in https://github.com/lllyasviel/Fooocus
BASE_RESOLUTIONS = [
    (1024, 1024),
    (704, 1408),
    (704, 1344),
    (768, 1344),
    (768, 1280),
    (832, 1216),
    (832, 1152),
    (896, 1152),
    (896, 1088),
    (960, 1088),
    (960, 1024),
    (1024, 960),
    (1088, 960),
    (1088, 896),
    (1152, 896),
    (1152, 832),
    (1216, 832),
    (1280, 768),
    (1344, 768),
    (1344, 704),
    (1408, 704),
    (1472, 704),
    (1536, 640),
    (1600, 640),
    (1664, 576),
    (1728, 576)
]

# Create a list of resolution strings for the drop-down menu
resolution_strings = [f"{width}x{height}" for width, height in BASE_RESOLUTIONS]

# Create the custom node class
class ResolutionSelector:
    """
    A node to provide a drop-down list of resolutions and returns two int values (width and height).
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        """
        Return a dictionary which contains config for all input fields.
        """
        return {
            "required": {
                "base_resolution": (resolution_strings,),
                "base_adjustment": (["SDXL (None)", "SD21 (75%)", "SD15 (50%)"],)
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "select_resolution"
    CATEGORY = 'utils'

    @staticmethod
    def select_resolution(base_resolution, base_adjustment):
        """
        Returns the width and height based on the selected resolution and adjustment.

        Args:
            base_resolution (str): Selected resolution in the format "widthxheight".
            base_adjustment (str): Selected adjustment (resolution values reduction) based on Stable Diffusion version.

        Returns:
            Tuple[int, int]: Adjusted width and height.
        """
        try:
            width, height = map(int, base_resolution.split('x'))
        except ValueError:
            raise ValueError("Invalid base_resolution format.")

        adjustment_factors = {"SDXL (None)": 1, "SD21 (75%)": 0.75, "SD15 (50%)": 0.5}
        factor = adjustment_factors.get(base_adjustment)

        if factor is None:
            raise ValueError("Invalid base_adjustment value.")

        width = int(width * factor)
        height = int(height * factor)

        return width, height

NODE_CLASS_MAPPINGS = {
    "ResolutionSelector": ResolutionSelector,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ResolutionSelector": "Resolution Selector (w x h)",
}