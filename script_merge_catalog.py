import argparse
import os
import re
import urllib.request
from collections import OrderedDict


def main():
    if not os.path.exists(args.source):
        print('Couldn\'t find file', args.source)
        exit()
    if not os.path.exists(args.target):
        download(args.root_url + args.target, args.target)
    source = parse(args.source)
    target = parse(args.target)  # Newest article is in the previous
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


clean_func = lambda x: x.strip('[]()（）翻译 *')


def parse(path) -> OrderedDict:
    rs = OrderedDict()
    file = open(path, 'r').read().strip()
    for line in file.split('\n'):
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
    f = urllib.request.urlopen(url)
    with open(path, "wb") as code:
        code.write(f.read())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='Android_old.md')
    parser.add_argument('--target', default='android.md')
    parser.add_argument('--root_url', default='https://github.com/xitu/gold-miner/raw/master/')
    args = parser.parse_args()
    main()
