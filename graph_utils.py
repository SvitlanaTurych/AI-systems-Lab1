import random
from collections import deque

import networkx as nx


def generate_tree_edges(n, seed=42, min_branches=5):
    rnd = random.Random(seed)
    nodes = list(range(1, n))
    rnd.shuffle(nodes)

    min_branches = min(min_branches, len(nodes))
    branches = nodes[:min_branches]
    rest = nodes[min_branches:]

    edges = []
    available = []
    for b in branches:
        edges.append((0, b))
        available.append(b)

    for node in rest:
        parent = rnd.choice(available)
        edges.append((parent, node))
        available.append(node)

    return edges


def generate_explicit_graph(n, seed=42):
    tree_edges = generate_tree_edges(n, seed=seed)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(tree_edges)

    rnd = random.Random(seed + 1)
    extra_edges = max(6, n // 3)
    nodes = list(G.nodes())
    added, attempts = 0, 0
    while added < extra_edges and attempts < extra_edges * 25:
        u, v = rnd.sample(nodes, 2)
        if u != v and not G.has_edge(u, v):
            G.add_edge(u, v)
            added += 1
        attempts += 1

    return G, tree_edges


def generate_tree_graph(n, seed=42):
    tree_edges = generate_tree_edges(n, seed=seed)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(tree_edges)
    return G, tree_edges


def make_directed(G, tree_edges, seed=42):
    rnd = random.Random(seed + 2)
    tree_set = set(tree_edges) | {(v, u) for (u, v) in tree_edges}
    D = nx.DiGraph()
    D.add_nodes_from(G.nodes())

    for u, v in G.edges():
        if (u, v) in tree_set:
            if (u, v) in tree_edges:
                D.add_edge(u, v)
            else:
                D.add_edge(v, u)
        else:
            if rnd.random() < 0.5:
                D.add_edge(u, v)
            else:
                D.add_edge(v, u)
    return D


def layered_positions(G, root=0):
    UG = G.to_undirected() if G.is_directed() else G
    if root not in UG.nodes():
        root = next(iter(UG.nodes()))

    levels = {root: 0}
    order = [root]
    visited = {root}
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for nb in sorted(UG.neighbors(node)):
            if nb not in visited:
                visited.add(nb)
                levels[nb] = levels[node] + 1
                order.append(nb)
                queue.append(nb)

    for node in UG.nodes():
        if node not in levels:
            levels[node] = 0
            order.append(node)

    level_nodes = {}
    for node in order:
        level_nodes.setdefault(levels[node], []).append(node)

    pos = {}
    for level, nodes_in_level in level_nodes.items():
        count = len(nodes_in_level)
        for i, node in enumerate(sorted(nodes_in_level)):
            x = (i - (count - 1) / 2) * 1.6
            y = -level * 1.3
            pos[node] = (x, y)
    return pos