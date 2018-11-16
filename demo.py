# -*-coding:utf-8-*-
import requests
import bs4
from io import BytesIO
from PIL import Image
import pytesser3
import re


class Douban:
    def __init__(self, username, password):
        self.root = "https://www.douban.com/"
        self.session = self.login(username, password)

    def login(self, username, password):
        # 获取图片response
        res = requests.get(url=self.root)
        soup = bs4.BeautifulSoup(res.content, "html5lib")
        img_url = soup.find(id="captcha_image")["src"]
        img_res = requests.get(img_url)

        # 写入内存文件
        f = BytesIO()
        f.write(img_res.content)
        img = Image.open(f).convert('L')
        # img.show()

        # 将用户名密码和验证码封装到data，并post，获得登录完事的session
        data = {
            "source": "index_nav",
            "form_email": username,
            "form_password": password,
            "captcha-solution": self.captcha(img),
            "captcha-id": re.findall("id=(.*)&", img_url)[0]
        }
        sess = requests.Session()
        sess.post(url=self.root, data=data)
        # TODO 是否需要添加头部信息
        # TODO 是否需要保存Cookies
        # TODO 登录失败处理

        return sess

    def send_code(self, num, area_code="+86"):
        # 向手机发送验证码
        data = {
            'area_code': area_code,
            'number': str(num),
            'step': 'input_number',
            'ck': "abcd"  # TODO Figure out this. 第一次是EEka
        }
        res = self.session.post(self.root + "accounts/j/phone/bind", data=data)
        # TODO 判断是否发送成功

    def bind(self, code):
        # 手机收到验证码之后填充验证码，绑定
        ck = "abcd"  # TODO Figure out this. 同上，第一次是EEka
        data = {
            'ck': ck,
            'code': code,
            'step': 'input_code'
        }
        res = self.session.post(self.root + "accounts/phone/bind?ck=" + ck)
        # TODO 判断是否绑定成功

    def captcha(self, img):
        # 输入Image.Image格式
        # TODO FileNotFound
        s = pytesser3.image_to_string(img)
        return s

if __name__ == '__main__':
    Douban("544301590@qq.com", "ZyfAiDota2")