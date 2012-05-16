"""
Nodenet definition
"""

from uuid import uuid1 as generate_uid

__author__ = 'joscha'
__date__ = '09.05.12'

class Nodenet(object):
    """Main data structure for MicroPsi agents,

    Contains the net entities and runs the activation spreading

    Attributes:
        nodespaces: A dictionary of node space UIDs and respective node spaces
        nodes: A dictionary of node UIDs and respective nodes
        calculate_always_nodes: A set of nodes that is either always active, or has received activation directly
        calculate_now_nodes: A set of nodes that has received activation in the current step
        links: A dictionary of link UIDs and respective links
        datasources: A dictionary of data source UIDs and data sources
        datatargets: A dictionary of data target UIDs and data targets
        gate_types: A dictionary of gate type names and the individual types of gates
        slot_types: A dictionary of slot type names and the individual types of slots
        native_module_types: A dictionary of native module names and individual native modules types
        step: a counter for the current simulation step
        worldadapter: A world adapter object residing in a world implementation
    """

    def __init__(self, worldadapter, name = ""):
        """create a new MicroPsi agent

        Arguments:
            worldadapter: the interface of this agent to its environment
            name (optional): a name for the agent and its resources. If the name matches an existing nodenet definition,
                the agent will use this definition.
        """

        self.uid = generate_uid()
        self.name = name
        self.nodespaces = {}
        self.nodes = {}
        self.calculate_always_nodes = {}
        self.calculate_now_nodes = {}
        self.links = {}
        self.gate_types = {}
        self.slot_types = {}
        self.native_module_types = {}
        self.step = 0
        self.worldadapter = worldadapter
        self.datasources = worldadapter.datasources
        self.datatargets = worldadapter.datatargets
        #TODO set up persistence
        #TODO set up initial nodespace


    #TODO add functionality for adding, editing and removing of nodes, links, native modules, nodespaces, etc

    def reset(self):
        """Revert to state of last save"""
        pass

    def set_worldadapter(self, worldadapter):
        """connects the nodenet with a worldadapter, and thus to some external environment"""
        self.worldadapter = worldadapter
        self.datasources = worldadapter.datasources
        self.datatargets = worldadapter.datatargets
        #TODO change connection of all sensors and actors

    def get_nodespace_view(self, nodespace_uid):
        """returns the nodes and links in a given nodespace"""
        pass

    # add functions for exporting and importing node nets
    def export_data(self):
        """serializes and returns the nodenet data for export to a end user"""
        pass

    def import_data(self, nodenet_data):
        """imports nodenet data as the current node net"""
        pass

    def merge_data(self, nodenet_data):
        """merges the nodenet data with the current node net, might have to give new UIDs to some entities"""
        pass

    def step(self):
        """perform a simulation step"""
        self.propagate_link_activation()
        self.calculate_node_functions()
        self.step +=1

    def propagate_link_activation(self):
        """propagate activation through all links, taking it from the gates and summing it up in the slots"""
        pass

    def calculate_node_functions(self):
        """for all active nodes, call their node function, which in turn should update the gate functions"""
        pass


class NetEntity(object):
    """The basic building blocks of node nets.

    Attributes:
        uid: the unique identifier of the net entity
        name: a human readable name (optional)
        position: a pair of coordinates on the screen
        nodenet: the node net in which the entity resides
        parent_nodespace: the node space this entity is contained in
    """

    def __init__(self, position, nodenet, parent_nodespace, name = ""):
        """create a net entity at a certain position and in a given node space"""

        self.uid = generate_uid()
        self.name = name
        self.position = position
        self.nodenet = nodenet
        self.parent_nodespace = parent_nodespace

class Comment(NetEntity):
    """Comments are simple text boxes that can be arbitrarily positioned to aid in understanding the node net.

    Attributes:
        the same as for NetEntities, and
        comment: a string of text
    """

    def __init__(self, position, nodenet, parent_nodespace, comment = ""):
        self.comment = comment
        NetEntity.__init__(position, nodenet, parent_nodespace, name = "Comment")

class Nodespace(NetEntity):
    """A container for net entities.

    One nodespace is marked as root, all others are contained in
    exactly one other nodespace.

    Attributes:
        activators: a dictionary of activators that control the spread of activation, via activator nodes
        netentities: a dictionary containing all the contained nodes and nodespaces, to speed up drawing
    """
    def __init__(self, position, nodenet, parent_nodespace = None, name = ""):
        """create a node space at a given position and within a given node space"""
        self.activators = {}
        self.netentities = {}
        NetEntity.__init__(self, position, nodenet, parent_nodespace, name)

    def get_contents(self):
        """returns a dictionary with all contained net entities, related links and dependent nodes"""
        pass

class Link(object):
    """A link between two nodes, starting from a gate and ending in a slot.

    Links propagate activation between nodes and thereby facilitate the function of the agent.
    Links have weights, but apart from that, all their properties are held in the gates where they emanate.
    Gates contain parameters, and the gate type effectively determines a link type.

    You may retrieve links either from the global dictionary (by uid), or from the gates of nodes themselves.
    """
    def __init__(self, source_node, source_gate_name, target_node, target_slot_name, weight = 1):
        """create a link between the source_node and the target_node, from the source_gate to the target_slot

        Attributes:
            weight (optional): the weight of the link (default is 1)
        """
        self.uid = generate_uid()
        self.link(source_node, source_gate_name, target_node, target_slot_name, weight)

    def link(self, source_node, source_gate_name, target_node, target_slot_name, weight = 1):
        """link between source and target nodes, from a gate to a slot.

            You may call this function to change the connections of an existing link. If the link is already
            linked, it will be unlinked first.
        """
        if self.source_node: self.source_gate.outgoing.remove(self.uid)
        if self.target_node: self.target_slot.incoming.remove(self.uid)
        self.source_node = source_node
        self.target_node = target_node
        self.source_gate = source_node.get_gate(source_gate_name)
        self.target_slot = target_node.get_slot(target_slot_name)
        self.weight = weight
        self.source_gate.outgoing.add(self.uid)
        self.target_slot.incoming[self.uid] = 0

    def __del__(self):
        """unplug the link from the node net"""
        self.source_gate.outgoing.remove(self.uid)
        del self.target_slot.incoming[self.uid]

class Node(NetEntity):
    """A net entity with slots and gates and a node function.

    Node functions are called alternating with the link functions. They process the information in the slots
    and usually call all the gate functions to transmit the activation towards the links.

    Attributes:
        activation: a numeric value (usually between -1 and 1) to indicate its activation. Activation is determined
            by the node function, usually depending on the value of the slots.
        slots: a list of slots (activation inlets)
        gates: a list of gates (activation outlets)
        node_function: a function to be executed whenever the node receives activation
    """

    def __init__(self, position, nodenet, parent_nodespace = 0, activation = 0, name = ""):
        self.activation = activation
        self.slots = []
        self.gates = []
        NetEntity.__init__(position, nodenet, parent_nodespace, name)

    def node_function(self):
        """called whenever the node is activated or active"""
        # process the slots
        if self.slots:
            activation = 0
            for i in self.slots:
                if self.slots[i].incoming:
                    if self.slots[i].current_step <
        self.activation = sum([self.slots[slot].incoming[link] for slot in self.slots for link in self.slots[slot].incoming])

class Gate(object):
    """The activation outlet of a node. Nodes may have many gates, from which links originate.

    Attributes:
        type: a string that determines the type of the gate
        node: the parent node of the gate
        activation: a numerical value which is calculated at every step by the gate function
        parameters: a dictionary of values used by the gate function
        gate_function: called by the node function, updates the activation
        outgoing: the set of links originating at the gate
    """
    def __init__(self, type, node, parameters = None):
        """create a gate.

        Parameters:
            type: a string that refers to a node type
            node: the parent node
            parameters: an optional dictionary of parameters for the gate function
        """
        self.type = type
        self.node = node
        self.parameters = parameters
        self.activation = 0
        self.outgoing = {}
        if parameters: self.parameters = parameters
        else:
            self.parameters = {
                "minimum": -1,
                "maximum": 1,
                "certainty": 1,
                "amplification": 1,
                "threshold": 0,
                "decay": 0
            }

    def gate_function(self, input_activation):
        """This function sets the activation of the gate.

        The gate function should be called by the node function, and can be replaced by different functions
        if necessary. This default gives a linear function (input * amplification), cut off below a threshold.
        You might want to replace it with a radial basis function, for instance.
        """

        gate_factor = 1

        # check if the current node space has an activator that would prevent the activity of this gate
        if self.type in self.node.parent_nodespace.activators:
            gate_factor = self.node.parent_nodespace.activators[self.type]
            if gate_factor == 0.0:
                self.activation = 0
                return  # if the gate is closed, we don't need to execute the gate function

        # simple linear threshold function; you might want to use a sigmoid for neural learning
        activation = max(input_activation, self.parameters["threshold"]) * self.parameters["amplification"] *gate_factor

        if self.parameters["decay"]:  # let activation decay gradually
            if activation < 0:
                activation = min(activation, self.activation*(1-self.parameters["decay"]))
            else:
                activation = max(activation, self.activation*(1-self.parameters["decay"]))

        self.activation = min(self.parameters["maximum"],max(self.parameters["minimum"],activation))

class Slot(object):
    """The entrance of activation into a node. Nodes may have many slots, in which links terminate.

    Attributes:
        type: a string that determines the type of the slot
        node: the parent node of the slot
        activation: a numerical value which is the sum of all incoming activations
        current_step: the simulation step when the slot last received activation
        incoming: a dictionary of incoming links together with the respective activation received by them
    """

    def __init__(self, type, node):
        """create a slot.

        Parameters:
            type: a string that refers to the slot type
            node: the parent node
        """
        self.type = type
        self.incoming = {}
        self.current_step = -1
        self.activation = 0

class NativeModule(Node):
    """A node with a complex node function that may perform arbitrary operations on the node net

        Native Modules encapsulate arbitrary functionality within the node net. They are written in a
        programming language (here: Python) and refer to an external resource file for the code, so it
        can be edited at runtime.
    """
    pass