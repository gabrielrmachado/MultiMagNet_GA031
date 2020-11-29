from modules.Deployment import ExecutionManager
from modules.Preprocessing import Image
from modules.Data import ImageDAO
import unittest

class TestDeployment(unittest.TestCase):

    def test_deployment_integration(self):
        runner = ExecutionManager()
        image, _ = ImageDAO.get_images(1)
        ans = runner.run(Image(image, 25), ro=90, rz=[28,28], sm=[])

        self.assertEqual(ans, True)