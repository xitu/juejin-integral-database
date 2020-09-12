import argparse
import math

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
    open(args.label + '.md', 'w').write(out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--md', default='integrals.md')
    parser.add_argument('--source', default='https://github.com/xitu/gold-miner/raw/master/integrals.md')
    parser.add_argument('--label', default='前端')
    parser.add_argument('--database', default='db.bin')
    args = parser.parse_args()
    main()
