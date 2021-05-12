
import networkx as nx



def assignment_simple(candidate_dic , fitness_dic, G,reverse=False):

    edge_list= [(u,v,float(w)) for ((u,v),w) in fitness_dic.items()]
    if reverse:
        edge_list = [(u, v, float(1-w)) for ((u, v), w) in fitness_dic.items()]


    B = nx.Graph()
    B.add_weighted_edges_from(edge_list)
    result_list = list(nx.max_weight_matching(B))

    G_output = G.copy()
    att_dic = nx.get_node_attributes(G_output, 'att')
    for (u, v) in result_list:
        (c, p) = (u,v) if u in candidate_dic else (v,u)
        att_dic[p] = candidate_dic[c]

    nx.set_node_attributes(G_output, att_dic, 'att')

    return G_output, result_list