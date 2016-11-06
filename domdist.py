""" A utility to calculate edit distance between 2 dom string """

import sys
import math

from util import *
from model import Node


def _is_last_elem_in_tag(x, index):
    return get_type(x[index + 1]) == TAG


def _is_elem_in_tag_deletion(left_node, x, index):
    cur_type = get_type(x[index-1])
    return left_node.is_from_deleted_tag and cur_type != TAG

def _is_last_elem_in_tag_deletion(left_node, x, index):
    next_type = get_type(x[index]) if index < len(x) else TAG
    return _is_elem_in_tag_deletion(left_node, x, index) and next_type == TAG


def _generate_new_node(mat, i, j, x, y):
    old_diag_score = mat[i-1][j-1].value
    old_right_score = mat[i][j-1].value
    old_down_score = mat[i-1][j].value

    xtype = get_type(x[j-1])
    ytype = get_type(y[i-1])

    # Calculate new_diag_score
    if x[j-1] == y[i-1]:
        new_diag_score = old_diag_score
    elif (xtype == 'tag' and ytype == 'tag'):
        new_diag_score = old_diag_score + 1
    else:
        # This is an illegal move because you can only 'change' tag
        new_diag_score = sys.maxsize

    # Calcualte new_down_score
    new_down_score = old_down_score + 1

    # Calculate new_right_score
    old_left_node = mat[i][j-1]
    if(_is_last_elem_in_tag_deletion(old_left_node, x, j)):
        new_right_score = old_left_node.deleted_tag_value
    else:
        new_right_score = old_right_score + 1

    # Pick the minimum value
    min_val = min(new_diag_score, new_right_score, new_down_score)

    # Create a new node and set is_from_deleted_tag to True if delete action is selected 
    # and the element is part of tag deletion or a new tag.
    if min_val == new_right_score and (xtype == TAG or _is_elem_in_tag_deletion(old_left_node, x, j)):
        node = Node(min_val, True)
        node.deleted_tag_value = min_val if xtype == TAG else old_left_node.deleted_tag_value
    else:
        node = Node(min_val, False)


    # For debugging purpose.
    if min_val == new_right_score:
        node.direction = 'left'
    elif min_val == new_diag_score:
        node.direction = 'diag'
    elif min_val == new_down_score:
        node.direction = 'up'

    node.x = x[j-1] 
    node.y = y[i-1]

    node.i = j
    node.j = i

    return node


def _lev(x, y):
    """
    Use modified Levenshetein distance algorithm to find the minimum edit.
    """
    mat = initialize_matrix(x, y)

    for i in range(1, len(y)+1):
        for j in range(1, len(x)+1):
            mat[i].append(_generate_new_node(mat, i, j, x, y))

    return mat


def _lev(x, y):
    """
    Use modified Levenshetein distance algorithm to find the minimum edit.
    """
    mat = initialize_matrix(x, y)

    for i in range(1, len(y)+1):
        for j in range(1, len(x)+1):
            mat[i].append(_generate_new_node(mat, i, j, x, y))

    return mat


def debug_get_edit_distance(init_dom, dest_dom):
    parsed_init_dom = parse(init_dom)
    parsed_dest_dom = parse(dest_dom)
    
    mat = _lev(parsed_init_dom, parsed_dest_dom)

    for x in mat:
        for y in x:
            print(y)
        print("===================\n")

    return mat[len(parsed_dest_dom)][len(parsed_init_dom)].value


def get_edit_distance(init_dom, dest_dom):
    parsed_init_dom = parse(init_dom)
    parsed_dest_dom = parse(dest_dom)
    
    mat = _lev(parsed_init_dom, parsed_dest_dom)
    return mat[len(parsed_dest_dom)][len(parsed_init_dom)].value


if __name__ == '__main__':
    print(get_edit_distance('div.green.dotted a#login', 'a#login div.green.dotted'))
    print(get_edit_distance('div.header.footer a#signup', 'div.basic.footer.header a#signup'))
    print(get_edit_distance('div.footer.fixed a#signup.blue.btn', 'div.header li.btn a#signup'))
    print(get_edit_distance('a#enter', 'a#enter.knob.green a#enter a#enter')) # ans = 6
    print(get_edit_distance('a#enter.knob.green', 'a#enter.knob.green a#enter a#enter')) # ans = 4
    print(get_edit_distance('a#enter', 'a#enter.knob.green a#enter a#enter')) # ans = 6
    print(get_edit_distance('header.cf.header div.nav-bar div.lc form.search-form fieldset input.search-field', 'header.cf.header div.nav-bar div.lc div.header-social ul.inline-list.social-list.sprite-social')) # ans = 8
    print(get_edit_distance('div#id span.text a#link.btn', 'a#id.btn')) # ans = 4

    print(debug_get_edit_distance('a#id.btn', 'div#id span.text a#link.btn')) # ans = 6

    # x = ' div div#cnn_maincntnr div.cnn_contentarea.cnn_shdcamtt12010.cnn_shdcamtt1l250.cnn_t1lo_bnews.cnn_t1lo_refresh div#cnn_maintopt1 div#cnn_maintoplive div.cnn_mc2cntr div.cnn_mc23x1cnntr div#cnn_mc2_large1.cnn_mc2_img_right.cnn_mc2_large div div.cnn_mc2_text_left div.cnn_mc2_blurb a'
    # y = ' div div#cnn_maincntnr div.cnn_contentarea.cnn_shdcamtt12010.cnn_shdcamtt1l250.cnn_t1lo_bnews.cnn_t1lo_refresh div#cnn_maintopprofile div#on_tv.cnn_hppersonal div#cnn_pmtvmodule div.cnn_hppersonalfeature div.cnn_pmtvmodddown.cnn_tsbnav form select'
    # print(debug_get_edit_distance(x, y))


    total_diff = 0
    total_wrong = 0
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        for i in range(2, len(lines), 3):
            score = get_edit_distance(lines[i-2], lines[i-1])
            diff = math.fabs(score - int(lines[i]))
            print("{} - {} == {}".format(score, lines[i].strip(), diff))

            total_diff += diff
            total_wrong += 1 if diff != 0 else 0

    print("total diff: {}".format(total_diff))
    print("total wrong: {}".format(total_wrong))

