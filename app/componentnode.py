#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Represent a Drawflow node as a ComponentNode with data relevent for the
generated Python configuration file.

ComponentNode objects are intended to, but not restricted to, only work with
ComponentTree objects.
"""


class ComponentNode:
    """
    Structured representation of Drawflow data nodes.

    Attributes
    ----------
    class_name: str = None
        Name of the component class. e.g. an Adder SST component will require
        a single class for implementation. That same class may be reused with
        different parameter and link values. However, the configuration of the
        parameters and links will be consistent.

    type: int = 0
        Type of the Drawflow node, provided by the "id" field generated when a
        node is added to the canvas. In an unexpanded hierarchy structure, the
        type is a unique attribute useful for determining the number of copies
        of the node required.

    name: str = None
        Unique name of the component, generated by the class_name and the
        number of occurrences of the class_name in the entire hierarchy.

    parent: str = None
        Name of the parent node of the component in the hierarchy. At the first
        level, the parent of the nodes is "Home", an empty ComponentNode object.
        The nodes at every other level have parents that point to ComponentNode
        objects.

    links: list<dict> = None
        List of bidirectional links represented by the directed connections in
        the Drawflow canvas. A link is represented as followed:
            `{
                "from_port": str,
                "to_node_type": int,
                "to_port": str,
            }`,
        where:
        "from_port" is the name of the output connection of the current node,
        "to_node_type" is the type of node (Drawflow node "id") with the input
        connection, and
        "to_port" is the name of the input connection

    params: str = None
        Parameter values stored in the "data" field of the Drawflow nodes. A
        parameter is a dictionary that has been converted to an immutable
        string, since it does not serve a purpose in building the hierarchy.

    Public methods
    --------------
    Setters
    -------
    set_class_name(str)
    set_type(int)
    set_name(str)
    set_parent(str)
    set_links(list)
    set_params(str)

    Overloaded built-ins
    --------------------
    __eq__
    __hash__
    """

    def __init__(
        self,
        class_name: str = None,
        type: int = 0,
        name: str = None,
        parent: str = None,
        links: list = None,
        params: str = None,
    ) -> None:
        """
        Constructor for ComponentNode.

        Params
        ------
        class_name: str = None
        type: int = 0
        name: str = None
        parent: str = None
        links: list = None
        params: str = None

        Returns
        -------
        None
        """
        self.class_name = class_name
        self.type = type
        self.name = name
        self.parent = parent
        self.links = links
        self.params = params
        self.id = id(self)

    def set_class_name(self, class_name: str) -> None:
        """
        Sets class_name of object

        Params
        ------
        class_name: str = None

        Returns
        -------
        None
        """
        self.class_name = class_name

    def set_type(self, type: int) -> None:
        """
        Sets type of object

        Params
        ------
        type: int = 0

        Returns
        -------
        None
        """
        self.type = type

    def set_name(self, name: str) -> None:
        """
        Sets name of object

        Params
        ------
        name: str = None

        Returns
        -------
        None
        """
        self.name = name

    def set_parent(self, parent: str) -> None:
        """
        Sets parent name of object

        Params
        ------
        parent: str = None

        Returns
        -------
        None
        """
        self.parent = parent

    def set_links(self, links: list) -> None:
        """
        Sets links of object

        Params
        ------
        links: list = None

        Returns
        -------
        None
        """
        self.links = links

    def set_params(self, params: str) -> None:
        """
        Sets params of object

        Params
        ------
        params: str = None

        Returns
        -------
        None
        """
        self.params = params

    def __repr__(self) -> str:
        # debugging method
        return f"{self.class_name}{str(self.id)[-5:]}"

    def __eq__(self, other) -> bool:
        """Overloaded the equality operator for the object"""

        # if being compared to another ComponentNode object
        if isinstance(other, ComponentNode):
            # compare their class_name
            return self.class_name == other.class_name

        # if being compared to a string
        elif isinstance(other, str):
            # compare with the object's class_name
            return self.class_name == other

        # if being compared to an int
        elif isinstance(other, int):
            # compare with the object's id
            return self.id == other

        # if being compared to any other types
        raise TypeError(
            f"No methods implemented to check equality between 'ComponentNode' and {type(other)}"
        )

    def __hash__(self) -> int:
        """Overloaded the hash operator for the object"""
        return hash(self.id)
