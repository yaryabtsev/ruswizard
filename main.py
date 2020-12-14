import random
import re
from datetime import datetime
from hashlib import sha256
from time import sleep

from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


class Ruswizard():
    def __init__(self):
        self.opts = Options()
        self.opts.set_headless()
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

    def set_time(self, mins=1):
        if self.browser.title == 'Добавить запись ‹ Testing example — WordPress':
            self.browser.find_element_by_id('post-title-0').click()
            sleep(1)
            self.browser.find_element_by_xpath(
                '//button[contains(@class, "editor-post-publish-panel__toggle")]').click()
            sleep(1)
            _xpath = '//div[contains(@class, "components-panel__body")]' \
                     '//h2[contains(@class, "components-panel__body-title")]' \
                     '//button[contains(@class, "components-panel__body-toggle")]'
            blocks = self.browser.find_elements_by_xpath(_xpath)
            for block in blocks:
                if 'Опубликована:' in block.text:
                    block.click()
            inpt = self.browser.find_element_by_class_name('components-datetime__time-field-minutes-input')
            curr_t = int(inpt.get_attribute('value'))
            if curr_t + mins > 59:
                return False
            inpt.send_keys(str(curr_t + mins))
            self.browser.find_element_by_xpath(
                '//button[contains(@aria-label, "Закрыть панель")]').click()
            return True
        return False

    def add_title(self):
        if self.browser.title in ['Добавить запись ‹ Testing example — WordPress',
                                  'Редактировать запись ‹ Testing example — WordPress']:
            self.browser.find_element_by_xpath('//button[contains(@aria-label, "Добавить блок")]').click()
            self.browser.find_element_by_xpath('//button[contains(@class, "block-editor-block-types-list__'
                                               'item editor-block-list-item-heading")]').click()
            self.browser.switch_to.active_element.send_keys("New Title")
            return True
        return False

    def add_quote(self):
        if self.browser.title in ['Добавить запись ‹ Testing example — WordPress',
                                  'Редактировать запись ‹ Testing example — WordPress']:
            self.browser.find_element_by_xpath('//button[contains(@aria-label, "Добавить блок")]').click()
            self.browser.find_element_by_xpath('//button[contains(@class, "block-editor-block-types-list__'
                                               'item editor-block-list-item-quote")]').click()
            elm = self.browser.switch_to.active_element
            elm.send_keys("New Quote")
            elm.send_keys(Keys.TAB)
            self.browser.switch_to.active_element.send_keys("NoOne")
            return True
        return False

    def add_block(self):
        if self.browser.title in ['Добавить запись ‹ Testing example — WordPress',
                                  'Редактировать запись ‹ Testing example — WordPress']:
            self.browser.find_element_by_xpath('//button[contains(@aria-label, "Добавить блок")]').click()
            self.browser.find_element_by_xpath('//button[contains(@class, "block-editor-block-types-list__'
                                               'item editor-block-list-item-paragraph")]').click()
            self.browser.switch_to.active_element.send_keys("New Paragraph")
            return True
        return False

    def add_img(self):
        if self.browser.title in ['Добавить запись ‹ Testing example — WordPress',
                                  'Редактировать запись ‹ Testing example — WordPress']:
            self.browser.find_element_by_xpath('//button[contains(@aria-label, "Добавить блок")]').click()
            self.browser.find_element_by_xpath('//button[contains(@class, "block-editor-block-types-list__'
                                               'item editor-block-list-item-image")]').click()
            self.browser.find_element_by_xpath('//div[contains(@class, "block-editor-media-placeholder__'
                                               'url-input-container")]//button[contains(@class,'
                                               ' "block-editor-media-placeholder__button")]').click()
            sleep(1)
            inpt = self.browser.find_element_by_xpath(
                '//input[contains(@placeholder, "Вставить или ввести URL-адрес")]')
            inpt.click()
            imgs = ['a8fca2352c62aaf357344c82473cf3af', 'c8c858b711f2a673a40bdb382f37f4ce',
                    '0f9d19e62ed05bbc944e4db3488e3830', '9a7ebe12a5ad8c0135932540a6db56d5',
                    '435ca34b2e72d906a799dd31499f1f7c', 'e6c122d6355d39a1ff927f645c79bd44',
                    '42f32697d62d7ecdb00511cca15f49b7', '8e84667a056ac2e33f00c199a1816d33',
                    '1153b4f0731f68fa9947f14002b85b98', '304526e1793bee54455323ffca624a83',
                    '809c86905f2d07b2445dc3ea03e01c2b', '94277904ae3660128a01705064daad4b',
                    'd6f02f1d62a9b368949f450b8707e472', '12fd44bb40f595df5adaff0054af6c4c',
                    'ecdb753cc9cc5b3f9ac4d4f51ef5ed96', '4889f08b251652e456c99fef259a1061',
                    'c4c952dbdc75df0a3ebd5f366c209ba7', '6da0d6192f744501d0c5613561472dba',
                    '5f3b29ec02e432d8383cb878fa1ef025', '000b3efa4c995c65e70f25484a0944fc',
                    '9c69efe1c78f8a5e91bba9edec08bcd1', '838acb5d2846e1334de4f9214984e614',
                    'ad9bc70754019d7eaaf9acf82558f9be', '3ff755a5324b498c8aadb8e3c7ad158e',
                    '068e51775f3a5004883047e71b972b8d', 'bab547ac31f6b5f7ea69f8bd0372241d',
                    '657567c9502198f64045300e01eb7fbe', '7fe79b7a2ab9fba1183b7b163aeeb5e8',
                    '58d87526bd4f43e9d5e8ceca8907ff91', '6eb13743271d0d3bc79757e4ec595a01',
                    '0cd72ed91a20f9a0d258f02be9e5813d', 'a9a842e685b91b8aeb5f71ca25715ddb',
                    '2f6b5c193b58da11ddbeb5192f0beeef', '381f86f9849c46c5dbfcb4bd17e8cffe',
                    '3fd374e626c24edb3e2c89417ad18ea4', '53bc1d16a0185c92adad0bd77ec8b3b7',
                    '1b17329658466254a51499c3cc1b5fb8', '0f9d19e62ed05bbc944e4db3488e3830',
                    '0f9d19e62ed05bbc944e4db3488e3830', '95d2050d26eaa1b59e52f27732a5a441',
                    'd0afd4bd96bf433a8420f87a9c5f4ea6', 'b805f3b8f56308e33aba7a2b2c2e9cae',
                    '9287fd286636ebe5ccb2d4c9910f331c', 'e1635649a54cef4423cd05a8dfcfbeda',
                    'aa57209322b579a50bb4cf9e7d4e1c92']
            src = "https://e-cdns-images.dzcdn.net/images/cover/" + random.choice(imgs) + "/264x264-000000-80-0-0.jpg"
            inpt.send_keys(src)
            inpt.submit()
            sleep(2)
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

    def append_body(self, text="*"):
        if self.browser.title in ['Добавить запись ‹ Testing example — WordPress',
                                  'Редактировать запись ‹ Testing example — WordPress']:
            self.browser.find_elements_by_xpath(
                '//div[contains(@class, "block-editor-block-list")]//p[contains(@id, "block-")]')[0].send_keys(text)
            return True
        return False

    def edit_body(self, text=""):
        if self.browser.title in ['Добавить запись ‹ Testing example — WordPress',
                                  'Редактировать запись ‹ Testing example — WordPress']:
            if not text:
                text = '***' + sha256((str(datetime.utcnow()) + 'geek').encode('utf-8')).hexdigest()
            self.browser.find_elements_by_xpath(
                '//div[contains(@class, "block-editor-block-list")]//p[contains(@id, "block-")]')[0].clear()
            self.append_body(text)
            return True
        return False

    def submit(self):
        if self.browser.title == 'Добавить запись ‹ Testing example — WordPress':
            self.browser.find_element_by_xpath(
                '//button[contains(@class, "editor-post-publish-panel__toggle")]').click()
            sleep(1)
            self.browser.find_element_by_xpath(
                '//button[contains(@class, "components-button'
                ' editor-post-publish-button editor-post-publish-button__button is-primary")]').click()
            sleep(2)
            urls = re.findall(r'https://ruswizard.site/test/\d+/\d+/\d+/[^/]+', self.browser.page_source)
            if not urls:
                return False
            return urls[0]
        elif self.browser.title == 'Редактировать запись ‹ Testing example — WordPress':
            self.browser.find_element_by_id('post-title-0').send_keys('*')
            self.browser.find_element_by_xpath(
                '//button[contains(@class, "editor-post-publish-button__button")]').click()
            return True
        return False

    def get_url(self, url="https://ruswizard.site/test/"):
        self.browser.get(url)
        return self.browser.title

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
    print(test.add_title())
    print(test.submit())
    print(test.log_out())
    del test
