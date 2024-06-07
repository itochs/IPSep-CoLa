import networkx as nx


def indicate_graph(graph: nx.Graph) -> nx.Graph:
    g = nx.Graph()
    node_indices = dict()
    for i, node in enumerate(graph.nodes):
        node_indices[node] = i
        g.add_node(i)

    for v, u in graph.edges:
        edge_data = graph.get_edge_data(v, u)
        g.add_edge(node_indices[v], node_indices[u], **edge_data)

    return g


def save_json(graph: nx.Graph, name):
    graph = nx.DiGraph(graph.edges)
    nodes = [{"id": i, "name": i} for i in graph.nodes]
    links = [{"source": i, "target": j} for i, j in graph.edges]

    edges = list(graph.edges.data())
    constraints = []

    have_weight_edges = [edge for edge in edges if edge[2].get("weight")]
    gap_ave = (
        sum([d["weight"] for i, j, d in have_weight_edges]) / len(have_weight_edges)
        if len(have_weight_edges)
        else 20
    )

    node_comp = dict()
    comps = list(nx.strongly_connected_components(graph))
    for i, comp in enumerate(comps):
        for node in comp:
            node_comp[node] = i

    constraints = []
    for i, j in graph.edges:
        u = node_comp[i]
        v = node_comp[j]
        if u != v:
            constraints.append(
                {
                    "axis": "y",
                    "left": i,
                    "right": j,
                    "gap": gap_ave,
                }
            )

    data = {
        "nodes": nodes,
        "links": links,
        "constraints": constraints,
    }
    import json

    json.dump(data, open(f"{name}.json", "w"), indent=2)


save_json(indicate_graph(nx.les_miserables_graph()), "les_miserables_graph")
save_json(indicate_graph(nx.florentine_families_graph()), "florentine_families_graph")
save_json(indicate_graph(nx.davis_southern_women_graph()), "davis_southern_women_graph")
save_json(indicate_graph(nx.karate_club_graph()), "karate_club_graph")
