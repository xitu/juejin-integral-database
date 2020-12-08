# temporary script for add exchangeing record to data
import argparse

from data.dataloader import Data
from script_add_user import check_user


def add_exchange(data, exchange_content, translator_name, exchange_integral):
    exchange_record = {'type': '减去积分', 'integral': exchange_integral, 'content': exchange_content, 'article': None}
    for user_record in data.data:
        if user_record['info']['name'] == translator_name:
            user_record['data'].insert(0, exchange_record)
            user_record['info']['integral'] -= exchange_integral
            if int(user_record['info']['integral']) < 0:
                print('用户积分小于 0：', translator_name)


def main():
    # 解析文件为 data
    data = Data(path=args.md, remote_path=args.source)
    # 直接在 data 上增加文章，并查找用户。如果用户不存在，则尝试新增用户
    while True:
        try:
            exchange_time = input('兑换时间，留空结束新增：\n')
            if exchange_time == '':
                break
            exchange_content = input('兑换内容（格式：小黄鸭 2 个）：\n')
            translator_name, exchange_integral = input('请输入译者名称与兑换扣除积分（正数），用空格分割：\n').split(' ')
            exchange_integral = float(exchange_integral)
            check_user(data, translator_name)
            add_exchange(data, exchange_time + ' 兑换 ' + exchange_content, translator_name, exchange_integral)
        except Exception as e:
            raise e
            print('兑换 ' + exchange_content + ' 录入失败，请重试')

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
