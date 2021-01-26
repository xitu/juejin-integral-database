import argparse
import math
import os
from collections import OrderedDict

import requests

from data.dataloader import Data


def main():
    data = Data(path=args.md, remote_path=args.source)
    user_article_map = [{'name': user_record['info']['name'], 'homepage': user_record['info']['url'], 'articles': list(
        map(lambda y: y['article'],
            filter(lambda x: x['type'] == '翻译' or x['type'] == '翻译校对', user_record['data'])))}
                        for user_record in data.data]  # Get translation type records.
    inverted_index = {}
    for user_record in user_article_map:
        for article in user_record['articles']:
            inverted_index[article['name']] = {'user': user_record['name'],
                                               'url': article['url'],
                                               'homepage': user_record['homepage']}
    page = 1
    rs = []
    while True:
        res = requests.get(
            'https://api.github.com/search/issues?repo=xitu/gold-miner&'
            'q=label:翻译完成+'
            'label:' + args.label +
            '+is:pr&per_page=100'
            '&page=' + str(page),
            headers={'Authorization': 'token %s' % open("secret").read()}
        ).json()
        rs += res['items']
        total_page = math.ceil(res['total_count'] / 100)
        print(page, '/', total_page)
        page += 1
        if page > total_page:
            break
    print('Total fetched:', len(rs))
    title_list = list(map(lambda x: x['title'], rs))

    cnt = 0
    out = ''
    for title in title_list:
        if title in inverted_index:
            cnt += 1
            article = inverted_index[title]
            out += '* [{doc_name}]({doc_url})（[{user_name}]({user_homepage}) 翻译）\n'.format(doc_name=title,
                                                                                           doc_url=article['url'],
                                                                                           user_name=article['user'],
                                                                                           user_homepage=article[
                                                                                               'homepage'])
    print('Total match:', cnt)
    print('Start merging...')

    if not os.path.exists(args.target):
        download(args.root_url + args.target, args.target)

    source = parse(out)
    target = parse(open(args.target).read())  # Newest article is in the previous
    source = OrderedDict(reversed(list(source.items())))  # reverse ordered dict
    target = OrderedDict(reversed(list(target.items())))
    for title in source:
        if title not in target:
            target[title] = source[title]
    target = OrderedDict(reversed(list(target.items())))
    out = ""
    for title in target:
        article = target[title]
        out += '* [{doc_name}]({doc_url})（[{user_name}]({user_homepage}) 翻译）\n'.format(doc_name=title,
                                                                                       doc_url=article['url'],
                                                                                       user_name=article['user'],
                                                                                       user_homepage=article[
                                                                                           'homepage'])
    open('new_' + args.target, 'w').write(out)


def parse(text) -> OrderedDict:
    rs = OrderedDict()
    data = text.strip()
    for line in data.split('\n'):
        line = line.strip()
        a, d = line.rsplit('](', 1)
        a, c = a.rsplit('[', 1)
        a, b = a.rsplit('](', 1)
        a = a.split('[', 1)[1]
        b = b.rstrip('() （')
        d = d.rstrip(')） 翻译')
        rs[a] = {'url': b, 'user': c, 'homepage': d}
    return rs


def download(url, path):
    print('Download file from ', url)
    content = requests.get(url).text
    open(path, "w").write(content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--md', default='integrals.md')
    parser.add_argument('--source', default='https://github.com/xitu/gold-miner/raw/master/integrals.md')
    parser.add_argument('--label', default='前端')
    parser.add_argument('--target', default='front-end.md')
    parser.add_argument('--root_url', default='https://github.com/xitu/gold-miner/raw/master/')
    args = parser.parse_args()
    main()
