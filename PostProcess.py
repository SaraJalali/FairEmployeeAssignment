

import sys
sys.path.insert(0, 'Score/')
sys.path.insert(0, '../InformationUnfairness/')
import IU as IU
import EC as EC
import statistics as st
import networkx as nx
import math
from community import community_louvain
from collections import defaultdict
import math

def post_process(G, P_set, matched, F):

    score=0
    for (u,v) in matched:
        if u in P_set:
            p =u
            c = v
        else:
            c=u
            p = v
        if (c, p) in F:
            score += float(F[(c,p)])
        else:
            x=0

    support = []
    att_dic = nx.get_node_attributes(G, 'att')

    for p in list(P_set):
        c_att = att_dic[p]
        neigh_list = G.neighbors(p)
        temp=0
        for neigh in neigh_list:
            att = att_dic[neigh]
            if att == c_att:
                temp += 1
        support.append(temp)

    '''
    if method ==1:
        ass = nx.attribute_assortativity_coefficient(G, 'att')
        div = ass
    elif method ==2:
        iu = IU.InformationUnfairness(G)
        div = iu
    elif method ==3:
        ec = EC.EchoChamber(G)
        div = ec
    '''

    average1, mean1 = support_group(G)
    return round(nx.attribute_assortativity_coefficient(G, 'att'),2),\
           round(IU.InformationUnfairness(G),2), \
           round(entropy(G),2),\
           round(score,2),\
           round(average1,2), round(mean1,2)



def brokerage_eq(G, groups):
    gender= nx.get_node_attributes(G, 'att')
    male_list=[]
    female_list=[]
    cent = nx.betweenness_centrality(G)
    for k,v in gender.items():
        if v=='male':
            male_list.append(cent[k])
        elif v == 'female':
            female_list.append(cent[k])
    if len(male_list)==0:
        male_list =[0]
    elif len(female_list)==0:
        female_list=[0]
    gap = st.mean(female_list) - st.mean(male_list)

    gaps=[]

    for group in groups:
        male_list = []
        female_list = []
        #cent = nx.betweenness_centrality(G)
        for k in group:
            v= gender[k]
            if v == 'male':
                male_list.append(cent[k])
            elif v == 'female':
                female_list.append(cent[k])
        if len(male_list)> len(female_list):
            if len(female_list) ==0:
                female_list=[0]
            gap = st.mean(female_list) - st.mean(male_list)
            gaps.append(gap)
        else:
            if len(male_list)==0:
                male_list=[0]
            if len(female_list)==0:
                female_list = [0]
            gap = -st.mean(female_list) + st.mean(male_list)
            gaps.append(gap)

    return gap, st.mean(gaps)





def post_process2(G, P_set, matched, F):

    score=0
    for (u,v) in matched:
        if u in P_set:
            p =u
            c = v
        else:
            c=u
            p = v
        if (c, p) in F:
            score += float(F[(c,p)])
        else:
            x=0

    support = []
    att_dic = nx.get_node_attributes(G, 'att')

    for p in list(P_set):
        c_att = att_dic[p]
        neigh_list = G.neighbors(p)
        temp=0
        for neigh in neigh_list:
            att = att_dic[neigh]
            if att == c_att:
                temp += 1
        support.append(temp)

    '''
    if method ==1:
        ass = nx.attribute_assortativity_coefficient(G, 'att')
        div = ass
    elif method ==2:
        iu = IU.InformationUnfairness(G)
        div = iu
    elif method ==3:
        ec = EC.EchoChamber(G)
        div = ec
    '''

    return round(nx.attribute_assortativity_coefficient(G, 'att'),3), round(IU.InformationUnfairness(G),3), round(EC.EchoChamber(G),3), round(score,3), round(st.mean(support),3)


def stats(G, P_set, matched, F, method=1):

    score=0
    for (u,v) in matched:
        if u in P_set:
            p =u
            c = v
        else:
            c=u
            p = v
        if (c, p) in F:
            score += float(F[(c,p)])
        else:
            x=0

    support = []
    att_dic = nx.get_node_attributes(G, 'att')

    for p in list(P_set):
        c_att = att_dic[p]
        neigh_list = G.neighbors(p)
        temp=0
        for neigh in neigh_list:
            att = att_dic[neigh]
            if att == c_att:
                temp += 1
        support.append(temp)


    if method ==1:
        ass = nx.attribute_assortativity_coefficient(G, 'att')
        div = ass
    elif method ==2:
        iu = IU.InformationUnfairness(G)
        div = iu
    elif method ==3:
        ec = EC.EchoChamber(G)
        div = ec

    return round(score,3), round(div,3), round(st.mean(support),3)


