import os
import unittest
from util.Docker import Docker

class GoServices(unittest.TestCase):
    def test_go(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        code_dir = script_dir + "/.."
        goPath = os.environ['GOPATH']
        command = ['docker', 'run', '--rm', '-v', goPath + ':/go/bin/', '-v', code_dir + ':/usr/src/', '-w',
                   '/usr/src/', '-e', 'GOPATH=/go/bin', 'golang:1.6', 'go', 'test', '-v']
        print(Docker().execute(command))


if __name__ == '__main__':
    unittest.main()
