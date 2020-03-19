import time
import sys

sys.path.append('..')
print(len(sys.path), sys.path)
import spider

now_time = time.localtime()
now_time = time.strftime('%Y-%m-%d', now_time)


def get_url_lists():
    result = set()

    njit = spider.get_html('http://www.njit.edu.cn')
    jwc = spider.get_html('http://jwc.njit.edu.cn')

    nc = spider.njit_catcher(njit)
    result.update(nc.get_all_link())

    time.sleep(1)
    jwcc = spider.jwc_catcher(jwc)
    result.update(jwcc.get_all_link())

    print(len(result), result)
    return result


def get_content(mail):
    send_list = []
    for url in get_url_lists():
        text = spider.get_html(url)
        if text is None:
            print(url + ' cannot load')
            continue
        if '无权访问' in text:
            print(url + ' can only access from local')
            continue

        if 'jwc' in url:
            parser = spider.jwc_parser(text)
        elif 'xinghuo' in url:
            parser = spider.xh_parser(text)
        elif 'www.njit' in url:
            parser = spider.njit_parser(text)
        else:
            print(url, 'cannot find parser')
            continue

        page_time = parser.get_time()
        if now_time == page_time:
            print(url, ' match time')
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
