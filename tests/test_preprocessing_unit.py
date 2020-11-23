import unittest
from modules.Preprocessing import Image, PreprocessingManager

class TestPreprocessing(unittest.TestCase):

    def setUp(self):
        from modules.Data import ImageDAO

        features, _ = ImageDAO.get_images(1)
        self.image = Image(features, 50)
        self.preprocessor = PreprocessingManager()

    def test_preprocessing_decorator(self):
        message = self.preprocessor.apply(self.image, ro=90)
        self.assertEqual(message, "Image 50, rotated 90 degrees")

        message = self.preprocessor.apply(self.image, rz=[28,28])
        self.assertEqual(message, "Image 50, rotated 90 degrees, no resized")

        message = self.preprocessor.apply(self.image, rz=[32,32])
        self.assertEqual(message, "Image 50, rotated 90 degrees, no resized, resized to 32x32x1")

        message = self.preprocessor.apply(self.image, sm=[])
        self.assertEqual(message, "Image 50, rotated 90 degrees, no resized, resized to 32x32x1, smoothed")