import copy
import os
import re
import urllib.request

import markdown
from lxml import etree
from tqdm import tqdm

from utils import formatNumber


class Data:
    def __init__(self, path, remote_path=None):
        self.path = path
        if not os.path.exists(path):
            self.download(remote_path, path)
        self.data = []  # 用 list 按用户记录存储数据
        self.header = ""
        self.table_header_sep = "|------|-------|-------|\n"
        data = self.load(path)
        self.parse(data)

    @staticmethod
    def download(url, path):
        print('Download file from ', url)
        f = urllib.request.urlopen(url)
        with open(path, "wb") as code:
            code.write(f.read())

    def load(self, path, header_line=6):
        file = open(path, 'r').read()
        lines = [line.strip() for line in file.split('\n')]
        self.header = '\n'.join(lines[:header_line])
        lines = lines[header_line:]
        return lines

    def parse(self, lines):
        print('Parsing data...')
        initial_user_record = {'info': {}, 'data': []}
        initial_record = {'type': None, 'integral': 0, 'content': None, 'article': {'name': None, 'url': None}}
        user_record = copy.deepcopy(initial_user_record)
        for l in tqdm(lines):
            if '|类型|积分|' in l or '|------' in l:
                # 忽略表头
                continue
            if l is '':
                continue
            if l.startswith('#'):
                # 将上一个用户的记录存入 list
                if user_record['info']:
                    self.data.append(user_record)
                    user_record = copy.deepcopy(initial_user_record)
                try:
                    user_record['info'] = self.extract_user_info(l)
                except AssertionError:
                    print('Error occur while parse user information : \n', l)
            else:
                if '待更新' in l:
                    continue
                record = copy.deepcopy(initial_record)
                text, action, integral = l.strip('|').split('|')
                if "+" in integral:
                    integral = eval(integral)
                if action in ['翻译', '校对', '翻译校对']:
                    record['type'] = action
                    try:
                        record['article'] = self.parse_article(text)
                    except Exception:
                        print(text)
                        print("Parse failed.")
                        raise SyntaxError
                    record['integral'] = float(integral)
                    record['content'] = None
                else:
                    record['type'] = action
                    record['content'] = text
                    record['integral'] = float(integral)
                    record['article'] = None

                user_record['data'].append(record)
        else:
            # 最后一个记录入库
            self.data.append(user_record)

    def export(self, output):
        print('Exporting data...')
        with open(output, 'w') as writer:
            writer.write(self.header)
            for user_record in tqdm(self.data):
                writer.write('\n')
                head = "## 译者：[{}]({}) 历史贡献积分：{} 当前积分：{}".format(user_record['info']['name'],
                                                                 user_record['info']['url'],
                                                                 formatNumber(user_record['info']['history_integral']),
                                                                 formatNumber(user_record['info']['integral']))
                if "integral_2021" in user_record['info']:
                    head += " 二零二一：{}".format(formatNumber(user_record['info']['integral_2021']))
                writer.write(head + '\n\n')
                writer.write("|文章|类型|积分|" + '\n')
                writer.write(self.table_header_sep)
                for record in user_record['data']:
                    if record['article'] is not None:
                        if record['article']['url'] != "" and record['article']['url'] is not None:
                            article = "|[{}]({})|{}|{}|".format(record['article']['name'], record['article']['url'],
                                                                record['type'], formatNumber(record['integral']))
                        else:
                            article = "|{}|{}|{}|".format(record['article']['name'],
                                                          record['type'], formatNumber(record['integral']))
                        writer.write(article + '\n')
                    else:
                        writer.write("|{}|{}|{}|".format(record['content'], record['type'],
                                                         formatNumber(record['integral'])) + '\n')

    @staticmethod
    def extract_user_info(text):
        username_re = re.compile(r'\[(.+)\]')
        userurl_re = re.compile(r'\((.+)\)')
        user_part_re = re.compile(r'\[.+\]\(.+\)')
        number_re = re.compile(r'-?\d+\.?\d*')
        username = username_re.search(text).group(1)
        userurl = userurl_re.search(text).group(1)
        integral_part = user_part_re.split(text)[-1]
        integrals = number_re.findall(integral_part)
        integrals = list(map(float, integrals))
        if len(integrals) is 3:
            # 有 2021 年积分记录
            history_integral, integral, integral_2021 = integrals
            assert history_integral >= integral
            assert history_integral >= integral_2021
            return {'name': username, 'url': userurl, 'history_integral': history_integral,
                    'integral': integral, 'integral_2021': integral_2021}
        elif len(integrals) is 2:
            # 没有 2021 年积分记录
            history_integral, integral = integrals
            assert history_integral >= integral
            return {'name': username, 'url': userurl, 'history_integral': history_integral,
                    'integral': integral}
        else:
            raise SyntaxError('Format error')

    @staticmethod
    def parse_article(text):
        md_html = markdown.markdown(text)
        md_html = md_html.replace('<code>', '`').replace('</code>', '`')
        doc = etree.fromstring(md_html)
        link = doc.xpath('//a')
        if len(link) == 0:  # 没有链接只有题目
            return {'name': text, 'url': ''}
        assert len(link) == 1
        articlename = link[0].text
        articleurl = link[0].get('href')
        return {'name': articlename, 'url': articleurl}
