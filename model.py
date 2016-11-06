""" Data types for domdist.py """

import sys

class Node:
    def __init__(self, value, is_from_deleted_tag):
        self.value = value
        self.is_from_deleted_tag = is_from_deleted_tag
        self.deleted_tag_value = sys.maxsize
        self.direction = None
        self.x = None
        self.y = None
        self.i = None
        self.j = None

    def __repr__(self):
        return "[({},{}) {}, {}, {}, {}, {}]".format(self.i, self.j, self.value, self.is_from_deleted_tag, self.direction, self.x, self.y)
