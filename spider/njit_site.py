import re


class site_parser:
    def __init__(self, text):
        self.text = text

    def get_body(self):
        pass

    def get_time(self):
        pass

    def get_title(self):
        pass

    def plain_match(self, p):
        result = re.findall(p, self.text)
        if len(result) == 0:
            return None
        return re.findall(p, self.text)[0]

    def body_match(self):
        p = '<div id="vsb_content_500">([\s\S]*?)</div>'
        match = self.plain_match(p)
        if match is None:
            p = '<div id="vsb_content">([\s\S]*?)</div>'
            match = self.plain_match(p)
            if match is None:
                match = self.text
        return self.get_body_result(match)

    def get_body_result(self, body):
        body = body.replace('<br>', '').replace('&nbsp;', ' ')
        result = []
        lines = body.split('\n')
        for i in lines:
            pp = '>(.*?)<'
            text = re.findall(pp, i)
            for body in text:
                if body == '':
                    continue
                result.append(body)
        return ''.join(result)


class jwc_parser(site_parser):
    def get_body(self):
        p = 'id=\'vsb_content\' align=center>([\s\S]*?)</div>'
        body = re.findall(p, self.text)[0]
        return self.get_body_result(body)

    def get_title(self):
        p = 'class="title">(.*?)<'
        return self.plain_match(p)

    def get_time(self):
        p = '>时间:(.*?)<'
        return self.plain_match(p)


class xh_parser(site_parser):
    def get_time(self):
        p = '时间：(.*?)<'
        return self.plain_match(p)

    def get_title(self):
        p = '<h1>(.*?)</h1>'
        return self.plain_match(p)

    def get_body(self):
        return self.body_match()


class njit_parser(site_parser):
    def get_body(self):
        return self.body_match()

    def get_title(self):
        p = '<title>(.*?)</title>'
        return self.plain_match(p)

    def get_time(self):
        p = '发表时间：(.*?)&nbsp;'
        return self.plain_match(p)
