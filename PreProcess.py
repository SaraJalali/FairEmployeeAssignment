import networkx as nx



def pre_assignment(cands, pos, fitness,G):
    pos_dic={}
    cand_dic={}
    matched=[]
    unmatched=[]
    atts = nx.get_node_attributes(G, 'att')

    for (v,u), w in fitness.items():
        if u in pos_dic:
            pos_dic[u].append(v)
        else:
            pos_dic[u] = [v]
        if v in cand_dic:
            cand_dic[v].append(u)
        else:
            cand_dic[v] = [u]

    flag = True

    while flag:
        flag = False
        for k, v in pos_dic.items():
            if len(v) == 0:
                flag = True
                pos.remove(k)
                removed = []
                for (c, p) in fitness:
                    if p == k:
                        removed.append((c, p))
                for item in removed:
                    del fitness[item]
                unmatched.append(k)

                del pos_dic[k]
                break

            if len(v) == 1:
                flag = True
                atts[k] = cands[v[0]]
                nx.set_node_attributes(G, atts, 'att')
                matched.append((k, v[0]))
                pos.remove(k)
                del cands[v[0]]
                removed = []
                for (c, p) in fitness:
                    if c == v[0] or p == k:
                        removed.append((c, p))
                for item in removed:
                    del fitness[item]
                v = v[0]
                for u in cand_dic[v]:
                    pos_dic[u].remove(v)
                del pos_dic[k]
                del cand_dic[v]
                break




    if len(unmatched)>0:
        print('unmatched')
        print(unmatched)
    return matched

