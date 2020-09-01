import argparse
import sys
import unittest
import os
from util.Api import Api
from time import sleep

from util.Docker import Docker
from util.Dredd import Dredd


class PaymentContainerTest(unittest.TestCase):
    TAG = "latest"
    PORT = "8080"

    container_name = Docker().random_container_name('payment')

    def __init__(self, methodName='runTest'):
        super(PaymentContainerTest, self).__init__(methodName)
        self.ip = ""
        
    def setUp(self):
        command = ['docker', 'run',
                   '-d',
                   '--name', PaymentContainerTest.container_name,
                   '-h', 'payment',
                   'weaveworksdemos/payment-dev:' + self.TAG,
                   '/app', '-port=' + PaymentContainerTest.PORT]
        Docker().execute(command)
        self.ip = Docker().get_container_ip(PaymentContainerTest.container_name)

    def tearDown(self):
        Docker().kill_and_remove(PaymentContainerTest.container_name)

    def test_api_validated(self):
        limit = 30
        url = f'http://{self.ip}:{PaymentContainerTest.PORT}/'
        
        while Api().noResponse(url + 'payments/'):
            if limit == 0:
                self.fail("Couldn't get the API running")
            limit = limit - 1
            sleep(1)
        
        out = Dredd().test_against_endpoint("payment",
                                            url,
                                            links=[self.container_name],
                                            dump_streams=True)
        
        self.assertGreater(out.find("0 failing"), -1)
        self.assertGreater(out.find("0 errors"), -1)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    default_tag = "latest"
    parser.add_argument('--tag', default=default_tag, help='The tag of the image to use. (default: latest)')
    parser.add_argument('unittest_args', nargs='*')
    args = parser.parse_args()
    PaymentContainerTest.TAG = args.tag

    if PaymentContainerTest.TAG == "":
        PaymentContainerTest.TAG = default_tag

    # Now set the sys.argv to the unittest_args (leaving sys.argv[0] alone)
    sys.argv[1:] = args.unittest_args
    unittest.main()
