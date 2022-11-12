import unittest
from unittest.mock import MagicMock

from replurker import parse_args
from replurker import is_replurkable
from replurker import get_plurk_ids


class TestBasicFunctions(unittest.TestCase):
    def setUp(self):
        self.plurk = {
            "plurk_id": 42,
            "content": "test #replurk_bot",
            "content_raw": "test #replurk_bot",
            "replurked": False,
            "replurkable": True,
            "anonymous": False,
        }

        self.anonymous_plurk = {
            "plurk_id": 43,
            "content": "test #replurk_bot",
            "content_raw": "test #replurk_bot",
            "replurked": False,
            "replurkable": True,
            "anonymous": True,
        }

        self.plurk_cli = MagicMock()
        self.plurk_cli.callAPI

    def test_parse_args(self):
        keyword = "#replurk_bot"
        key_file = "dummy.keys"

        args1 = f"{key_file} {keyword} -a".split()
        r1 = parse_args(args1)

        self.assertEqual(r1.keyword, keyword)
        self.assertEqual(r1.auth_key, key_file)
        self.assertTrue(r1.allow_anonymous)

        args2 = f"{key_file} {keyword}".split()
        r2 = parse_args(args2)
        self.assertFalse(r2.allow_anonymous)

        args3 = f"-a {key_file}".split()
        self.assertRaises(SystemExit, parse_args, args3)

    def test_is_replurkable(self):
        p1 = dict(self.anonymous_plurk)
        self.assertFalse(is_replurkable(p1, "#replurk_bot", False))
        self.assertTrue(is_replurkable(p1, "#replurk_bot", True))

        p2 = dict(self.anonymous_plurk)
        p2["replurked"] = True
        self.assertFalse(is_replurkable(p2, "#replurk_bot", True))

        p3 = dict(self.anonymous_plurk)
        p3["replurkable"] = False
        self.assertFalse(is_replurkable(p3, "#replurk_bot", True))

        p4 = dict(self.plurk)
        self.assertTrue(is_replurkable(p4, "#replurk_bot", True))
        self.assertTrue(is_replurkable(p4, "#replurk_bot", False))

    def test_get_plurk_ids(self):
        plurks = {"plurks": [dict(self.plurk), dict(self.anonymous_plurk)]}
        self.plurk_cli.callAPI = MagicMock(return_value=plurks)

        ids1 = get_plurk_ids(self.plurk_cli, "#replurk_bot", True)
        self.assertEqual(ids1, [42, 43])

        ids2 = get_plurk_ids(self.plurk_cli, "#replurk_bot", False)
        self.assertEqual(ids2, [42])


if __name__ == "__main__":
    unittest.main()
