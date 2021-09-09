#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Resolves Drawflow connections between nodes to represent one-to-one
relationships between SST Links.

The class is a helper class and builds on an initialized ComponentTree object.
The connections between the nodes must be resolved for the Python configuration
file. Without the SST Links, the configuration file would instantiate SST
Components that do not have any functionality.
"""

from .componentnode import ComponentNode


class HierarchyResolver:
    """
    Helper class to build SST Links from the ComponentNodes in an initialized
    ComponentTree object.

    Attributes
    ----------
    __tree: dict<ComponentNode, list<dict<ComponentNode>, list...>>
        the tree generated from a ComponentTree object.

    __hierarchy_links: list<tuple<str>>
        list of SST Links generated from the ComponentTree object's tree.

    Methods
    -------
    Public methods
    --------------
    get_path_to_root(ComponentNode, list)
    get_parent(ComponentNode)
    get_sibling_subtree(ComponentNode, int)
    resolve_from_port(ComponentNode, str)
    resolve_to_port()
    parse_connection(str)
    resolve_hierarchy()
    get_links()

    Private methods
    ---------------
    __resolve_port(list, dict)
    __find_node_by_attr(dict, str, int)
    __get_parent(ComponentNode, dict)
    __resolve_hierarchy(dict)
    """

    def __init__(self, component_tree: dict) -> None:
        """
        Constructor for HierarchyResolver

        Params
        ------
        component_tree: dict<ComponentNode, list<dict<ComponentNode>, list...>>
            the tree generated from a ComponentTree object.

        Returns
        -------
        None
        """
        self.__tree = component_tree
        self.__hierarchy_links = []

    def __find_node_by_attr(self, subtree: dict, attr: str, data: int) -> ComponentNode:
        """
        Constructor for HierarchyResolver

        Params
        ------
        subtree: dict

        attr: str


        data: int

        Returns
        -------
        None
        """
        for key, value in subtree.items():
            if getattr(key, attr) == data:
                return key, subtree

            for node in value:
                found = self.__find_node_by_attr(node, attr, data)
                if found:
                    return found

    def get_path_to_root(self, node: ComponentNode, node_types_list: list) -> list:

        node_types_list.append(node.type)

        parent = self.get_parent(node)
        node_types_list.append(parent.type)

        while parent.type:
            parent = self.get_parent(parent)
            node_types_list.append(parent.type)

        return node_types_list

    def get_parent(self, node: ComponentNode) -> ComponentNode:

        return self.__get_parent(node, self.__tree)

    def __get_parent(self, node: ComponentNode, subtree: dict) -> ComponentNode:

        for key, value in subtree.items():
            for k in value:

                if node.id == next(iter(k)).id:
                    return key

                parent = self.__get_parent(node, k)
                if parent:
                    return parent

    def get_sibling_subtree(self, node: ComponentNode, sibling_node_type: int) -> dict:

        current_node, _ = self.__find_node_by_attr(self.__tree, "id", node.id)
        current_parent = self.get_parent(current_node)
        current_parent, subtree = self.__find_node_by_attr(
            self.__tree, "id", current_parent.id
        )
        sibling_node = self.__find_node_by_attr(subtree, "type", sibling_node_type)
        while not sibling_node:
            current_parent = self.get_parent(current_parent)
            current_parent, subtree = self.__find_node_by_attr(
                self.__tree, "id", current_parent.id
            )
            sibling_node = self.__find_node_by_attr(subtree, "type", sibling_node_type)
        else:
            sibling_node, subtree = sibling_node

        return subtree

    def __resolve_port(self, node_types_list: list, subtree: dict) -> ComponentNode:

        while node_types_list:
            node, subtree = self.__find_node_by_attr(
                subtree, "type", node_types_list.pop()
            )
            if not subtree[node]:
                return node

    def resolve_from_port(self, node: ComponentNode, connection: str) -> tuple:

        connection_name, node_types_list = self.parse_connection(connection)

        if not node_types_list:
            return node, connection_name

        node_types_list = self.get_path_to_root(node, node_types_list)

        subtree = self.__tree
        return self.__resolve_port(node_types_list, subtree), connection_name

    def resolve_to_port(
        self, node: ComponentNode, to_node_type: int, connection: str
    ) -> tuple:

        subtree = self.get_sibling_subtree(node, to_node_type)
        connection_name, node_types_list = self.parse_connection(connection)
        if not node_types_list:
            return (
                self.__find_node_by_attr(subtree, "type", to_node_type)[0],
                connection_name,
            )

        return self.__resolve_port(node_types_list, subtree), connection_name

    def parse_connection(self, connection: str) -> tuple:
        """Parse connection string representing SST Links

        The connection string is split on the node delimiter. The first node of the
        list is the name of the connection, and the rest of the list is its nested types
        """
        connection_list = connection.split("#")
        return connection_list[0], [int(i) for i in connection_list[1:]]

    def resolve_hierarchy(self) -> None:

        self.__resolve_hierarchy(self.__tree)

    def __resolve_hierarchy(self, subtree: dict) -> None:

        for value in subtree.values():
            if not value:
                return
            for node in value:
                k = next(iter(node))
                for link in k.links:

                    from_node, from_port = self.resolve_from_port(k, link["from_port"])
                    to_node, to_port = self.resolve_to_port(
                        k,
                        link["to_node_type"],
                        link["to_port"],
                    )

                    self.__hierarchy_links.append(
                        (*(from_node, from_port), *(to_node, to_port))
                    )
                self.__resolve_hierarchy(node)

    def get_links(self) -> list:

        return self.__hierarchy_links
