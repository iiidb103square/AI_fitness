def bodyType(bodysize):  # 分辨體態用
    print("module.bodyType_start")    
    # demo 用的使用者資料

    sex = '男'
    fat = 20
    size = bodysize   
    # 體態類型
    means = {'1': '消瘦型',     '4': '精實型',   '7': '運動員型',
             '2': '精瘦型',     '5': '標準型',   '8': '超重型',
             '3': '陰性肥胖型', '6': '高脂肪型', '9': '肥胖型'}
    
    # 體態判別式
    if sex == '男':
        if size == 'S':
            if fat > 25:
                return means['3']
            elif fat < 14:
                return means['1']
            else:
                return means['2']

        elif size == 'M':
            if fat > 25:
                return means['6']
            elif fat < 14:
                return means['4']
            else:
                return means['5']

        else:
            if fat > 25:
                return means['9']
            elif fat < 14:
                return means['7']
            else:
                return means['8']

    if sex == '女':
        if size == 'S':
            if fat > 30:
                return means['3']
            elif fat < 17:
                return means['1']
            else:
                return means['2']

        elif size == 'M':
            if fat > 30:
                return means['6']
            elif fat < 17:
                return means['4']
            else:
                return means['5']

        else:
            if fat > 30:
                return means['9']
            elif fat < 17:
                return means['7']
            else:
                return means['8']


