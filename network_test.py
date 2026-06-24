import json

from modules.network_analysis import (
    build_graph,
    draw_graph
)

with open(
    "data/profiles.json",
    "r",
    encoding="utf-8"
) as file:

    profiles = json.load(file)

G = build_graph(
    profiles
)

draw_graph(G)