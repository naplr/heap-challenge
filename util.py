""" Util methods for domdist.py """

from model import Node


TAG = 'tag'
ID = 'id'
CLS = 'cls'


def _normalize_li(li):
    """
    Sort the class sections of each tag. This is to take into account that the order does not matter.
    """
    norm_li = []
    temp_cls_li = []
    for i in range(len(li)):
        if get_type(li[i]) == CLS:
            temp_cls_li.append(li[i])
        else:
            norm_li.extend(sorted(temp_cls_li))
            norm_li.append(li[i])
            temp_cls_li = []

    # Add the last class element if it exists.
    if len(temp_cls_li) > 0:
        norm_li.extend(sorted(temp_cls_li))

    return norm_li


def get_type(s):
    if (s[0] == '#'):
        return ID
    elif (s[0] == '.'):
        return CLS
    else:
        return TAG


def parse(s):
    s = s.strip()
    li = []

    start_index = 0
    for i in range(len(s)):
        if s[i] in [' ', '#', '.']:
            li.append(s[start_index:i].strip())
            start_index = i

    # Add the last element.
    li.append(s[start_index:])
    norm_li = _normalize_li(li)

    return norm_li


def initialize_matrix(x, y):
    mat = []
    for i in range(len(y)+1):
        mat.append([Node(i, False)])

    val = 0
    for i in range(len(x)):
        val += (1 if get_type(x[i]) == 'tag' else 0)
        mat[0].append(Node(val, True))

    return mat
