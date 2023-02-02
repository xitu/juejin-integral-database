# temporary script for add article to data
import argparse

from data.dataloader import Data
from script_add_user import check_user


def add_article(data, article_name, article_url, translator_name, translator_integral, proofreader_name_list,
                proofreader_integral_list):
    article = {'name': article_name, 'url': article_url}
    # 给译者加分
    add_article_for_user(data, translator_name, article, '翻译', translator_integral)
    # 给校对加分
    for proofreader_name, proofreader_integral in zip(proofreader_name_list, proofreader_integral_list):
        add_article_for_user(data, proofreader_name, article, '校对', proofreader_integral)


def add_article_for_user(data, username, article, type, integral):
    article_record = {'type': type, 'integral': integral, 'content': None, 'article': article}
    for user_record in data.data:
        if user_record['info']['name'] == username:
            user_record['data'].insert(0, article_record)
            user_record['info']['integral'] += integral
            user_record['info']['history_integral'] += integral
            if 'integral_yearly' not in user_record['info']:
                user_record['info']['integral_yearly'] = integral
            else:
                user_record['info']['integral_yearly'] += integral


def main():
    # 解析文件为 data
    data = Data(path=args.md, remote_path=args.source)
    # 直接在 data 上增加文章，并查找用户。如果用户不存在，则尝试新增用户
    while True:
        try:
            article_name = input('请输入新增文章名称，留空结束新增：\n')
            if article_name == '':
                break
            article_url = input('请输入新增文章url：\n')
            translator_name, translator_integral = input('请输入译者名称与翻译积分，用空格分割：\n').split(' ')
            translator_integral = float(translator_integral)
            check_user(data, translator_name)
            print('开始录入校对信息，留空完成录入')
            proofreader_name_list = []
            proofreader_integral_list = []
            while True:
                proofreader_name_and_integral = input('请输入第%d位校对名称与校对积分，用空格分割：\n' % (len(proofreader_name_list) + 1))
                if proofreader_name_and_integral == '':
                    break
                proofreader_name, proofreader_integral = proofreader_name_and_integral.split(' ')
                check_user(data, proofreader_name)
                proofreader_name_list.append(proofreader_name)
                proofreader_integral_list.append(float(proofreader_integral))
            else:
                print('您一共输入了%d位校对者')

            add_article(data, article_name, article_url, translator_name, translator_integral, proofreader_name_list,
                        proofreader_integral_list)
        except Exception as e:
            raise e
            print('文章 ' + article_name + ' 录入失败，请重试')

    # 导出 data 至文件
    data.export(output=args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--md', default='integrals.md')
    parser.add_argument('--source', default='https://github.com/xitu/gold-miner/raw/master/integrals.md')
    parser.add_argument('--output', default='integrals_new.md')
    parser.add_argument('--database', default='db.bin')
    args = parser.parse_args()
    main()
