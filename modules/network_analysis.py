import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network


def build_graph(profiles):

    G = nx.Graph()

    for profile in profiles:

        G.add_node(
            profile["id"]
        )

    return G


def add_link(

    G,

    profile1_id,
    profile2_id,

    fusion_score

):

    G.add_edge(

        profile1_id,

        profile2_id,

        weight=round(
            fusion_score,
            3
        )
    )


def draw_graph(G):

    pos = nx.spring_layout(G)

    nx.draw(
        G,
        pos,
        with_labels=True
    )

    labels = nx.get_edge_attributes(
        G,
        "weight"
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=labels
    )

    plt.savefig(
        "network_graph.png"
    )

    plt.close()


def detect_communities(G):

    communities = list(
        nx.connected_components(G)
    )

    return communities


def calculate_centrality(G):

    centrality = nx.degree_centrality(
        G
    )

    ranking = sorted(

        centrality.items(),

        key=lambda x: x[1],

        reverse=True

    )

    return ranking
def generate_interactive_graph(G):

    net = Network(

        height="750px",

        width="100%",

        bgcolor="#222222",

        font_color="white"

    )

    net.from_nx(G)

    net.show(
        "network_graph.html",
        notebook=False
    )