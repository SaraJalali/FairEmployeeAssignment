import networkx as nx
import PreProcess as PP1
import UpdateWeights as UW


def assignment_max_weight(cands, pos, fitness, G, weight_probability=[1, 0, 0], version= 3):
    matched_1 =PP1.pre_assignment(cands,pos,fitness,G)
    if weight_probability[2]==1:
        matched_1.extend(PP1.support_group_assignment(cands, pos, fitness, G))
    bi_G = nx.Graph()
    bi_edges, edge_weights, l = UW.p_based_weight(pos, cands, fitness, G)
    bi_G.add_weighted_edges_from(bi_edges)
    final_matched = nx.max_weight_matching(bi_G)
    final_matched= list(final_matched)
    final_matched.extend(matched_1)
    final_matched = set(final_matched)

    return G, final_matched
