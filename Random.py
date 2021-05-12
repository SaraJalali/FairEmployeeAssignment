import networkx as nx
import random
import UpdateWeights as UW



def assignment_random(cands, pos, fitness, G):

    bi_edges, edge_weights, l = UW.update_weights_simple(pos, cands, fitness)
    bi_G = nx.Graph()
    bi_edges = [(u, v, w) for (u, v, w) in bi_edges if w != 0]
    bi_G.add_weighted_edges_from(bi_edges)
    final_matched = nx.max_weight_matching(bi_G)
    gender=nx.get_node_attributes(G, 'att')
    for (u, v) in final_matched:
        if u in pos:
            gender.update({u: cands[v]})
        else:
            gender.update({v: cands[u]})

    nx.set_node_attributes(G, gender, 'att')
    return G, final_matched