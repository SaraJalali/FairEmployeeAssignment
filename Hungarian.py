'''
This implementation is based on this article:
https://www.cse.ust.hk/~golin/COMP572/Notes/Matching.pdf

'''


import networkx as nx
import UpdateWeights as UW



def pre_process(cands, pos, final_matched, G, fitness, cands2=[], weight_probability=[1,0,0], version= 3, G_El=[],local=False):
    if cands2 == []: cands2 = cands

    edges, edge_dic, l = UW.update_weights(G, pos, cands, fitness, final_matched, hungerian=True,
                                            cands2=cands2,weight_probability=weight_probability, version=version,local=local)

    G_El = update_G_EL(edges, l)
    return l, G_El, edge_dic, edges

def update_G_EL(edges, l):
    G_El = nx.Graph()
    El = []
    for (u, v, s) in edges:
        if round(l[u] + l[v],2) <= round(s,2):
            El.append((u, v, s))
    G_El.add_weighted_edges_from(El)
    return G_El


def update_l_G_EL(G_El, edges, l, al, S, T):
    for u in S:
        l[u] = l[u]- al
    for u in T:
        l[u]= l[u]+al
    El = []
    for (u, v, s) in edges:
        if round(l[u] + l[v],2) <= round(s,2):
            El.append((u, v, s))
    G_El.add_weighted_edges_from(El)
    return G_El

def Hungarian(cand, pos, M, G, fitness, weight_probability=[1, 0, 0], version=3, local=False):
    X = pos
    Y = list(cand.keys())
    unmatched_X = []
    unmatched_Y = []

    matched_pos_dic = {}
    matched_cand_dic = {}
    for (u, v) in M:
        if u in pos:
            matched_pos_dic[u] = v
            matched_cand_dic[v] = u
        else:
            matched_pos_dic[v] = u
            matched_cand_dic[u] = v
    for u in pos:
        if u not in matched_pos_dic:
            unmatched_X.append(u)
    for u in cand:
        if u not in matched_cand_dic:
            unmatched_Y.append(u)

    # 1) generate initial labelling l and matching M in El.
    l, G_El, edge_dic, edges = pre_process(cand, pos, M, G, fitness, weight_probability=weight_probability,
                                           version=version, local=local)

    # If M perfect, stop.Otherwise pick free vertex u ∈ X. SetS={u},T =∅.
    Flaggg =True
    while len(M) != len(X) and Flaggg:
        S = []
        T = []
        u = unmatched_X[0]
        S.append(u)
        Tree = [u]
        Trees = []
        NlS = list(G_El.neighbors(u))
        '''
        1) Find an augmenting path for M in El this increases size of M

        2) If no augmenting path exists, improve l to l′ such that El ⊂ El′. Go to 1
        '''

        '''
        If Nl(S) = T, update labels (forcing Nl(S) ̸= T )
         αl = mins∈S, y̸∈T {l(x) + l(y) − w(x, y)}
    ′ l(v)−αl ifv∈S 
         l(v)= l(v)+αl ifv∈T
       l(v) otherwise
    '''

        step_three_flag = True
        while step_three_flag:
            step_three_flag = False
            if len(list(set(NlS) - set(T))) == 0:
                al = 100000
                # mm=[]
                for u in S:
                    temp = list(set(Y) - set(T))
                    for v in temp:
                        if (u, v) in edge_dic:
                            temp = round(l[u] + l[v] - edge_dic.get((u, v), 0), 5)

                            al = min(al, temp)

                if al==100000:
                    Flaggg=False
                    break

                G_El = update_l_G_EL(G_El, edges, l, al, S, T)


                for u in S:
                    neigh_list = list(G_El.neighbors(u))
                    NlS = list(set(NlS + neigh_list))

            if len(list(set(NlS) - set(T))) != 0:
                temp = list(set(NlS) - set(T))
                flag = True
                while (flag):
                    current_node = Tree[-1]
                    neighbor_list = G_El.neighbors(current_node)
                    for neighbor_node in neighbor_list:
                        if neighbor_node in temp:
                            y = neighbor_node
                            flag = False
                            break
                    if flag:
                        if len(Tree) > 2:
                            if Tree not in Trees:
                                Trees.append(Tree.copy())
                            Tree.pop()
                            Tree.pop()
                        else:
                            Tree = Trees.pop(0)

                Tree.extend([y])
                if y in unmatched_Y:
                    gender = nx.get_node_attributes(G, 'att')
                    for i in range(int(len(Tree) / 2)):
                        u = Tree[2 * i]
                        v = Tree[2 * i + 1]
                        if u in pos:
                            p1 = u
                            c1 = v
                        else:
                            c1 = u
                            p1 = v

                        gender[p1] = cand[c1]
                        matched_pos_dic[p1] = c1
                        matched_cand_dic[c1] = p1
                        if p1 in unmatched_X:
                            unmatched_X.remove(p1)
                        if c1 in unmatched_Y:
                            unmatched_Y.remove(c1)

                    M = [(u, v) for (u, v) in matched_pos_dic.items()]
                    nx.set_node_attributes(G, gender, 'att')
                    l, G_El, edge_dic, edges = pre_process(cand, pos, M, G, fitness,
                                                           weight_probability=weight_probability, version=version,local=local)

                else:
                    z = matched_cand_dic[y]
                    if y == Tree[-1]:
                        Tree = Tree + [z]
                    else:
                        Tree = [z] + Tree
                    S.append(z)
                    T.append(y)
                    neigh_list = list(G_El.neighbors(z))
                    NlS = list(set(NlS + neigh_list))
                    step_three_flag = True

    if Flaggg==False:
        return [],[]

    return M, G




def Hungarian_simple(cand, pos, M, edges,edge_dic , l, G):
    X = pos
    Y = list(cand.keys())
    unmatched_X = []
    unmatched_Y = []

    matched_pos_dic = {}
    matched_cand_dic = {}
    for (u, v) in M:
        if u in pos:
            matched_pos_dic[u] = v
            matched_cand_dic[v] = u
        else:
            matched_pos_dic[v] = u
            matched_cand_dic[u] = v
    for u in pos:
        if u not in matched_pos_dic:
            unmatched_X.append(u)
    for u in cand:
        if u not in matched_cand_dic:
            unmatched_Y.append(u)

    G_El = update_G_EL(edges, l)
    flaggggg=True
    # If M perfect, stop.Otherwise pick free vertex u ∈ X. SetS={u},T =∅.
    while len(M) != len(X) and flaggggg:
        S = []
        T = []
        u = unmatched_X[0]
        S.append(u)
        Tree = [u]
        Trees = []
        if u not  in G_El.nodes():
            aaaa=0
        NlS = list(G_El.neighbors(u))
        '''
        1) Find an augmenting path for M in El this increases size of M

        2) If no augmenting path exists, improve l to l′ such that El ⊂ El′. Go to 1
        '''

        '''
        If Nl(S) = T, update labels (forcing Nl(S) ̸= T )
         αl = mins∈S, y̸∈T {l(x) + l(y) − w(x, y)}
    ′ l(v)−αl ifv∈S 
         l(v)= l(v)+αl ifv∈T
       l(v) otherwise
    '''

        step_three_flag = True
        while step_three_flag:
            step_three_flag = False
            if len(list(set(NlS) - set(T))) == 0:
                al = 100000
                # mm=[]
                for u in S:
                    temp = list(set(Y) - set(T))
                    for v in temp:
                        if (u, v) in edge_dic:
                            temp = round(l[u] + l[v] - edge_dic.get((u, v), 0), 5)
                            al = min(al, temp)

                if al==100000:
                    flaggggg= False

                G_El = update_l_G_EL(G_El, edges, l, al, S, T)

                for u in S:
                    neigh_list = list(G_El.neighbors(u))
                    NlS = list(set(NlS + neigh_list))

            if len(list(set(NlS) - set(T))) != 0:
                temp = list(set(NlS) - set(T))
                flag = True
                while (flag):
                    current_node = Tree[-1]
                    neighbor_list = G_El.neighbors(current_node)
                    for neighbor_node in neighbor_list:
                        if neighbor_node in temp:
                            y = neighbor_node
                            flag = False
                            break
                    if flag:
                        if len(Tree) > 2:
                            if Tree not in Trees:
                                Trees.append(Tree.copy())
                            Tree.pop()
                            Tree.pop()
                        else:
                            Tree = Trees.pop(0)

                Tree.extend([y])
                if y in unmatched_Y:
                    gender = nx.get_node_attributes(G, 'att')
                    for i in range(int(len(Tree) / 2)):
                        u = Tree[2 * i]
                        v = Tree[2 * i + 1]
                        if u in pos:
                            p1 = u
                            c1 = v
                        else:
                            c1 = u
                            p1 = v

                        gender[p1] = cand[c1]
                        matched_pos_dic[p1] = c1
                        matched_cand_dic[c1] = p1
                        if p1 in unmatched_X:
                            unmatched_X.remove(p1)
                        if c1 in unmatched_Y:
                            unmatched_Y.remove(c1)

                    M = [(u, v) for (u, v) in matched_pos_dic.items()]
                    nx.set_node_attributes(G, gender, 'att')
                    # l, G_El, edge_dic, edges = Hungarian_pre_process(Y, X, M, G, fitness, method, cands2=cand,
                    #                                                 weight_probability=weight_probability, G_El=G_El)
                    #l, G_El, edge_dic, edges = pre_process(cand, pos, M, G, fitness,weight_probability=weight_probability, version=version)
                    #G_El = update_G_EL(edges, l)
                else:
                    z = matched_cand_dic[y]
                    if y == Tree[-1]:
                        Tree = Tree + [z]
                    else:
                        Tree = [z] + Tree
                    S.append(z)
                    T.append(y)
                    if z not in G_El.nodes():
                        x=0
                    neigh_list = list(G_El.neighbors(z))
                    NlS = list(set(NlS + neigh_list))
                    step_three_flag = True
    if flaggggg==False:
        return [],[]
    return M, G


def Hungarian2(cand, pos, M, G, fitness, method=1, weight_probability=[1, 0, 0], version=3):
    X = pos
    Y = list(cand.keys())
    unmatched_X = []
    unmatched_Y = []

    matched_pos_dic = {}
    matched_cand_dic = {}
    for (u, v) in M:
        if u in pos:
            matched_pos_dic[u] = v
            matched_cand_dic[v] = u
        else:
            matched_pos_dic[v] = u
            matched_cand_dic[u] = v
    for u in pos:
        if u not in matched_pos_dic:
            unmatched_X.append(u)
    for u in cand:
        if u not in matched_cand_dic:
            unmatched_Y.append(u)

    # 1) generate initial labelling l and matching M in El.
    l, G_El, edge_dic, edges = pre_process(cand, pos, M, G, fitness, method, weight_probability=weight_probability,
                                           version=version)

    # If M perfect, stop.Otherwise pick free vertex u ∈ X. SetS={u},T =∅.
    while len(M) != len(X):
        S = []
        T = []
        u = unmatched_X[0]
        S.append(u)
        Tree = [u]
        Trees = []
        NlS = list(G_El.neighbors(u))
        '''
        1) Find an augmenting path for M in El this increases size of M

        2) If no augmenting path exists, improve l to l′ such that El ⊂ El′. Go to 1
        '''

        '''
        If Nl(S) = T, update labels (forcing Nl(S) ̸= T )
         αl = mins∈S, y̸∈T {l(x) + l(y) − w(x, y)}
    ′ l(v)−αl ifv∈S 
         l(v)= l(v)+αl ifv∈T
       l(v) otherwise
    '''

        step_three_flag = True
        while step_three_flag:
            step_three_flag = False
            if len(list(set(NlS) - set(T))) == 0:
                al = 100000
                # mm=[]
                for u in S:
                    temp = list(set(Y) - set(T))
                    for v in temp:
                        if (u, v) in edge_dic:
                            temp = round(l[u] + l[v] - edge_dic.get((u, v), 0), 5)
                            al = min(al, temp)



                G_El = update_l_G_EL(G_El, edges, l, al, S, T)

                for u in S:
                    neigh_list = list(G_El.neighbors(u))
                    NlS = list(set(NlS + neigh_list))

            if len(list(set(NlS) - set(T))) != 0:
                temp = list(set(NlS) - set(T))
                flag = True
                while (flag):
                    current_node = Tree[-1]
                    neighbor_list = G_El.neighbors(current_node)
                    for neighbor_node in neighbor_list:
                        if neighbor_node in temp:
                            y = neighbor_node
                            flag = False
                            break
                    if flag:
                        if len(Tree) > 2:
                            if Tree not in Trees:
                                Trees.append(Tree.copy())
                            Tree.pop()
                            Tree.pop()
                        else:
                            Tree = Trees.pop(0)

                Tree.extend([y])
                if y in unmatched_Y:
                    gender = nx.get_node_attributes(G, 'att')
                    for i in range(int(len(Tree) / 2)):
                        u = Tree[2 * i]
                        v = Tree[2 * i + 1]
                        if u in pos:
                            p1 = u
                            c1 = v
                        else:
                            c1 = u
                            p1 = v

                        gender[p1] = cand[c1]
                        matched_pos_dic[p1] = c1
                        matched_cand_dic[c1] = p1
                        if p1 in unmatched_X:
                            unmatched_X.remove(p1)
                        if c1 in unmatched_Y:
                            unmatched_Y.remove(c1)

                    M = [(u, v) for (u, v) in matched_pos_dic.items()]
                    nx.set_node_attributes(G, gender, 'att')
                    # l, G_El, edge_dic, edges = Hungarian_pre_process(Y, X, M, G, fitness, method, cands2=cand,
                    #                                                 weight_probability=weight_probability, G_El=G_El)
                    l, G_El, edge_dic, edges = pre_process(cand, pos, M, G, fitness, method,
                                                           weight_probability=weight_probability, version=version)

                else:
                    z = matched_cand_dic[y]
                    if y == Tree[-1]:
                        Tree = Tree + [z]
                    else:
                        Tree = [z] + Tree
                    S.append(z)
                    T.append(y)
                    neigh_list = list(G_El.neighbors(z))
                    NlS = list(set(NlS + neigh_list))
                    step_three_flag = True

    return M, G

