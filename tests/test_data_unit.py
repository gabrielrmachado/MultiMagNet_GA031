import unittest
import numpy as np
from modules.Data import ImageDAO, UserDAO, Dataset, AttackAlgorithm

class TestData(unittest.TestCase):
    
    def test_number_images_and_labels_vleg_set(self):
        number_legitimate_images = 153
        images_vleg, labels_vleg = ImageDAO.get_images(number_legitimate_images)
        self.assertEqual(len(images_vleg), number_legitimate_images)
        self.assertEqual(len(labels_vleg), number_legitimate_images)

    def test_number_images_and_labels_v_set(self):
        number_legitimate_images = 153
        images_v, labels_v = ImageDAO.get_Vdataset(number_legitimate_images, AttackAlgorithm.FGSM, eps=0.3)
        self.assertEqual(len(images_v), number_legitimate_images*2)
        self.assertEqual(len(labels_v), number_legitimate_images*2)

    def test_v_set_is_balanced(self):
        number_legitimate_images = 153
        _, labels_v = ImageDAO.get_Vdataset(number_legitimate_images, AttackAlgorithm.FGSM, eps=0.3)
        unique, counts = np.unique(labels_v, return_counts=True)
        c = dict(zip(unique, counts))
        self.assertEqual(c[0], c[1])

    def test_load_users_from_file(self):
        userDao = UserDAO()
        self.assertEqual(userDao.get_users_size()-1, 2)
