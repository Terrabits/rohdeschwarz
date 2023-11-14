
from .fixtures.osp                      import driver, path
from ddt                                import ddt, data
from rohdeschwarz.instruments.ospswitch import OspSwitch
from rohdeschwarz.test.mock.bus         import OspBus
from unittest                           import main, TestCase


@ddt
class TestOspSwitch(TestCase):

    # init for tests

    def setUp(self):
        self.osp     = OspSwitch(driver)
        self.osp.bus = OspBus()


    # tests


    @data(
        {'name': 'k99'}
    )
    def test_unknown_switch(self, data):
        def get_switch():
            getattr(self.osp, data['name'])
        self.assertRaises(AttributeError, get_switch)


    def test_set_switches(self):
        self.osp.set_switches(path)
        for key in path:
            value = path[key]
            if value == 'nc':
                value = 0
            elif value == 'no':
                value = 1
            self.assertEqual(getattr(self.osp, key.lower()), value)


# main

if __name__ == '__main__':
    main()
