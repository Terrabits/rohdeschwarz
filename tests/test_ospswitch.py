from   rohdeschwarz.test.mock.bus         import OspBus
from   rohdeschwarz.instruments.ospswitch import OspSwitch

from   ddt    import ddt, data
from   ruamel import yaml

import unittest

@ddt
class TestOspSwitch(unittest.TestCase):
    def setUp(self):
        switches = {}
        with open('test/fixtures/osp/driver.yaml', 'r') as f:
            switches = yaml.safe_load(f.read())
        self.osp     = OspSwitch(switches)
        self.osp.bus = OspBus()

    @data({'name': 'k99'})
    def test_unknown_switch(self, data):
        def get_switch():
            getattr(self.osp, data['name'])
        self.assertRaises(AttributeError, get_switch)

    def test_set_switches(self):
        path = {}
        with open('test/fixtures/osp/path.yaml', 'r') as f:
            path = yaml.safe_load(f.read())
        self.osp.set_switches(path)
        for key in path:
            value = path[key]
            if value == 'nc':
                value = 0
            elif value == 'no':
                value = 1
            self.assertEqual(getattr(self.osp, key.lower()), value)


if __name__ == '__main__':
    unittest.main()
