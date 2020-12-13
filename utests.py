import unittest
from datetime import datetime
from hashlib import sha256
from time import sleep

from main import Ruswizard


class RuswizardTest(unittest.TestCase):
    def setUp(self):
        self.test = Ruswizard()

    def setDown(self):
        del self.test

    def test_comment_0(self):
        self.assertEqual(self.test.comment(), True)

    def test_comment_1(self):
        self.assertEqual(self.test.comment(url='vk.com'), True)

    def test_comment_2(self):
        self.assertEqual(self.test.comment(
            msg="u r geek 2! " + sha256((str(datetime.utcnow()) + 'geek').encode('utf-8')).hexdigest()), False)

    def test_log_in_out(self):
        self.assertEqual(self.test.log_in("ya", "12345"), True)
        self.assertEqual(self.test.log_out(), True)


class RuswizardTestLogin(unittest.TestCase):
    def setUp(self):
        self.test = Ruswizard()
        self.assertEqual(self.test.log_in("ya", "12345"), True)

    def setDown(self):
        self.assertEqual(self.test.log_out(), True)
        del self.test

    def test_comment_0(self):
        self.assertEqual(self.test.comment(), True)

    def test_comment_1(self):
        posts = self.test.first_page()
        self.assertGreater(len(posts), 0)
        sol = sha256((str(datetime.utcnow()) + 'sol').encode('utf-8')).hexdigest()
        self.assertEqual(self.test.comment(msg=('The five boxing wizards jump quickly. ' + sol), title=posts[0]),
                         True)
        sleep(10)
        self.assertEqual(self.test.comment(msg=('The five boxing wizards jump quickly. ' + sol), title=posts[0]),
                         False)
        sleep(10)

    def test_comment_2(self):
        my_posts = self.test.my_posts()
        posts = self.test.first_page()
        self.assertGreater(len(posts), 0)
        self.assertEqual(self.test.comment(title=posts[0], msg="u r geek 2! " + sha256(
            (str(datetime.utcnow()) + 'geek').encode('utf-8')).hexdigest()), posts[0] == my_posts[0])

    def test_all_posts(self):
        all_posts = self.test.all_posts_page()
        self.assertGreater(len(all_posts), 0)

    def test_all_comments(self):
        all_comments = self.test.all_comments_page()
        self.assertGreater(len(all_comments), 0)


if __name__ == '__main__':
    unittest.main()
