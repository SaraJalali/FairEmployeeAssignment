'''
An edge exists between a candidate and a position if the candidate is qualified for that position.

'''
import sys

sys.path.insert(0, 'Score/')
sys.path.insert(0, '../InformationUnfairness/')
import networkx as nx
import random




def update_weights(G, pos, cands, fitness, final_matched=[], cands2=[], hungerian=False, weight_probability=[1, 0, 0],
                   version=2, aaa=1, local=True):
    '''

    :param G:
    :param pos:
    :param cands:
    :param fitness:
    :param method:
    :param final_matched:
    :param cands2:
    :param hungerian:
    :param weight_probability:
    : 0: diversity
    : 1: quality
    : 2: support
    method: 1:
    1: pareto optimal v1
    2: pareto optimal v2
    3: simple
    :return:
    '''
    weight_probability[2] = 0
    edge_weights_list = [{}, {}, {}]
    if weight_probability[0] > 0 and version != 3 and not local:
        edge_weights_1 = update_weights_assortativity(pos, cands, G, hungerian, fitness, final_matched=[],
                                                      cands2=cands2)
        edge_weights_list[0] = edge_weights_1
        if len(edge_weights_list[0]) > 1:
            m1 = max(list(edge_weights_list[0].values()))
            if m1 > 0:
                edge_weights_list[0] = {k: round(v / m1, 1) for k, v in edge_weights_list[0].items()}
    if version == 3 or local:
        edge_list, edge_dic = local_based_weight(pos, cands, fitness, G)
        edge_weights_list[0] = edge_dic

    if weight_probability[1] > 0:
        edge_weights_2 = update_weights_quality(pos, cands, fitness)
        edge_weights_list[1] = edge_weights_2
        if len(edge_weights_list[0]) > 1:
            m2 = max(list(edge_weights_list[1].values()))
            if m2 > 0:
                edge_weights_list[1] = {k: round(v / m2, 1) for k, v in edge_weights_list[1].items()}

    if version == 3:
        edge_list, edge_dic, l = p_based_weight(pos, cands, fitness, G)
    elif version == 2:
        edge_list, edge_dic, l = pareto_based_weight(pos, cands, weight_probability, edge_weights_list, hungerian,
                                                     final_matched, version=1, aaa=aaa)
    elif version == 1:
        edge_list, edge_dic, l = percent_based_weight(pos, cands, hungerian, weight_probability, edge_weights_list)
    elif version == 4:
        edge_list, edge_dic, l = pareto_based_weight(pos, cands, weight_probability, edge_weights_list, hungerian,
                                                     final_matched, version=3, aaa=aaa)

    return edge_list, edge_dic, l

def update_weights_simple(pos, cands, fitness):
    edges = []
    l = {}
    for u in pos:
        for v in cands:
            if (v, u) in fitness:
                edges.append((u, v, 1))
        l.update({u: 1})
    for v in cands:
        l.update({v: 0})
    ##
    edge_weights = {}
    for (u, v, s) in edges:
        edge_weights.update({(u, v): s})

    return edges, edge_weights, l

def update_weights_quality(pos, cands, fitness):
    edges = []
    # l = {}
    for u in pos:
        for v in cands:
            if (v, u) in fitness:
                edges.append((u, v, fitness[(v, u)]))
    edge_weights = {}
    for (u, v, s) in edges:
        edge_weights.update({(u, v): s})

    return edge_weights

def update_weights_assortativity(pos, cands, G, hungerian, fitness, final_matched=[], cands2=[]):
    if cands2 == []: cands2 = cands
    asst = nx.attribute_assortativity_coefficient(G, 'att')
    if asst < 0:
        method = 2
    else:
        method = 1
    if cands2 == []: cands2 = cands
    gender = nx.get_node_attributes(G, 'att')
    scores = {}
    for u in pos:
        neigh = G[u]
        m = 0
        f = 0
        for v in neigh:
            if gender[v] == 'male':
                m += 1
            elif gender[v] == 'female':
                f += 1
        scores.update({u: ((m, f))})

    edges = []
    for u in pos:
        (m, f) = scores[u]

        for v in cands:
            if (v, u) in fitness:  # fitness[(v, u)] == 1:
                if (cands2[v] == 'male' and method == 1) or (cands2[v] == 'female' and method == 2):
                    if f != 0 or hungerian:
                        edges.append((u, v, f))
                elif (cands2[v] == 'male' and method == 2) or (cands2[v] == 'female' and method == 1):
                    if m != 0 or hungerian:
                        edges.append((u, v, m))

    edge_weights = {}
    for (u, v, s) in edges:
        edge_weights.update({(u, v): s})
    return edge_weights

def pareto_based_weight(pos, cands, weight_probability, edge_weights_list, hungarian=False, final_matched=[], version=1,
                        aaa=1):
    n = 0
    x = 0
    i = -1
    for item in weight_probability:
        i += 1
        if item > 0:
            n += 1
        else:
            x = i

    weights_list = [[], [], []]
    edge_list = []

    for u in pos:
        for v in cands:
            flag = False
            w = [0, 0, 0]
            edge = (u, v)
            if weight_probability[0] > 0 and edge in edge_weights_list[0]:
                w[0] = edge_weights_list[0][edge]
                flag = True
            if weight_probability[1] > 0 and edge in edge_weights_list[1]:
                w[1] = edge_weights_list[1][edge]
                flag = True
            if weight_probability[2] > 0 and edge in edge_weights_list[2]:
                w[2] = edge_weights_list[2][edge]
                flag = True
            if flag:
                edge_list.append((u, v))
                if weight_probability[0] > 0:
                    weights_list[0].append(w[0])
                if weight_probability[1] > 0:
                    weights_list[1].append(w[1])
                if weight_probability[2] > 0:
                    weights_list[2].append(w[2])

    if n == 3:
        ranked_list = fast_non_dominated_sort2(weights_list[0], weights_list[1], weights_list[2])
    else:
        weights_list.remove(weights_list[x])
        ranked_list = fast_non_dominated_sort(weights_list[0], weights_list[1])

    output_edge_list = []
    output_edge_dic = {}
    if version == 1:
        k = len(ranked_list) + 1
        while len(ranked_list) > 0:
            k -= 1
            ll1 = ranked_list.pop(0)
            for i in ll1:
                (u, v) = edge_list[i]
                output_edge_list.append((u, v, k))
                output_edge_dic[(u, v)] = k

    elif version == 2:
        ll1 = ranked_list[0]
        for i in ll1:
            (u, v) = edge_list[i]
            output_edge_list.append((u, v, 1))
            output_edge_dic[(u, v)] = 1

    elif version == 3:
        k = len(ranked_list) + 1
        j = 0
        while len(ranked_list) > 0:
            j += 1
            k -= 1
            ll1 = ranked_list.pop(0)
            for i in ll1:
                (u, v) = edge_list[i]
                output_edge_list.append((u, v, k))
                output_edge_dic[(u, v)] = k
            if j == aaa:
                break

    l = {}
    if hungarian:
        for u in pos:
            l[u] = 0
            for v in cands:
                if (u, v) in output_edge_dic:
                    w = output_edge_dic[(u, v)]
                    if hungarian and ((u, v) in final_matched or (v, u) in final_matched):
                        l[u] = w
                        break
                    else:
                        l[u] = max(w, l[u])
        for v in cands:
            l[v] = 0

    return output_edge_list, output_edge_dic, l

def percent_based_weight(pos, cands, hungerian, weight_probability, edge_weights_list):
    l = {}
    edge_list = []
    edge_dic = {}
    m = int(weight_probability[0] * len(pos))
    sample = set(random.sample(pos, m))

    for u in pos:
        l[u] = 0
        for v in cands:
            flag = False
            w = 0
            edge = (u, v)
            if u in sample:
                w = edge_weights_list[0][edge]
                flag = True
            else:
                w = edge_weights_list[1][edge]
                flag = True
            if w > 0 or (hungerian and flag):
                if w < 0:
                    w = 0.1
                edge_dic[(u, v)] = w
                edge_list.append((u, v, w))
                if hungerian:
                    # if flag1:
                    l[u] = max(w, l[u])
                    # if hungerian and ((u, v) in final_matched or (v, u) in final_matched):
                    #    l[u] = w
                    #   flag1 = False
    if hungerian:
        for v in cands:
            l.update({v: 0})
    return edge_list, edge_dic, l

def p_based_weight(pos, cands, fitness, G):
    l = {}
    edge_list = []
    edge_dic = {}
    gender = nx.get_node_attributes(G, 'att')
    for u in pos:
        neighs = G[u]
        m = 0
        f = 0
        for vv in neighs:
            if gender[vv] == 'male':
                m += 1
            else:
                f += 1
        for v in cands:
            if (v, u) in fitness:
                w = fitness[(v, u)]
                if m > f:
                    if cands[v] == 'female':
                        w += 1
                elif m < f:
                    if cands[v] == 'male':
                        w += 1
                edge_dic[(u, v)] = round(w, 2)
                edge_list.append((u, v, round(w, 2)))

    return edge_list, edge_dic, l

def local_based_weight(pos, cands, fitness, G):
    edge_list = []
    edge_dic = {}
    gender = nx.get_node_attributes(G, 'att')
    for u in pos:
        neighs = G[u]
        m = 0
        f = 0
        for vv in neighs:
            if gender[vv] == 'male':
                m += 1
            else:
                f += 1
        for v in cands:
            if (v, u) in fitness:
                w = 0
                if m > f:
                    if cands[v] == 'female':
                        w += 1
                elif m < f:
                    if cands[v] == 'male':
                        w += 1
                edge_dic[(u, v)] = round(w, 2)
                edge_list.append((u, v, round(w, 2)))

    return edge_list, edge_dic

#Function to carry out NSGA-II's fast non dominated sort
def fast_non_dominated_sort(values1, values2):

    last=set()
    S=[[] for i in range(0,len(values1))]
    front = [[]]
    n=[0 for i in range(0,len(values1))]
    rank = [0 for i in range(0, len(values1))]

    for p in range(0,len(values1)):
        if p not in last:
            S[p] = []
            n[p] = 0
            for q in range(0, len(values1)):
                if q not in last:
                    if (values1[p] > values1[q] and values2[p] > values2[q]) or (
                            values1[p] >= values1[q] and values2[p] > values2[q]) or (
                            values1[p] > values1[q] and values2[p] >= values2[q]):
                        if q not in S[p]:
                            S[p].append(q)
                    elif (values1[q] > values1[p] and values2[q] > values2[p]) or (
                            values1[q] >= values1[p] and values2[q] > values2[p]) or (
                            values1[q] > values1[p] and values2[q] >= values2[p]):
                        n[p] = n[p] + 1

            if n[p] == 0:
                rank[p] = 0
                if p not in front[0]:
                    front[0].append(p)


    i = 0
    while(front[i] != []):
        Q=[]
        for p in front[i]:
            for q in S[p]:
                n[q] =n[q] - 1
                if( n[q]==0):
                    rank[q]=i+1
                    if q not in Q:
                        Q.append(q)
        i = i+1
        front.append(Q)

    del front[len(front)-1]
    if len(last)>0:
        front.append(list(last))
    return front


#Function to carry out NSGA-II's fast non dominated sort
def fast_non_dominated_sort2(values1, values2, values3=[0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,1,1,1,0,0]):

    S=[[] for i in range(0,len(values1))]
    SS=[set() for i in range(0,len(values1))]
    front = [[]]
    rank = [0 for i in range(0, len(values1))]
    cands= set(range(len(values1)))

    for p in range(0,len(values1)):
        S_p = [set(),set(),set()]
        for q in range(0, len(values1)):
            if values1[q] > values1[p]:
                S_p[0].add(q)
                SS[q].add(p)
            elif values1[q] == values1[p] and ((values2[q] > values2[p] and values3[q] > values3[p]) or (values2[q] == values2[p] and values3[q] > values3[p]) or (values2[q] > values2[p] and values3[q] == values3[p])):
                S_p[0].add(q)
                SS[q].add(p)
            if values2[q] > values2[p]:
                S_p[1].add(q)
                SS[q].add(p)
            elif values2[q] == values2[p] and ((values1[q] > values1[p] and values3[q] > values3[p]) or (values1[q] == values1[p] and values3[q] > values3[p]) or (values1[q] > values1[p] and values3[q] == values3[p])):
                S_p[1].add(q)
                SS[q].add(p)
            if values3[q] > values3[p]:
                S_p[2].add(q)
                SS[q].add(p)
            elif values3[q] == values3[p] and ((values2[q] > values2[p] and values1[q] > values1[p]) or (values2[q] == values2[p] and values1[q] > values1[p]) or (values2[q] > values2[p] and values1[q] == values1[p])):
                S_p[2].add(q)
                SS[q].add(p)
        S[p]=S_p
        if len(S_p[0])==0 or len(S_p[1])==0 or len(S_p[2])==0:
            front[0].append(p)
            cands.remove(p)


    i = 0
    while(front[i] != []):
        Q=[]
        for p in front[i]:
            for q in SS[p]:
                if q in cands:
                    for item in S[q]:
                        if p in item:
                            item.remove(p)
                            if len(item)==0:
                                cands.remove(q)
                                Q.append(q)
                                break
        i = i+1
        front.append(Q)

    del front[len(front)-1]

    return front

