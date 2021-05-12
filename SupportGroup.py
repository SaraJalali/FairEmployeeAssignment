
import networkx as nx
from community import community_louvain
from collections import defaultdict
import math
import PreProcess as PP



def support_group_assignment(cands, pos, fitness,G, p=0.2):
    att_dic = nx.get_node_attributes(G, 'att')

    communities = community_louvain.best_partition(G)
    communities_dic = defaultdict(list)
    for key, value in sorted(communities.items()):
        communities_dic[value].append(key)

    final_matched=[]

    for k , v in communities_dic.items():
        count=0
        male=0
        female=0
        cand =set()
        for u in v:
            gen = att_dic[u]
            count+=1
            if gen=='male': male +=1
            elif gen=='female': female+=1
            else: cand.add(u)

        if p ==2:
            n=2
        else:
            n = math.ceil(p*count)
        if len(cand)>0:
            if male<n:
                m = n-male
                matched = match('male', fitness, cand, cands, pos, m,G)
                final_matched.extend(matched)
            if female<n:
                m = n-female
                matched =match('female', fitness, cand, cands, pos, m, G)
                final_matched.extend(matched)

    return final_matched


def match(gen, fitness, cand, cands, pos, m ,G):
    final_matched =[]
    gender = nx.get_node_attributes(G, 'att')
    edges = []
    bi_G = nx.Graph()
    for (u, v), w in fitness.items():
        if v in cand and cands[u] == gen:
            edges.append((u, v, w))
    bi_G.add_weighted_edges_from(edges)
    matched = nx.max_weight_matching(bi_G)
    l = {}
    for (u, v) in matched:
        if u in cand:
            temp = u
            u = v
            v = temp
        l[(u, v)] = fitness[(u, v)]
    l = {k: v for k, v in sorted(l.items(), key=lambda item: item[1], reverse=True)}
    l = list(l.keys())

    i,j = 0, 0
    while j<=len(l)-1 and i < m:
        (u,v) = l[j]
        j+=1
        if u in cands:
            temp = u
            u = v
            v = temp
        if u in pos and v in cands:
            final_matched.append((u,v))
            i+=1
            gender[u] = gen
            pos.remove(u)
            del cands[v]
            remove_list = []
            for (a, b) in fitness.keys():
                if a == v or b == u:
                    remove_list.append((a, b))
            for item in remove_list:
                del fitness[item]
            nx.set_node_attributes(G, gender, 'att')
            final_matched.extend(PP.pre_assignment(cands, pos, fitness, G))

    return final_matched

