import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from database.db_manager import DatabaseManager
from modules.evidence_graph.graph_builder import GraphBuilder

st.set_page_config(page_title="Evidence Graph", layout="wide")
st.title("Identity Linkage Graph")
st.caption("Visual representation of cross-platform identity clusters")

st.divider()

db = DatabaseManager()
comparisons = db.get_comparisons()

if not comparisons:
    st.info("Run an investigation first to generate graph data.")
else:
    with st.spinner("Rendering Evidence Graph..."):
        # Build the graph using the module
        G = GraphBuilder.build_graph(comparisons)
        
        if len(G.nodes) == 0:
            st.warning("No high-confidence linked accounts found to graph yet.")
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Create a nice layout
            pos = nx.spring_layout(G, k=0.8)
            
            # Draw the graph
            nx.draw(
                G, 
                pos, 
                with_labels=True, 
                node_color="#4F46E5", 
                node_size=3000, 
                font_color="white", 
                font_weight="bold", 
                edge_color="#9CA3AF",
                width=2
            )
            
            st.pyplot(fig)
            st.success("Graph rendered successfully.")