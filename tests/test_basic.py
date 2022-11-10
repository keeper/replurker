import unittest

from replurker import parse_args


class TestBasicFunctions(unittest.TestCase):
    def test_parse_args(self):
        keyword = "#replurk_bot"
        key_file = "dummy.keys"

        args1 = f"-k {keyword} --auth_key {key_file} -a".split()
        r1 = parse_args(args1)

        self.assertEqual(r1.keyword, keyword)
        self.assertEqual(r1.auth_key, key_file)
        self.assertTrue(r1.allow_anonymous)

        args2 = f"-k {keyword} --auth_key {key_file}".split()
        r2 = parse_args(args2)
        self.assertFalse(r2.allow_anonymous)


if __name__ == "__main__":
    unittest.main()
