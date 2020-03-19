import requests
import time
import sys
import re

sys.path.append('..')
print(sys.path)
import spider

now_time = time.localtime()
now_time = time.strftime('%Y-%m-%d', now_time)


def get_url_lists():
    result = []
    url = 'http://jwc.njit.edu.cn/'
    r = requests.get(url)
    if r.status_code != 200:
        print('website index booooooom!')

    p = 'href="content.jsp(.*?)"  target="_blank"'
    jwc = re.findall(p, r.text)
    for i in jwc:
        result.append(url + 'content.jsp' + i)

    p = 'href="http://www.njit.edu.cn/info(.*?)"  target="_blank"'
    njit = re.findall(p, r.text)
    for i in njit:
        result.append('http://www.njit.edu.cn/info' + i)

    p = 'href="http://xinghuo.njit.edu.cn/info(.*?)"  target="_blank"'
    xh = re.findall(p, r.text)
    for i in xh:
        result.append('http://xinghuo.njit.edu.cn/info' + i)

    print(len(result), result)
    return result


def get_content(mail):
    send_list = []
    for url in get_url_lists():
        r = requests.get(url=url)
        r.encoding = 'utf-8'
        if r.status_code != 200:
            print(url + ' cannot load')
            continue
        if r.url == 'http://jwc.njit.edu.cn/system/resource/code/auth/auth.htm':
            print(url + ' can only access from local')
            continue

        if 'jwc' in url:
            parser = spider.jwc_parser(r.text)
        elif 'xinghuo' in url:
            parser = spider.xh_parser(r.text)
        else:
            parser = spider.njit_parser(r.text)

        page_time = parser.get_time()
        if now_time == page_time:
            # if True:
            title = parser.get_title()
            body = parser.get_body()

            send_list.append((page_time + " NJIT:" + title, title + '\n' + body + '\n\n' + url))

        time.sleep(1)

    print(len(send_list), send_list)

    for send in send_list:
        title = send[0]
        body = send[1]

        mail.send_mail_to(title, body)
        time.sleep(1)


def main(mail):
    get_content(mail)


if __name__ == '__main__':
    if (len(sys.argv) != 1):
        password = sys.argv[1]
        mail = spider.SMTP(password)
        main(mail)
