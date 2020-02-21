# temporary script for statistics data during 2019
import argparse

from data.dataloader import Data


def main():
    # 解析文件为 data
    data = Data(path=args.md, remote_path=args.source)
    to_statistic = list(filter(lambda user_record: 'integral_2019' in user_record['info'], data.data))
    ordered_2019 = sorted(to_statistic, key=lambda user_record: -user_record['info']['integral_2019'])
    print('2019 年度积分统计结果如下：')
    for user_record in ordered_2019[:50]:
        print('{:<15}2019 年度积分：{:<8}总积分：{:<8}'.format(
            user_record['info']['name'],
            user_record['info']['integral_2019'],
            user_record['info']['history_integral']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--md', default='integrals.md')
    parser.add_argument('--source', default='https://github.com/xitu/gold-miner/raw/master/integrals.md')
    args = parser.parse_args()
    main()
