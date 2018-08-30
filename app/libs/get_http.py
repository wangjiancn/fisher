# coding = utf-8
import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        # 三元表达式写法
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return {} if return_json else ''
            return r.json() if return_json else r.text
        except:
            return ""
        # 普通写法
        # r = requests.get(url)
        # if r.status_code ==200:
        #     if return_json:
        #         return r.json()
        #     else:
        #         return r.text
        # else:
        #     if return_json:
        #         return {}
        #     else:
        #         return ''


# t = HTTP()
# r = t.get(url='http://t.yushu.im/v2/book/isbn/9787501524044')
