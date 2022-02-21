# temporary script for add rewarding record to data
import argparse

from data.dataloader import Data
from script_add_user import check_user


def add_reward(data, reward_content, translator_name, reward_integral):
    reward_record = {'type': '奖励', 'integral': reward_integral, 'content': reward_content, 'article': None}
    for user_record in data.data:
        if user_record['info']['name'] == translator_name:
            user_record['data'].insert(0, reward_record)
            user_record['info']['integral'] += reward_integral
            user_record['info']['history_integral'] += reward_integral
            if 'integral_2022' not in user_record['info']:
                user_record['info']['integral_2022'] = reward_integral
            else:
                user_record['info']['integral_2022'] += reward_integral


def main():
    # 解析文件为 data
    data = Data(path=args.md, remote_path=args.source)
    # 直接在 data 上增加文章，并查找用户。如果用户不存在，则尝试新增用户
    while True:
        try:
            reward_content = input('奖励内容，留空结束新增：\n')
            if reward_content == '':
                break
            translator_name, reward_integral = input('请输入译者名称与奖励积分，用空格分割：\n').split(' ')
            reward_integral = float(reward_integral)
            check_user(data, translator_name)
            add_reward(data, reward_content, translator_name, reward_integral)
        except Exception as e:
            raise e
            print('奖励 ' + reward_content + ' 录入失败，请重试')

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
