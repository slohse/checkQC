import unittest

import os

from checkQC.app import App


class TestApp(unittest.TestCase):

    RUNFOLDER = os.path.join(os.path.dirname(__file__), "resources", "170726_D00118_0303_BCB1TVANXX/")

    def test_run(self):
        app = App(runfolder=self.RUNFOLDER)
        app.run()

    def test_run_json_mode(self):
        app = App(runfolder=self.RUNFOLDER, json_mode=True)
        app.run()


if __name__ == '__main__':
    unittest.main()
