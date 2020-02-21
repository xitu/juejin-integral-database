import argparse
import pickle

from data.dataloader import Data


def main():
    # 解析文件为 data
    data = Data(path=args.md, remote_path=args.source)
    # 导出 data 至二进制文件
    pickle.dump(data, open(args.output, 'wb'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--md', default='integrals.md')
    parser.add_argument('--source', default='https://github.com/xitu/gold-miner/raw/master/integrals.md')
    parser.add_argument('--output', default='db.bin')
    args = parser.parse_args()
    main()
