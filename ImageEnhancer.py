""" A helper class that will increase an image's contrast in an attempt to make the QR code more visible to opencv"""

from PIL import Image
from pathlib import Path
import tempfile


class ImageEnhancer:
    """ Has a static method that will increase the image's contrast. """

    @staticmethod
    def increase_contrast(path: Path, contrast_level=128, brightness_level=100) -> Path:
        """Will increase the image's contrast and brightness. The function used is as follows:

            F(x-128)+128+b where F (contrast factor) can be less than one or greater than one, b is 
            brightness, x is each pixel's RGB value.

            F = 259(C + 255) / 255(259-C) where C is the desired contrast level

        Args:
            path (Path): Path to the image file
            contrast_level (int, optional): The desired contrast level. Defaults to 128.
            brightness_level (int, optional): The desired brightnes level. Defaults to 100.


        Returns:
            Path: Returns a temporary file path to the adjusted image
        """

        """"""

        __temp_image = Path(tempfile.gettempdir())
        __temp_image = __temp_image / (path.stem + '_TEMP' + path.suffix)

        #print("TEMP PATH: " + str(__temp_image))

        with Image.open(path) as image:

            C = contrast_level

            contrast_factor = (259 * (C + 255)) / (255 * (259 - C))
            # print(contrast_factor)

            out = image.point(lambda i: contrast_factor *
                              (i - 128) + 128 + brightness_level)

            out.save(__temp_image)

            return __temp_image
