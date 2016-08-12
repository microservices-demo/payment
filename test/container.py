import argparse
import unittest

import sys
from time import sleep

from util.Api import Api
from util.Docker import Docker
from util.Dredd import Dredd


class CatalogueContainerTest(unittest.TestCase):
    TAG = "latest"
    container_name = Docker().random_container_name('catalogue')
    mysql_container_name = Docker().random_container_name('catalogue-db')

    def __init__(self, methodName='runTest'):
        super(CatalogueContainerTest, self).__init__(methodName)
        self.ip = ""

    def setUp(self):
        db_command = ['docker', 'run', '-d', '-h', 'catalogue-db', '--name', self.mysql_container_name, '-e', 'MYSQL_ALLOW_EMPTY_PASSWORD=true', 'mysql']
        Docker().execute(db_command)
        command = ['docker', 'run',
                   '-d',
                   '--name', CatalogueContainerTest.container_name,
                   '-h', 'catalogue',
                   '--link',
                   self.mysql_container_name,
                   'weaveworksdemos/catalogue:' + self.TAG]
        Docker().execute(command)
        self.ip = Docker().get_container_ip(CatalogueContainerTest.container_name)

    def tearDown(self):
        Docker().kill_and_remove(CatalogueContainerTest.container_name)
        Docker().kill_and_remove(CatalogueContainerTest.mysql_container_name)

    def test_api_validated(self):
        limit = 60
        while Api.noResponse('http://' + self.ip + ':80/catalogue'):
            if limit == 0:
                self.fail("Couldn't get the API running")
            limit = limit - 1
            sleep(1)

        out = Dredd().test_against_endpoint("catalogue/catalogue.json", CatalogueContainerTest.container_name,
                                            "http://catalogue/", self.mysql_container_name)
        self.assertGreater(out.find("0 failing"), -1)
        self.assertGreater(out.find("0 errors"), -1)
        print(out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', default="latest", help='The tag of the image to use. (default: latest)')
    parser.add_argument('unittest_args', nargs='*')
    args = parser.parse_args()
    CatalogueContainerTest.TAG = args.tag
    # Now set the sys.argv to the unittest_args (leaving sys.argv[0] alone)
    sys.argv[1:] = args.unittest_args
    unittest.main()
