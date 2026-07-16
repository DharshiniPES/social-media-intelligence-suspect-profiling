import networkx as nx

class GraphBuilder:
    @staticmethod
    def build_graph(comparisons):
        G = nx.Graph()
        for row in comparisons:
            # Add nodes and edges if the link is verified (linked == 1)
            if row[13] == 1: 
                G.add_edge(row[1], row[2], weight=row[11])
        return G