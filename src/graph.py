import collections
import functools


class GraphError(Exception):
    pass

class NodeError(GraphError):
    pass

class EdgeError(GraphError):
    pass


class Node(collections.UserDict):

    def __init__(self, key, value=None, blob=None):
        self.data = dict()
        self._k = key
        self.v = value
        self.blob = blob

    def __hash__(self):
        return hash(self._k)

    def __str__(self):
        if self.v is None:
            return f"Node({self.k!r})"
        return f"Node({self.k!r}, {self.v!r})"

    def __repr__(self):
        return f"Node({self.k!r}, {self.v!r}, {self.blob!r})"

    @property
    def k(self):
        return self._k

    def adde(self, node, dist):
        self[node] = dist

    # def contract(self, other):
    #     self_other = self[other] if other in self else None
    #     other_self = other[self] if self in other else None
    #     for k, v in other.items():
    #         # Update edge (self, k)
    #         if self_other is None:
    #             self[k] = v
    #         elif k in self:
    #             self[k] = min(self_other + v, self[k])
    #         else:
    #             self[k] = self_other + v
    #         # Update edge (k, self), if exists
    #         if self in k:
    #             if other in k:  # Otherwise, no alternate path
    #                 k_other = k[other]
    #                 if other_self is None:
    #                     k[self] = min(k_other, k[self])
    #                 else:
    #                     k[self] = min(k_other + other_self, k[self])

    def cleave(self, new_key, dist, value=None, blob=None):
        if new_key == self._k:
            raise KeyError(f"Duplicate node key: {new_key}")
        new_node = Node(new_key, value, blob)
        new_node.update(self)
        self.data = {new_node: dist}
        return new_node

    def basic_search(self, queue_class, select_func, append_func, dest=None, max_depth=None):
        distances = {self: 0}
        parents = {self: None}
        queue = queue_class([self])
        i = 1
        found = False
        while queue:
            visit_node = select_func(queue)
            for neighbor in visit_node:
                if neighbor in distances:
                    continue
                distances[neighbor] = distances[visit_node] + 1
                if neighbor is dest:
                    found = True
                    break
                parents[neighbor] = visit_node
                append_func(queue, neighbor)
            if found:
                break
            if max_depth is not None and i > max_depth:
                break
        return distances, parents

    bfs = functools.partialmethod(
        basic_search,
        collections.deque,
        lambda q: q.popleft(),
        lambda q, x: q.append(x),
    )
    dfs = functools.partialmethod(
        basic_search,
        collections.deque,
        lambda q: q.popleft(),
        lambda q, x: q.appendleft(x),
    )



class _Decorators(object):

    @staticmethod
    def check_key(func):
        @functools.wraps(func)
        def checked_func(self, key, *args, **kwargs):
            if not self.has(key):
                raise KeyError(f"Node {key} does not exist")
            return func(self, key, *args, **kwargs)
        return checked_func
            
    @staticmethod
    def check_key_pair(func):
        @functools.wraps(func)
        def checked_func(self, key1, key2, *args, **kwargs):
            if not self.has(key1):
                raise KeyError(f"Node {key1} does not exist")
            if not self.has(key2):
                raise KeyError(f"Node {key2} does not exist")
            return func(self, key1, key2, *args, **kwargs)
        return checked_func

    @staticmethod
    class VertexOrEdge(object):
        def __init__(self, v_func, e_func):
            self.v_func = v_func
            self.e_func = e_func
        def __call__(self, func):
            v_func = self.v_func
            e_func = self.e_func
            @functools.wraps(func)
            def vertex_edge_func(this, key, *args, **kwargs):
                if isinstance(key, tuple):
                    if len(key) != 2:
                        raise TypeError(f"An edge must consist of exactly two vertices: {key}")
                    return e_func(this, *key, *args, **kwargs)
                return v_func(this, key, *args, **kwargs)
            return vertex_edge_func


class AbstractGraph(object):
    pass

class BaseGraph(AbstractGraph):

    data = None

    def __str__(self):
        adj_list = dict()
        for k, n in self.data.items():
            adj_list[k] = {n.k: d for n, d in n.items()}
        return str(adj_list)

    def __repr__(self):
        class_name = self.__class__.__name__
        dict_class = self.data.__class__.__name__
        edges = []
        for key, node in self.data.items():
            for neighbor, dist in node.items():
                edges.append((key, neighbor.k, dist))
        return f"{class_name}({edges=!r}, {dict_class=!s})"


class Digraph(BaseGraph, collections.UserDict):

    def __init__(self, edges=None, dict_class=dict):
        self.data = dict_class()
        if edges is not None:
            self._init_edges(edges)

    def _init_edges(self, edges):
        for e in edges:
            if len(e) == 2:
                key1, key2 = e
                dist = 1
            elif len(e) == 3:
                key1, key2, dist = e
            else:
                raise ValueError(f"Edge description must be (key1, key2) or "
                                  "(key1, key2, dist): {e}")
            self.sete(key1, key2, dist)

    # Existence checks.

    def has(self, key):
        return key in self.data

    @_Decorators.check_key
    def getv(self, key):
        return self.data[key]
    _getv = getv.__wrapped__

    @_Decorators.check_key_pair
    def isadj(self, key1, key2):
        return self._getv(key2) in self._getv(key1)
    _isadj = isadj.__wrapped__

    @_Decorators.VertexOrEdge(has, isadj)
    def __contains__(self, item):
        pass

    # Getters.

    def nodes(self):
        return self.data.values()

    @_Decorators.check_key
    def neigh(self, key):
        return self._getv(key).keys()
    _neigh = neigh.__wrapped__

    @_Decorators.check_key_pair
    def gete(self, key1, key2):
        if self._isadj(key1, key2):
            return self._getv(key1)[self._getv(key2)]
        raise KeyError(f"Edge ({key1}, {key2}) does not exist")
    _gete = gete.__wrapped__

    @_Decorators.VertexOrEdge(getv, gete)
    def __getitem__(self, key):
        pass

    # Adders.

    def _addv(self, key, value):
        new_node = Node(key, value)
        self.data[key] = new_node
        return new_node

    def _setv(self, key, value):
        self._getv(key).v = value

    def addv(self, key, value=None):
        if self.has(key):
            if value is None:
                raise NodeError(f"Node {key} already exists")
            self._setv(key, value)
        self._addv(key, value)

    def setv(self, key, value):
        if self.has(key):
            self._setv(key, value)
        self._addv(key, value)

    def _adde(self, key1, key2, dist):
        self._getv(key1).adde(self._getv(key2), dist)

    def _sete(self, key1, key2, dist):
        self._getv(key1)[self._getv[key2]] = dist

    def _check_adde(self, key1, key2):
        if self._isadj(key1, key2):
            raise EdgeError(f"Edge ({key1}, {key2} already exists")

    def adde(self, key1, key2, dist=1):
        if not self.has(key1):
            self._addv(key1, None)
        if not self.has(key2):
            self._addv(key2, None)
        self._check_adde(key1, key2)
        self._adde(key1, key2, dist)

    def sete(self, key1, key2, dist):
        if not self.has(key1):
            self._addv(key1, None)
        if not self.has(key2):
            self._addv(key2, None)
        if self._isadj(key1, key2):
            self._sete(key1, key2, dist)
            return
        self._adde(key1, key2, dist)
 
    @_Decorators.VertexOrEdge(setv, sete)
    def __setitem__(self, key, item):
        pass

    # Deleters.

    @_Decorators.check_key
    def delv(self, key):
        del_node = self._getv(key)
        del self.data[key]
        for node in self.data.items():
            if del_node in node:
                del node[del_node]
    _delv = delv.__wrapped__

    @_Decorators.check_key_pair
    def dele(self, key1, key2):
        if not self._isadj(key1, key2):
            raise KeyError(f"Edge ({key1}, {key2}) does not exist")
        del self._getv(key1)[self._getv(key2)]
    _dele = dele.__wrapped__
    
    @_Decorators.VertexOrEdge(delv, dele)
    def __delitem__(self, key):
        pass


class Graph(Digraph):

    def adde(self, key1, key2, dist=1):
        if not self.has(key1):
            self._addv(key1, None)
        if not self.has(key2):
            self._addv(key2, None)
        self._check_adde(key1, key2)
        self._adde(key1, key2, dist)
        self._adde(key2, key1, dist)

    def sete(self, key1, key2, dist):
        if not self.has(key1):
            self._addv(key1, None)
        if not self.has(key2):
            self._addv(key2, None)
        if self._isadj(key1, key2):
            self._sete(key1, key2, dist)
            self._sete(key2, key1, dist)
            return
        self._adde(key1, key2, dist)
        self._adde(key2, key1, dist)

    @_Decorators.check_key_pair
    def dele(self, key1, key2):
        if not self._isadj(key1, key2):
            raise KeyError(f"Edge ({key1}, {key2}) does not exist")
        del self._getv(key1)[self._getv(key2)]
        del self._getv(key2)[self._getv(key1)]
    _dele = dele.__wrapped__
 