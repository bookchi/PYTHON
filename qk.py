import requests
import time
# headers = {
#     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Connection': 'keep-alive',
#     'Cookie': 'sessionid=dslwydcdekumlob3bnb7xvzuprucaf8s; csrftoken=0A4SL7GPCHUNXKQs1V4iAumBtzpMLtAuzdOgvCpeSdx4XMBklXPSSzd9eXHsFRsz',
#     'Host': 'dean.bjtu.edu.cn',
#     'Referer': 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
# }
# def submit_req(hashkey,ans):
#     url = 'https://dean.bjtu.edu.cn//course_selection/courseselecttask/selects_action/?action=submit'
#     data = {'checkboxs': "84400", 'hashkey': hashkey, 'answer': ans}
#
#     res = requests.post(url,data=data,headers=headers)
#     print(res.status_code)
#     print(res.text)
#
# submit_req('asd','sad')

import requests
from bs4 import BeautifulSoup
from PIL import Image
import time

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'sessionid=dslwydcdekumlob3bnb7xvzuprucaf8s; csrftoken=0A4SL7GPCHUNXKQs1V4iAumBtzpMLtAuzdOgvCpeSdx4XMBklXPSSzd9eXHsFRsz',
    'Host': 'dean.bjtu.edu.cn',
    'Referer': 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}
# 打开验证码
def get_captcha():
    q_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'sessionid=dslwydcdekumlob3bnb7xvzuprucaf8s; csrftoken=0A4SL7GPCHUNXKQs1V4iAumBtzpMLtAuzdOgvCpeSdx4XMBklXPSSzd9eXHsFRsz',
        'Host': 'dean.bjtu.edu.cn',
        'Referer': 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'

    }
    ref_url = 'https://dean.bjtu.edu.cn/captcha/refresh/'

    res = requests.get(ref_url,headers=q_headers)
    name = res.json()['key']
    img_url = 'https://dean.bjtu.edu.cn/captcha/image/'+name
    img = requests.get(img_url,headers=q_headers)


    with open('img/'+name+'.png','wb') as f:
        f.write(img.content)

    image = Image.open('img/'+name+'.png')
    image.show()
    return name
# 提交选课请求
def submit_req(hashkey,ans):
    url = 'https://dean.bjtu.edu.cn//course_selection/courseselecttask/selects_action/?action=submit'
    data = {'checkboxs': "84400", 'hashkey': hashkey, 'answer': ans}

    res = requests.post(url,data=data,headers=headers)
    print(res.status_code)
    print(res.text)

def qk():
    req_url = 'https://dean.bjtu.edu.cn/course_selection/courseselecttask/selects_action/?kch=00L093T&kxh=&kclbdm=&kzm=&action=load&iframe=school&submit=&has_advance_query='
    while True:
        # 查找课程
        res = requests.post(req_url,headers=headers)
        soup = BeautifulSoup(res.text,'lxml')
        print(soup)
        try:
            # 无余量时
            msg = soup.find_all('span',class_='red')[0].string
            print(msg)
            time.sleep(0.2)
        #否则
        except:
            print('有余量！！！！！！！！！！！！！！！！！！！！！！！！！')
            # 产生验证码
            hashkey = get_captcha()
            ans = input('输入验证码>>>>>')
            submit_req(hashkey,ans)
            break

qk()
