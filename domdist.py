import sys
import math


class Node:
    def __init__(self, value, is_from_deleted_tag):
        self.value = value
        self.is_from_deleted_tag = is_from_deleted_tag
        self.deleted_tag_value = sys.maxsize

    def __repr__(self):
        return "[{}, {}]".format(self.value, self.is_from_deleted_tag)


def _get_type(s):
    if (s[0] == '#'):
        return 'id'
    elif (s[0] == '.'):
        return 'cls'
    else:
        return 'tag'


def _initialize_matrix(x, y):
    mat = []
    for i in range(len(y)+1):
        mat.append([Node(i, False)])

    val = 0
    for i in range(len(x)):
        val += (1 if _get_type(x[i]) == 'tag' else 0)
        mat[0].append(Node(val, True))

    return mat


def _normalize_li(li):
    """
    Sort the class sections of each tag.
    """
    norm_li = []
    temp_cls_li = []
    for i in range(len(li)):
        t = _get_type(li[i])
        if t == 'cls':
            temp_cls_li.append(li[i])
        else:
            norm_li.extend(sorted(temp_cls_li))
            norm_li.append(li[i])
            temp_cls_li = []

    if len(temp_cls_li) > 0:
        norm_li.extend(sorted(temp_cls_li))

    return norm_li


def _parse(s):
    s = s.strip()
    li = []

    start_index = 0
    for i in range(len(s)):
        if s[i] == ' ':
            li.append(s[start_index:i])
            start_index = i+1
        elif s[i] in ['#', '.']:
            li.append(s[start_index:i])
            start_index = i

    li.append(s[start_index:])
    norm_li = _normalize_li(li)

    return norm_li
        

def _calculate_min_score(mat, i, j, x, y):
    is_from_deleted_tag = False
    old_diag_score = mat[i-1][j-1].value
    old_right_score = mat[i][j-1].value
    old_down_score = mat[i-1][j].value

    old_right_node = mat[i][j-1]

    xtype = _get_type(x[j-1])
    ytype = _get_type(y[i-1])

    if x[j-1] == y[i-1]:
        new_diag_score = old_diag_score 
        new_right_score = old_right_score + 1
        new_down_score = old_down_score + 1
    else:
        if (xtype == 'tag' and ytype == 'tag'):
            new_diag_score = old_diag_score + 1
        else:
            # This is an illegal move because you can only 'change' tag
            new_diag_score = sys.maxsize

        next_xtype = _get_type(x[j]) if j < len(x) else 'tag'
        if (old_right_node.is_from_deleted_tag and xtype != 'tag' and next_xtype == 'tag'):
            new_right_score = old_right_node.deleted_tag_value

        # if (old_right_node.is_from_deleted_tag and xtype != 'tag'):
            # new_right_score = old_right_score
        else:
            new_right_score = old_right_score + 1

        new_down_score = old_down_score + 1

    # Get the new node. If it is from deleted tag, set the flag to True.
    min_val = min(new_diag_score, new_right_score, new_down_score)

    node = Node(min_val, is_from_deleted_tag)
    
    prev_xtype = _get_type(x[j-2])
    if min_val == new_right_score and (xtype == 'tag' or old_right_node.is_from_deleted_tag) and not (x[j-1] == y[i-1]):
        is_from_deleted_tag = True
        node.is_from_deleted_tag = True

        if xtype == 'tag':
            node.deleted_tag_value = min_val
        else:
            node.deleted_tag_value = old_right_node.deleted_tag_value

    return node

def _lev(x, y):
    """
    Use modified Levenshetein distance algorithm to find the minimum edit.
    """
    mat = _initialize_matrix(x, y)

    for i in range(1, len(y)+1):
        for j in range(1, len(x)+1):
            mat[i].append(_calculate_min_score(mat, i, j, x, y))

    return mat[len(y)][len(x)].value


def _lev_mat(x, y):
    """
    Use modified Levenshetein distance algorithm to find the minimum edit.
    """
    mat = _initialize_matrix(x, y)

    for i in range(1, len(y)+1):
        for j in range(1, len(x)+1):
            mat[i].append(_calculate_min_score(mat, i, j, x, y))

    return mat


def get_edit_distance(init_dom, dest_dorm):
    return _lev(_parse(init_dom), _parse(dest_dorm))


if __name__ == '__main__':
    x = _parse('div.green.dotted a#login')
    y = _parse('a#login div.green.dotted')
    print(_lev(x,y))
    # mat = _lev(x, y)

    # for x in mat:
        # for y in x:
            # print(y)
            # print('\n')
        # print("===================\n")

    x = _parse('div.header.footer a#signup')
    y = _parse('div.basic.footer.header a#signup')
    print(_lev(x,y))

    x = _parse('div.footer.fixed a#signup.blue.btn')
    y = _parse('div.header li.btn a#signup')
    print(_lev(x,y))

    #6
    print(get_edit_distance('a#enter', 'a#enter.knob.green a#enter a#enter'))

    #4
    print(get_edit_distance('a#enter.knob.green', 'a#enter.knob.green a#enter a#enter'))

    #6
    print(get_edit_distance('a#enter', 'a#enter.knob.green a#enter a#enter'))

    #8
    print(get_edit_distance('header.cf.header div.nav-bar div.lc form.search-form fieldset input.search-field', 'header.cf.header div.nav-bar div.lc div.header-social ul.inline-list.social-list.sprite-social'))

    #4
    print(get_edit_distance('div#id span.text a#link.btn', 'a#id.btn'))
    mat = _lev_mat(_parse('div#id span.text a#link.btn'), _parse('a#id.btn'))

    for x in mat:
        for y in x:
            print(y)
            # print('\n')
        print("===================\n")


    total_diff = 0
    total_wrong = 0
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        for i in range(2, len(lines), 3):
            score = get_edit_distance(lines[i-2], lines[i-1])
            diff = math.fabs(score - int(lines[i]))
            print("{} - {} == {}".format(score, lines[i].strip(), diff))

            total_diff += diff
            if diff != 0:
                total_wrong += 1

    print("total diff: {}".format(total_diff))
    print("total wrong: {}".format(total_wrong))

