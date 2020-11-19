import unittest
from modules.Data import ImageDAO, UserDAO, Dataset, AttackAlgorithm

class TestData(unittest.TestCase):
    
    def setUp(self):
        self._number_legitimate_images = 200

    def test_number_legitimate_images_and_labes_vleg_set(self):
        images, labels = ImageDAO.get_images(self._number_legitimate_images)
        self.assertEqual(len(images), self._number_legitimate_images)
        self.assertEqual(len(labels), self._number_legitimate_images)

    def test_number_images_and_labels_v_set(self):
        vdata, vlabels = ImageDAO.get_Vdataset(self._number_legitimate_images, AttackAlgorithm.FGSM, eps=0.3)
        self.assertEqual(len(vdata), self._number_legitimate_images*2)
        self.assertEqual(len(vlabels), self._number_legitimate_images*2)