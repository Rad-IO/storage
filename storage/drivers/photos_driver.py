import os
from datetime import datetime
import random
import base64
import py

import tensorflow as tf

import storage.utils as utils

_DEFAULT_IMG_FORMAT = 'jpeg'
_DIGITS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


class PhotosStorageDriver:
    """Class handling photos reading/ saving.

    Parameters
    ----------
    location: str
        Path to the root directory where to save the data.

    """

    _IMAGE_READERS = {
        True: tf.gfile.GFile,
        False: open,
    }

    def __init__(self, location):
        self._location = os.path.abspath(location)

    def _get_image_path(self, format, id):
        """Construct the path for an image.

        Parameters
        ----------
        format: str
            Format of the image we're looking for.
        id: str
            Id of the image we're looking for.

        Returns
        -------
        str
            With the full path for that image.

        """
        return os.path.join(self._location, format, '{}.{}'.format(id, format))

    def _generate_new_image_id(self):
        """Generate an id for a new image.

        Returns
        ----------
        str
            With the new image id.
        """
        time = str(
            datetime.now()
        ).replace(' ', '').replace(':', '').replace('-', '').replace('.', '')
        random_sequence = ''.join(
            [str(random.choice(_DIGITS)) for _ in range(5)]
        )

        return '{}_{}'.format(time, random_sequence)

    def get_image_by_id(self, img_id, use_tf=False, format=_DEFAULT_IMG_FORMAT):
        """Get image data by it's id.

        Parameters
        ----------
        img_id: str
            With the id of the image we're looking for.
        use_tf: bool
            Whether to use tensorflow or not when reading data. If using
            tensorflow, the file will be opened using `tf.gfile.GFile`, instead
            of `open`. Default `FALSE`
        format: str
            The format of the image.

        Returns
        -------
        bytes
            With the data that was read.

        """
        image_path = self._get_image_path(format, img_id)
        with self._IMAGE_READERS[use_tf](image_path, 'rb') as stream:
            return stream.read()

    def save_new_image(self, b64data):
        """Save a new image to disc.

        Parameters
        ----------
        b64data: str
            Base64-encoded image.

        Returns
        -------
        str
            With the id of the image.

        """
        new_id = self._generate_new_image_id()
        path = self._get_image_path(_DEFAULT_IMG_FORMAT, new_id)
        utils.create_directories_for_path(path)

        raw_data = base64.b64decode(b64data)

        with open(path, 'wb') as stream:
            stream.write(raw_data)

        return new_id
