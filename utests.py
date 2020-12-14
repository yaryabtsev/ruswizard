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

    def test_post_0(self):
        self.assertEqual(self.test.new_post(), True)
        self.assertNotEqual(type(self.test.submit()), type(True))

    def test_post_1(self):
        title = "Test Post 1 _" + str(datetime.utcnow().microsecond)
        self.assertEqual(self.test.new_post(title=title), True)
        url = self.test.submit()
        self.assertNotEqual(type(url), type(True))
        self.assertEqual(self.test.get_url(url), title + ' — Testing example')

    def test_post_2(self):
        title = "Test Post 2 _" + str(datetime.utcnow().microsecond)
        self.assertEqual(self.test.new_post(title=title), True)
        url = self.test.submit()
        self.assertNotEqual(type(url), type(True))
        self.assertEqual(self.test.log_out(), True)
        self.assertEqual(self.test.log_in('d', '1'), True)
        self.assertEqual(self.test.get_url(url), title + ' — Testing example')

    def test_post_3(self):
        title = "Test Post 1" + str(datetime.utcnow().microsecond)
        self.assertEqual(self.test.new_post(title=title), True)
        url = self.test.submit()
        self.assertNotEqual(type(url), type(True))
        url += '/#comments'
        self.assertEqual(self.test.get_url(url), title + ' — Testing example')

    def test_post_4(self):
        self.assertEqual(self.test.edit_post(), True)
        self.assertEqual(self.test.submit(), True)

    def test_post_visible_0(self):
        title = "Test Visible Post 0 _" + str(datetime.utcnow().microsecond)
        self.assertEqual(self.test.new_post(title=title), True)
        url = self.test.visible(False)
        self.assertNotEqual(type(url), type(True))
        self.assertEqual(self.test.log_out(), True)
        self.assertEqual(self.test.log_in('d', '1'), True)
        self.assertEqual(self.test.get_url(url), 'Страница не найдена — Testing example')

    def test_post_visible_1(self):
        title = "Test Post 1 _" + str(datetime.utcnow().microsecond)
        self.assertEqual(self.test.new_post(title=title), True)
        url = self.test.visible(False)
        self.assertNotEqual(type(url), type(True))
        self.assertEqual(self.test.get_url(url), title + ' — Testing example')

    def test_edit_post_0(self):
        self.assertEqual(self.test.new_post(), True)
        self.assertEqual(self.test.edit_title("Test Post 0 _" + str(datetime.utcnow().microsecond)), True)
        self.assertNotEqual(type(self.test.submit()), type(True))

    def test_edit_post_1(self):
        self.assertEqual(self.test.new_post(), True)
        self.assertEqual(self.test.edit_body("Test Post 1 _" + sha256(
            (str(datetime.utcnow()) + 'geek').encode('utf-8')).hexdigest()), True)
        self.assertNotEqual(type(self.test.submit()), type(True))

    def test_tokens_post_0(self):
        self.assertEqual(self.test.new_post(), True)
        self.assertEqual(self.test.add_tokens(['t0', 't1', 't2', 't3']), True)
        self.assertNotEqual(type(self.test.submit()), type(True))

    def test_set_time_post_0(self):
        if datetime.utcnow().minute + 3 < 60:
            self.assertEqual(self.test.new_post(), True)
            self.assertEqual(self.test.set_time(2), True)
            url = self.test.submit()
            self.assertNotEqual(type(url), type(True))
            self.assertEqual(self.test.log_out(), True)
            self.assertEqual(self.test.log_in('d', '1'), True)
            self.assertEqual(self.test.get_url(url), 'Страница не найдена — Testing example')

    def test_add_img_0(self):
        self.assertEqual(self.test.new_post(), True)
        self.assertEqual(self.test.add_img(), True)
        self.assertNotEqual(type(self.test.submit()), type(True))

    def test_add_title_0(self):
        self.assertEqual(self.test.new_post(), True)
        self.assertEqual(self.test.add_title(), True)
        self.assertNotEqual(type(self.test.submit()), type(True))

    def test_add_quote_0(self):
        self.assertEqual(self.test.new_post(), True)
        self.assertEqual(self.test.add_quote(), True)
        self.assertNotEqual(type(self.test.submit()), type(True))

    def test_add_block_0(self):
        self.assertEqual(self.test.new_post(), True)
        self.assertEqual(self.test.add_block(), True)
        self.assertNotEqual(type(self.test.submit()), type(True))


if __name__ == '__main__':
    unittest.main()
