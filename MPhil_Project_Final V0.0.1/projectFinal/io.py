# -*- coding: utf-8 -*-
"""
I/O Functions
=============

Custom tools and processes for segmenting circuit diagrams

author: C. R. Kelly
email: CK598@cam.ac.uk

"""

import os

from PIL import Image

from skimage import io, img_as_ubyte
from skimage.color import rgb2gray, rgba2rgb

from .classes import Image
from .config import Config

config = Config()


def importImage(path):
    """ Imports a given image and converts it into two copies, one as grayscale, one as a binarized skeletonized copy.

    :param path: str: File path of the image.
    :return image: ndarray: Grayscale conversion of imported image.
    :return binaryImage: ndarray: Binarized Skeletonized copy of imported image.
    """
    image = io.imread(path)
    if len(image.shape) == 2:
        image = Image(image, path)
        return image
    else:

        dim3 = image.shape[2]
        if dim3 == 4:
            image = rgba2rgb(image)
            image = rgb2gray(image)

            image = Image(image, path)
            return image
        elif dim3 == 3:
            image = rgb2gray(image)

            image = Image(image, path)
            return image
        else:
            image = Image(image, path)
            return image


def exportComponent(originalImage, components, EXTENSION=config.extension):
    """

    :param EXTENSION: String: File output extension
    :param originalImage: NDARRAY: original input image
    :param components: list of identified components
    :return: nil
    """
    dirPath = os.path.join(config.exportPath, originalImage.name, 'Components')
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

    for component in components:
        top, bottom, left, right = component.getRegion(originalImage)
        image = img_as_ubyte(originalImage.image[top:bottom, left:right])
        # filePath = os.path.splitext(originalImage.path)[0] + "/Components/" + str(component.id) + EXTENSION
        filePath = dirPath + '\\' + str(component.id) + EXTENSION
        component.path = filePath
        io.imsave(filePath, image, plugin='pil', dpi=config.exportDPI)



