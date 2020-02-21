import argparse

from data.dataloader import Data


def main():
    # 解析文件为 data
    data = Data(path=args.md, remote_path=args.source)
    for idx, _ in enumerate(data.data):
        if 'integral_2019' in data.data[idx]:
            del data.data[idx]['integral_2019']
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
