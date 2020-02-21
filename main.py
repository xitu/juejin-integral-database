import argparse

from data.dataloader import Data


def main():
    # 解析文件为 data
    data = Data(path=args.md, remote_path=args.source)
    # TODO: 加载 data 至 database

    # TODO: 操作 database

    # TODO: 导出 database 至 data

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
