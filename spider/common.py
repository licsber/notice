import requests
import os


def parse_cookies(cookie_str):
    cookie_str = cookie_str.replace('"', '')
    ss = cookie_str.split(';')
    result = {}
    for s in ss:
        k, v = s.split('=')
        result[k] = v
    return result


def download(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.content
    return b''


def file_exists_or_has_content(file_path):
    if not os.path.exists(file_path):
        return False
    with open(file_path, 'rb') as f:
        b = f.read(1)
        return len(b) != 0


if __name__ == '__main__':
    cookie = '"PHPSESSID=prifumsi4fv8h3kh017tql8p6c; _gid=978693621275; _gidv=39c7e4d4060e58949878bfbb03bd64f6; Hm_lvt_a84b27ffd87daa3273555205ef60df89=1582717654,1582717684; Hm_lpvt_a84b27ffd87daa3273555205ef60df89=1582717881"'
    cookie = parse_cookies(cookie)
    print(cookie)
