import re


class link_catcher:
    def __init__(self, text):
        self.text = text
        self.set = set()

    def parse_link(self, p, prefix=None):
        match = re.findall(p, self.text)
        if prefix is not None:
            for i in range(len(match)):
                match[i] = prefix + match[i]
        self.set.update(match)
        return self.set

    def get_all_link(self):
        pass


class njit_catcher(link_catcher):
    def get_all_link(self):
        self.get_local_link()
        self.get_info_link()
        self.get_xh_link()
        return self.set

    def get_local_link(self):
        p = 'href="content.jsp(.*?)"'
        return self.parse_link(p, 'http://www.njit.edu.cn/content.jsp')

    def get_info_link(self):
        p = 'href="info(.*?)"'
        return self.parse_link(p, 'http://www.njit.edu.cn/info')

    def get_xh_link(self):
        p = 'href="http://xinghuo.njit.edu.cn/info(.*?)"'
        return self.parse_link(p, 'http://xinghuo.njit.edu.cn/info')


class jwc_catcher(link_catcher):
    def get_all_link(self):
        self.get_njit_link()
        self.get_info_link()
        self.get_xh_link()
        return self.set

    def get_njit_link(self):
        p = 'href="content.jsp(.*?)"'
        return self.parse_link(p, 'http://jwc.njit.edu.cn/content.jsp')

    def get_info_link(self):
        p = 'href="http://www.njit.edu.cn/info(.*?)"'
        return self.parse_link(p, 'http://www.njit.edu.cn/info')

    def get_xh_link(self):
        p = 'href="http://xinghuo.njit.edu.cn/info(.*?)"'
        return self.parse_link(p, 'http://xinghuo.njit.edu.cn/info')


if __name__ == '__main__':
    # r = requests.get('http://www.njit.edu.cn')
    # r.encoding = 'utf-8'
    # catcher = njit_catcher(r.text)
    # links = catcher.get_all_link()
    # print(len(links), links)
    import spider

    text = spider.get_html('http://jwc.njit.edu.cn/')
    catcher = jwc_catcher(text)
    link = catcher.get_all_link()
    print(len(link), link)
