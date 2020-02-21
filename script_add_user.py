def add_user(data, username, userurl):
    user_record = {'info': {
        'name': username,
        'url': userurl,
        'history_integral': 0,
        'integral': 0
    }, 'data': []}
    data.data.append(user_record)


def check_user(data, username):
    # 检查 data 中 username 是否存在；如果不存在则提示新增用户
    search_result = list(filter(lambda user_record: user_record['info']['name'] == username, data.data))
    if not search_result:
        print('未找到用户 ' + username)
        userurl = input('请输入用户 ' + username + '的 github 主页：\n')
        add_user(data, username, userurl)
    else:
        return None
