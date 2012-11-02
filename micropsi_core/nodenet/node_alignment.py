#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
Auto-align the net entities in a given nodespace
"""

__author__ = 'joscha'
__date__ = '15.10.12'

from collections import OrderedDict
from micropsi_core.tools import OrderedSet
import math


BORDER = 50.0
GRID = 170.0
PREFERRED_WIDTH = 8.0


def align(nodenet, nodespace):
    """aligns the entities in the given nodenet.
        Arguments:
            nodenet: current node net
            nodespace: the nodespace in which the entities are to be aligned
        Returns:
            True on success, False otherwise
    """
    if not nodespace in nodenet.nodespaces: return False

    unaligned_nodespaces = sorted(nodenet.nodespaces[nodespace].netentities.get("nodespaces", []),
        key=lambda i:nodenet.nodespaces[i].index)
    unaligned_nodes = sorted(nodenet.nodespaces[nodespace].netentities.get("nodes", []),
        key = lambda i: nodenet.nodes[i].index)
    sensors = [ s for s in unaligned_nodes if nodenet.nodes[s].type == "Sensor" ]
    actors = [ a for a in unaligned_nodes if nodenet.nodes[a].type == "Actor" ]
    unaligned_nodes = [ n for n in unaligned_nodes if not nodenet.nodes[n].type in ("Sensor", "Actor") ]


    # position nodespaces

    for i, id in enumerate(unaligned_nodespaces):
        nodenet.nodespaces[id].position = (
            BORDER + (i%PREFERRED_WIDTH+1)*GRID - GRID/2,
            BORDER + int(i/PREFERRED_WIDTH+1)*GRID - GRID/2,
            )

    start_position = (BORDER + GRID/2, BORDER + (0.5+math.ceil(len(unaligned_nodespaces)/PREFERRED_WIDTH))*GRID)

    # simplify linkage
    group = unify_links(nodenet, unaligned_nodes)
    # connect all nodes that have por- and ret-links
    por_groups = group_horizontal_links(group)
    # connect native modules
    # group_other_links(por_groups)
    # group nodes that share a sur-linked parent below that parent
    group_with_same_parent(por_groups)
    # put sensors and actors below
    sensor_group = HorizontalGroup([ DisplayNode(i) for i in sensors ] + [ DisplayNode(i) for i in actors ])
    por_groups.append(sensor_group)
    # calculate actual coordinates by traversing the group structure
    por_groups.arrange(nodenet, start_position)

    return True

INVERSE_DIRECTIONS = { "s": "n", "w": "e", "nw": "se", "ne": "sw",
                       "n": "s", "e": "w", "se": "nw", "sw": "ne",
                       "o": "O", "O": "o", "b": "a", "a": "b" }

class DisplayNode(object):
    def __init__(self, uid, directions = None, parent = None):
        self.uid = uid
        self.directions = directions or {}
        self.parent = parent

    def __repr__(self):
        params = "%s" % str(self.uid)
        if self.directions:
            params += ", dirs: "
            for i in self.directions:
                params += "[%s]: " % i
                for j in self.directions[i]:
                    params += "%s, " % str(j.uid)
        return '%s(%s)' % ("Node", params)

    def __repr__2(self):
        params = "'%s'" % self.uid
        if self.directions:
            params += ", directions=%r" % self.directions
        if self.parent:
            params += ", parent=%r" % self.parent
        return '%s(%s)' % (self.__class__.__name__, params)

    def width(self):
        return 1

    def height(self):
        return 1

    def arrange(self, nodenet, starting_point = (0,0)):
        nodenet.nodes[self.uid].position = starting_point

def unify_links(nodenet, node_id_list):
    """create a proxy representation of the node space to simplify bi-directional links.
    This structure is an ordered set of proxy nodes (DisplayNode) with directions.
    Each direction is marked by its key (such as "n"), and followed by a list of nodes
    that are linked in that direction. The nodes are sorted by their index (as marked in
    the node net).

    Arguments:
        nodenet: the nodenet that we are working on
        node_id_list: a list of node ids to be processed
    """

    node_index = OrderedDict([(i, DisplayNode(i)) for i in node_id_list])

    for node_id in node_id_list:
        node = nodenet.nodes[node_id]
        for gate_type in node.gates:
            direction = {"sub": "s", "ret": "w", "cat": "ne", "sym":"nw",
                         "sur": "n", "por": "e", "exp": "sw", "ref":"se", "gen": "b"}.get(gate_type, "o")
            if direction:
                # "o" is for unknown gate types
                link_ids = node.gates[gate_type].outgoing
                for link_id in link_ids:
                    target_node_id = nodenet.links[link_id].target_node.uid
                    if target_node_id in node_index:
                        # otherwise, the link points outside the current nodespace and will be ignored here
                        if not direction in node_index[node_id].directions:
                            node_index[node_id].directions[direction]=OrderedSet()
                        node_index[node_id].directions[direction].add(node_index[target_node_id])
                        inverse = INVERSE_DIRECTIONS[direction]
                        if not inverse in node_index[target_node_id].directions:
                            node_index[target_node_id].directions[inverse]=OrderedSet()
                        node_index[target_node_id].directions[inverse].add(node_index[node_id])

    # finally, let us sort all node_id_list in the direction groups
    for node_id in node_index:
        for direction in node_index[node_id].directions:
            node_index[node_id].directions[direction] = list(node_index[node_id].directions[direction])
            node_index[node_id].directions[direction].sort(key = lambda i: nodenet.nodes[i.uid].index)

    return UnorderedGroup(node_index.values())

def group_horizontal_links(all_nodes):
    """group direct horizontal links (por)"""
    h_groups = UnorderedGroup()
    excluded_nodes = OrderedSet()
    for i in all_nodes:
        if not i.directions.get("w"): # find leftmost nodes
            excluded_nodes.add(i)
            if i.directions.get("e"):
                h_group = HorizontalGroup([i])
                _add_nodes_horizontally(i, h_group, excluded_nodes)
                if len(h_group) > 1:
                    h_groups.append(h_group)
                else:
                    h_groups.append(i)
            else:
                h_groups.append(i)
        # now handle circles (we find them by identifying left-over nodes that still have "e" links)
    for i in all_nodes:
        if not i in excluded_nodes:
            excluded_nodes.add(i)
            if i.directions.get("e"):
                h_group = HorizontalGroup([i])
                _add_nodes_horizontally(i, h_group, excluded_nodes)
                if len(h_group) > 1:
                    h_groups.append(h_group)
                else:
                    h_groups.append(i)
            else:
                h_groups.append(i)
    _fix_link_inheritance(h_groups, OrderedSet())
    return h_groups

def _add_nodes_horizontally(display_node, h_group, excluded_nodes):
    """recursive helper function for adding horizontally linked nodes to a group"""

    successor_nodes = [ node for node in display_node.directions.get("e", []) if node not in excluded_nodes ]

    if len(successor_nodes) > 1:
        # let us group these guys vertically
        v_group = VerticalGroup()
        for node in successor_nodes:
            excluded_nodes.add(node)
            if node.directions.get("e"):
                local_h_group = HorizontalGroup([node])
                _add_nodes_horizontally(node, local_h_group, excluded_nodes)
                v_group.append(local_h_group)
            else:
                v_group.append(node)
        h_group.append(v_group)

    else:
        if len(successor_nodes) == 1:
            node = successor_nodes[0]
            excluded_nodes.add(node)
            h_group.append(node)
            if node.directions.get("e"):
                _add_nodes_horizontally(node, h_group, excluded_nodes)

def group_other_links(all_groups):
    """group other horizontal links (native modules)"""
    excluded_nodes = OrderedSet()
    _group_other_links(all_groups, excluded_nodes, "O")
    _group_other_links(all_groups, excluded_nodes, "o")
    _fix_link_inheritance(all_groups, OrderedSet())
    return all_groups

def _group_other_links(groups, excluded_nodes, direction):
    for i in groups:
        if i.directions.get(direction): # inverse non-standard links
            predecessors = []
            for node in i.directions[direction]:
                if not node in excluded_nodes and not node.directions.get("w") and not node.directions.get("e"):
                    # this node is not part of another group at this point
                    excluded_nodes.add(node)
                    predecessors.append(node.parent)
            if len(predecessors) == 1:
                i.insert(0, predecessors[0])
            if len(predecessors) > 1:
                i.insert(0, VerticalGroup(predecessors[0]))

def group_with_same_parent(all_groups):
    """group horizontal groups that share the same super-node"""
    # find groups with same super-node
    candidates = OrderedDict()
    for i in all_groups:
        if i.directions.get("n"):
            key = list(i.directions["n"])[0]
            if not candidates.get(key): candidates[key] = []
            candidates[key].append(i)
    # build vertical groups
    for c in candidates:
        h_group = HorizontalGroup()
        for g in candidates[c]:
            if hasattr(g, "uid"): h_group.append(g)
            else:
                for e in g: h_group.append(e)
            all_groups.remove(g)
        parent_group = c.parent
        v_group = VerticalGroup([c, h_group])
        index = parent_group.index(c)
        parent_group[index] = v_group

    #_fix_link_inheritance(all_groups, OrderedSet())
    return all_groups

def _fix_link_inheritance(group, excluded_nodes):
    """recursive helper function to mark for a group and every sub-group into which directions it is linked.
    The function adds the links as .directions to the group and its sub-groups, and carries a set of
    excluded_nodes to remember which links should not be inherited upwards"""

    if hasattr(group, "uid"):
        excluded_nodes.add(group)
    else:
        for i in group:
            locally_excluded_nodes = OrderedSet()
            _fix_link_inheritance(i, locally_excluded_nodes)
            for d in i.directions:
                if not d in group.directions: group.directions[d] = OrderedSet()
                for node in i.directions[d]:
                    group.directions[d].add(node)
            for i in locally_excluded_nodes:
                excluded_nodes.add(i)
        # now delete all links to excluded nodes
        for d in group.directions.keys():
            for node in group.directions[d]:
                if node in excluded_nodes: group.directions[d].remove(node)
            if not group.directions[d]: del group.directions[d]

class UnorderedGroup(list):

    def __init__(self, elements = None, parent = None):
        self.directions = {}
        self.parent = parent
        if elements:
            list.__init__(self, elements)
            for i in elements:
                i.parent = self

    def __repr__(self):
        sig = "Group"
        if self.__class__.__name__ == "HorizontalGroup": sig = "HGroup"
        if self.__class__.__name__ == "VerticalGroup": sig = "VGroup"

        params = ""
        if self.directions:
            params += "dirs: "
            for i in self.directions:
                params += "[%s]: " % i
                for j in self.directions[i]:
                    params += "%s, " % str(j.uid)

        if len(self):
            params += "%r, " % list(self)
        return '%s(%s)' % (sig, params)

    def __repr2__(self):
        params = ""
        if len(self):
            params += "%r" % list(self)
        # if self.parent:
        #    params += ", parent=%r" % self.parent
        if self.directions:
            params += ", directions=%r" % self.directions
        return '%s(%s)' % (self.__class__.__name__, params)

    def width(self):
        width = 0
        for i in self:
            width = max(width, i.width())
        return width

    def height(self):
        height = 0
        for i in self:
            height += i.height()
        return height

    def append(self, element):
        element.parent = self
        list.append(self, element)

    def arrange(self, nodenet, start_position = (0, 0)):
        # arrange elements of unordered group below each other
        x, y = start_position
        for i in self:
            i.arrange(nodenet, (x, y))
            y += i.height()*GRID

class HorizontalGroup(UnorderedGroup):

    def width(self):
        width = 0
        for i in self:
            width += i.width()
        return width

    def height(self):
        height = 0
        for i in self:
            height = max(i.height(), height)
        return height

    def arrange(self, nodenet, start_position = (0,0)):
        x, y = start_position
        for i in self:
            i.arrange(nodenet, (x, y))
            x += i.width()*GRID

class VerticalGroup(UnorderedGroup):

    def width(self):
        width = 0
        for i in self:
            width = max(width, i.width())
        return width

    def height(self):
        height = 0
        for i in self:
            height += i.height()
        return height

    def arrange(self, nodenet, start_position = (0,0)):
        x, y = start_position
        for i in self:
            i.arrange(nodenet, (x, y))
            y += i.height()*GRID