import networkx as nx
import PreProcess as PP
import Hungarian as Hu
import UpdateWeights as UW





def select_positions(G, positions, candidates, fitness, weight_probability, aaa, version=4, local=False):
    bi_edges, edge_weights, l = UW.update_weights(G, positions, candidates, fitness, [],
                                                  weight_probability=weight_probability, version=version,
                                                  cands2=[], aaa=aaa, local=local)
    output=set()
    for (u,v) in edge_weights:
        if u in positions:
            output.add(u)
        else:
            output.add(u)

    bi_G = nx.Graph()
    bi_edges = [(u, v, w) for (u, v, w) in bi_edges if w != 0]
    bi_G.add_weighted_edges_from(bi_edges)
    final_matched = nx.max_weight_matching(bi_G)

    return list(output), final_matched



def assignment_fairea(cands, pos, fitness, G, weight_probability=[1, 0, 0], version= 4,kk=0, local=False):

    matched_1 = PP.pre_assignment(cands, pos, fitness, G)
    if weight_probability[2] == 1:
        if kk !=0:
            matched_1.extend(PP.support_group_assignment(cands, pos, fitness, G, p=kk))
        else:
            matched_1.extend(PP.support_group_assignment(cands, pos, fitness, G))
    i=-1
    while True:
        i+=1
        positions, final_matched = select_positions(G, pos, cands, fitness, weight_probability, i + 1, version=version, local=local)
        if len( final_matched) < len(positions):
            final_matched, G = Hu.Hungarian(cands, positions, final_matched, G, fitness,
                            weight_probability=weight_probability, version=2,local=local)
            if final_matched ==[]:
                return [], []

        if len(final_matched) == len(pos):
            break
    final_matched = list(final_matched)
    final_matched.extend(matched_1)

    return G, set(final_matched)

