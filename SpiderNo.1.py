import requests
import re
from selenium import webdriver
home_url = 'https://www.douban.com/'    #豆瓣首页
login_url = 'https://accounts.douban.com/login'     #登录页
head = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'}
username = input('请输入账号:')
password = input('请输入你的密码:')
data = {
    'source': 'index_nav',
    'redir': 'https://www.douban.com/',
    'form_email': username,
    'form_password': password,
    'login': '登录'
}
s = requests.session()
'''
判断登陆状态...
'''
def is_login(html):
    accout = re.search('"_blank".*?class="bn-more">.*?<span>(.*?)</span>',html,re.S)
    print('现在登陆的账号是:'+accout.group(1))

'''
判断是否存在验证码，有则捕获验证码地址留后用。
'''
def is_captcha():
    global code
    global captcha_id
    response = s.get(home_url)
    captcha = re.findall('id="captcha_image".*?src="(.*?)"',response.text,re.S)[0]
    captcha_id = captcha.split('=')[1].split('&')[0]
    if captcha:
        print('存在验证码,请等待浏览器加载验证码...')
        driver = webdriver.Chrome()
        driver.get(captcha)
        code = input('请输入验证码:')
    else:
        code = None
        captcha_id = None

'''
登陆发起...
'''
def login():
    data['captcha-solution'] = code
    data['captcha-id'] = captcha_id
    response = s.post(login_url,headers = head,data = data)
    return response.text


if __name__ == '__main__':
    is_captcha()
    page_source = login()
    is_login(page_source)