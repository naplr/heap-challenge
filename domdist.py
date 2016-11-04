def get_type(s):
    if (s[0] == '#'):
        return 'id'
    elif (s[0] == '.'):
        return 'cls'
    else:
        return 'tag'


def normalize_cls(li):
    newli = []
    clsli = []
    for i in range(len(li)):
        atype = get_type(li[i])
        if atype == 'cls':
            clsli.append(li[i])
        else:
            newli.extend(sorted(clsli))
            newli.append(li[i])
            clsli = []

    if len(clsli) > 0:
        newli.extend(sorted(clsli))

    return newli


def parse(s):
    s = s.strip()
    li = []
    p = 0
    for i in range(len(s)):
        if s[i] == ' ':
            li.append(s[p:i])
            p = i+1
        elif s[i] in ['#', '.']:
            li.append(s[p:i])
            p = i

    li.append(s[p:])

    norm_li = normalize_cls(li)
    # norm_li = li

    return norm_li
        

def initialize_mat(x, y):
    mat = []
    for i in range(len(y)+1):
        mat.append([i])

    for i in range(1, len(x)+1):
        mat[0].append(i)

    return mat


def cal_min_score(mat, i, j, x, y):
    old_diag_score = mat[i-1][j-1]
    old_right_score = mat[i][j-1]
    old_down_score = mat[i-1][j]

    new_diag_score = 100
    new_right_score = 100
    new_down_score = 100

    xtype = get_type(x[j-1])
    ytype = get_type(y[i-1])

    if x[j-1] == y[i-1]:
        new_diag_score = old_diag_score 
        new_right_score = old_right_score 
        new_down_score = old_down_score 
    else:
        if (xtype == 'tag' and ytype == 'tag'):
            new_diag_score = old_diag_score + 1
        else:
            new_diag_score = old_diag_score + 2
        new_right_score = old_right_score + 1
        new_down_score = old_down_score + 1

    return min(new_diag_score, new_right_score, new_down_score)


def lev(x, y):
    mat = initialize_mat(x, y)

    for i in range(1, len(y)+1):
        for j in range(1, len(x)+1):
            min_score = cal_min_score(mat, i, j, x, y)
            mat[i].append(min_score)

    print(mat)
    print(mat[len(y)][len(x)])


if __name__ == '__main__':
    x = parse('div.green.dotted a#login')
    y = parse('a#login div.green.dotted')

    # x = parse('div.header.footer a#signup')
    # y = parse('div.basic.footer.header a#signup')

    # x = parse('div.footer.fixed a#signup.blue.btn')
    # y = parse('div.header li.btn a#signup')

    print(x)
    print(y)

    # x = 'abcdef'
    # y = 'akced'
    lev(x, y)





