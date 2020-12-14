import random
from datetime import datetime
from time import sleep

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


class Ruswizard():
    def __init__(self):
        self.opts = Options()
        # self.opts.set_headless()
        self.browser = Firefox(options=self.opts)
        self.authorized = False

    def first_page(self):
        self.get_url()
        posts = self.browser.find_elements_by_xpath(
            '//article[contains(@class, "post")]//h2[contains(@class, "entry-title")]//a')
        return [post.text for post in posts]

    def my_posts(self):
        if not self.authorized:
            return False
        self.get_url('https://ruswizard.site/test/wp-admin/edit.php')
        sleep(1)
        posts = self.browser.find_elements_by_xpath('//table[contains(@class, "posts")]//tbody[contains(@id, '
                                                    '"the-list")]//strong//a[contains(@class, "row-title")]')
        return [post.text for post in posts]

    def all_posts_page(self):
        if not self.authorized:
            return False
        self.get_url('https://ruswizard.site/test/wp-admin/')
        sleep(1)
        self.browser.find_element_by_xpath('//a[contains(@href, "edit.php?post_type=post")]').click()
        sleep(1)
        self.browser.find_element_by_xpath('//a[contains(@href, "edit.php?post_type=post&all_posts=1")]').click()
        sleep(1)
        posts = self.browser.find_elements_by_xpath('//table[contains(@class, "posts")]//tbody[contains(@id, '
                                                    '"the-list")]//tr[contains(@id, "post-")]')
        return [post.text for post in posts]

    def add_tokens(self, tokens=None):
        if not tokens:
            return False
        if self.browser.title == 'Добавить запись ‹ Testing example — WordPress':
            self.browser.find_element_by_id('post-title-0').click()
            sleep(1)
            if not self.browser.find_elements_by_xpath('//button[contains(@class, "edit-post-post-visibility")]'):
                self.browser.find_element_by_xpath('//div[contains(@class, "interface-pinned-items")]'
                                                   '//button[contains(@class, "has-icon")]').click()
            xpath = '//input[contains(@id, "components-form-token-input-")]'
            inpt = self.browser.find_elements_by_xpath(xpath)
            _xpath = '//div[contains(@class, "components-panel__body")]' \
                     '//h2[contains(@class, "components-panel__body-title")]' \
                     '//button[contains(@class, "components-panel__body-toggle")]'
            if not inpt:
                self.browser.find_elements_by_xpath(_xpath)[0].click()
                self.browser.find_elements_by_xpath(_xpath)[3].click()
                inpt = self.browser.find_elements_by_xpath(xpath)
            for token in tokens:
                inpt[0].send_keys(str(token) + ',')
            _xpath = '//div[contains(@class, "components-panel__body")]' \
                     '//h2[contains(@class, "components-panel__body-title")]' \
                     '//button[contains(@class, "components-panel__body-toggle")]'
            self.browser.find_elements_by_xpath(_xpath)[3].click()
            self.browser.find_elements_by_xpath(_xpath)[0].click()
            return True
        return False

    def visible(self, flag=True):
        if self.browser.title == 'Добавить запись ‹ Testing example — WordPress':
            self.browser.find_element_by_id('post-title-0').click()
            sleep(1)
            xpath = '//button[contains(@class, "edit-post-post-visibility")]'
            btn = self.browser.find_elements_by_xpath(xpath)
            if not btn:
                self.browser.find_element_by_xpath('//div[contains(@class, "interface-pinned-items")]'
                                                   '//button[contains(@class, "has-icon")]').click()
                btn = self.browser.find_elements_by_xpath(xpath)
            btn[0].click()
            if not flag:
                self.browser.find_element_by_xpath('//input[contains(@id, "editor-post-private-")]').click()
                sleep(1)
                try:
                    sleep(1)
                    self.browser.switch_to.alert.accept()
                    sleep(1)
                except Exception:
                    return False
                xpath = '//a[contains(@class, "components-external-link")]'
                url = self.browser.find_elements_by_xpath(xpath)
                if not url:
                    _xpath = '//div[contains(@class, "components-panel__body")]' \
                             '//h2[contains(@class, "components-panel__body-title")]' \
                             '//button[contains(@class, "components-panel__body-toggle")]'
                    self.browser.find_elements_by_xpath(_xpath)[0].click()
                    self.browser.find_elements_by_xpath(_xpath)[1].click()
                    url = self.browser.find_elements_by_xpath(xpath)
                self.get_url(url[1].text.split('\n')[0])
                return self.browser.current_url
            else:
                self.browser.find_element_by_xpath('//input[contains(@id, "editor-post-public-")]').click()
            self.browser.find_element_by_xpath('//div[contains(@class, "interface-pinned-items")]'
                                               '//button[contains(@class, "has-icon")]').click()
            return True
        return False

    def all_comments_page(self):
        if not self.authorized:
            return False
        self.get_url('https://ruswizard.site/test/wp-admin/')
        sleep(1)
        self.browser.find_element_by_xpath('//a[contains(@href, "edit-comments.php")]').click()
        sleep(1)
        comments = self.browser.find_elements_by_xpath(
            '//table[contains(@class, "comments")]//tbody[contains(@id, "the-comment-list")]//'
            'tr[contains(@id, "comment-")]')
        return [comment.text for comment in comments]

    @staticmethod
    def choose_post(title="", posts=None):
        if posts is None:
            posts = []
        if not posts:
            return False
        if not title:
            return posts[0]
        else:
            for post in posts:
                if post.text == title:
                    return post
        return False

    def comment(self, name="", email="", url="", msg="", title=""):
        self.get_url()
        posts = self.browser.find_elements_by_xpath('//article[contains(@class, "post")]//'
                                                    'h2[contains(@class, "entry-title")]//a')
        post = self.choose_post(title, posts)
        if not post:
            return False
        post.click()
        sleep(1)
        if not msg:
            msg = 'awesome comment ' + str(datetime.utcnow().microsecond)
        self.browser.find_element_by_id('comment').send_keys(msg)
        if not self.authorized:
            if not name:
                name = random.choice(
                    ["OLIVER", "JACK", "HARRY", "JACOB", "CHARLIE", "THOMAS", "GEORGE", "OSCAR", "JAMES", "WILLIAM",
                     "NOAH", "ALFIE", "JOSHUA", "MUHAMMAD", "HENRY", "LEO", "ARCHIE", "ETHAN", "JOSEPH", "FREDDIE",
                     "SAMUEL", "ALEXANDER", "LOGAN", "DANIEL", "ISAAC", "MAX", "MOHAMMED", "BENJAMIN", "MASON", "LUCAS",
                     "EDWARD", "HARRISON", "JAKE", "DYLAN", "RILEY", "FINLEY", "THEO", "SEBASTIAN", "ADAM", "ZACHARY",
                     "ARTHUR", "TOBY", "JAYDEN", "LUKE", "HARLEY", "LEWIS", "TYLER", "HARVEY", "MATTHEW", "DAVID"])
            if not email:
                email = name + "@mail.ru"
            self.browser.find_element_by_id('author').send_keys(name)
            self.browser.find_element_by_id('email').send_keys(email)
            if url:
                self.browser.find_element_by_id('url').send_keys(url)
        self.browser.find_element_by_id('submit').click()
        sleep(1)
        comments = self.browser.find_elements_by_class_name("comment-content")
        if not comments:
            return False
        comments = [comment.text for comment in comments]
        if msg in comments:
            return True
        if (msg + '\nВаш комментарий ожидает одобрения.') in comments:
            return True
        return False

    def log_in(self, name, passwd):
        if self.authorized:
            return False
        self.get_url()
        self.browser.find_element_by_link_text("Войти").click()
        sleep(1)
        self.browser.find_element_by_id('user_login').send_keys(name)
        self.browser.find_element_by_id('user_pass').send_keys(passwd)
        self.browser.find_element_by_id('wp-submit').click()
        sleep(1)
        if self.browser.title == 'Консоль ‹ Testing example — WordPress':
            self.authorized = True
            return True
        return False

    def append_title(self, text="*"):
        if self.browser.title in ['Добавить запись ‹ Testing example — WordPress',
                                  'Редактировать запись ‹ Testing example — WordPress']:
            self.browser.find_element_by_id('post-title-0').send_keys(text)
            return True
        return False

    def edit_title(self, text=""):
        if self.browser.title in ['Добавить запись ‹ Testing example — WordPress',
                                  'Редактировать запись ‹ Testing example — WordPress']:
            if not text:
                text = "New Post _" + str(datetime.utcnow().microsecond) + '*'
            self.browser.find_element_by_id('post-title-0').clear()
            self.append_title(text)
            return True
        return False

    def submit(self):
        if self.browser.title == 'Добавить запись ‹ Testing example — WordPress':
            title = self.browser.find_element_by_id('post-title-0').text
            self.browser.find_element_by_xpath(
                '//button[contains(@class, "editor-post-publish-panel__toggle")]').click()
            sleep(2)
            self.browser.find_element_by_xpath(
                '//button[contains(@class, "components-button'
                ' editor-post-publish-button editor-post-publish-button__button is-primary")]').click()
            sleep(5)
            self.browser.find_element_by_link_text(title).click()
            return self.browser.current_url
        elif self.browser.title == 'Редактировать запись ‹ Testing example — WordPress':
            self.browser.find_element_by_id('post-title-0').send_keys('*')
            self.browser.find_element_by_xpath(
                '//button[contains(@class, "editor-post-publish-button__button")]').click()
            return True
        return False

    def get_url(self, url="https://ruswizard.site/test/"):
        self.browser.get(url)
        return True

    def log_out(self):
        if not self.authorized:
            return False
        self.get_url()
        self.browser.find_element_by_link_text("Выйти").click()
        sleep(1)
        if self.browser.title == 'Войти ‹ Testing example — WordPress':
            self.authorized = False
            return True
        return False

    def new_post(self, title="", text=""):
        if not self.authorized:
            return False
        self.get_url('https://ruswizard.site/test/wp-admin/edit.php')
        self.browser.find_element_by_link_text("Добавить новую").click()
        sleep(1)
        if not title:
            title = "New Post _" + str(datetime.utcnow().microsecond)
        if not text:
            text = "They're creepy and they're kooky,\nMysterious and spooky,\nThey're all together ooky,\n" \
                   "The Addams Family."
        self.browser.find_element_by_id('post-title-0').send_keys(title)
        body = self.browser.find_element_by_xpath(
            '//div[contains(@class, "block-list-appender")]//div[contains(@class, "wp-block")]'
            '//textarea[contains(@class, "block-editor-")]')
        body.click()
        body = self.browser.find_elements_by_xpath(
            '//div[contains(@class, "block-editor-block-list")]//p[contains(@id, "block-")]')[0]
        body.send_keys(text)
        return True

    def edit_post(self, title=""):
        if not self.authorized:
            return False
        self.get_url('https://ruswizard.site/test/wp-admin/edit.php')
        sleep(1)
        posts = self.browser.find_elements_by_xpath('//table[contains(@class, "posts")]//tbody[contains(@id, '
                                                    '"the-list")]//strong//a[contains(@class, "row-title")]')
        post = self.choose_post(title, posts)
        if not post:
            return False
        post.click()
        sleep(1)
        return True

    def __del__(self):
        self.browser.quit()


if __name__ == "__main__":
    test = Ruswizard()
    print(test.log_in("ya", "12345"))
    print(test.new_post())
    print(test.add_tokens(['t1', 't2', 't3']))
    print(test.submit())
    print(test.log_out())
    del test
