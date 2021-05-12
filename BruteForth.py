import networkx as nx
import PostProcess as PP2
import Evaluation as EV




def assignmentBruthForth1(cands_dic, pos_list, fitness_dic, G):
    p_c_dic = {}
    c_p_dic = {}
    for (c,p) in fitness_dic:
        if p in p_c_dic:
            p_c_dic[p].append(c)
        else:
            p_c_dic[p] = [c]
        if c in c_p_dic:
            c_p_dic[c].append(p)
        else:
            c_p_dic[c] = [p]
    matched = bruthForth(p_c_dic, c_p_dic, pos_list)

    output=[]
    Gs = {}
    for matched in matched:
        G1 = G.copy()
        gender = nx.get_node_attributes(G, 'att')
        for (p,c) in matched:
            gender[p] = cands_dic[c]
        nx.set_node_attributes(G1, gender, 'att')
        stats = EV.evaluate(G1, set(pos_list), fitness_dic, matched=matched)
        r1 = abs(stats[0])
        r2 = stats[1]
        r3 = stats[2]
        r= (r1,r2)
        flag= True
        remove_list=[]
        for (s1,s2) in output:
            if s1<=r1 and s2>=r2:
                flag = False
            elif s1>=r1 and s2<=r2:
                remove_list.append((s1,s2))
                flag = True
        for item in remove_list:
            output.remove(item)
        if flag:
            output.append(r)
            Gs[r] = (G1.copy(), matched.copy())

    r1= sorted(output, key=lambda item:item[0])
    r2= sorted(output, key=lambda item:item[1], reverse=True)
    ds={}
    a=abs(r1[0][0] + r2[0][0])/2
    b=abs(r1[0][1] + r2[0][1])/2
    if a==0: a=0.1
    for item in output:
        d = ((item[0] -a)/a)**2 + ((item[1]-b)/b)**2
        ds[item] = d
    r4 = [k for(k,v) in sorted(ds.items(), key=lambda item:item[1])]
    return Gs[r1[0]], Gs[r2[0]], Gs[r4[0]]

def assignmentBruthForth2(cands_dic, pos_list, fitness_dic, G):
    p_c_dic = {}
    c_p_dic = {}
    for (c,p) in fitness_dic:
        if p in p_c_dic:
            p_c_dic[p].append(c)
        else:
            p_c_dic[p] = [c]
        if c in c_p_dic:
            c_p_dic[c].append(p)
        else:
            c_p_dic[c] = [p]
    matched = bruthForth(p_c_dic, c_p_dic, pos_list)

    output=[]
    Gs = {}
    for matched in matched:
        G1 = G.copy()
        gender = nx.get_node_attributes(G, 'att')
        for (p,c) in matched:
            gender[p] = cands_dic[c]
        nx.set_node_attributes(G1, gender, 'att')
        stats = EV.evaluate(G1, set(pos_list), fitness_dic, matched=matched)
        r1 = abs(stats[0])
        r2 = stats[1]
        r3 = stats[2]
        r= (r1,r2, r3)
        flag= True
        remove_list=[]
        for (s1,s2,s3) in output:
            if s1<=r1 and s2>=r2 and s3<=r3:
                flag = False
            elif s1>=r1 and s2<=r2 and  s3>=r3:
                remove_list.append((s1,s2,s3))
                flag = True
        for item in remove_list:
            output.remove(item)
        if flag:
            output.append(r)
            Gs[r] = (G1.copy(), matched.copy())

    r1= sorted(output, key=lambda item:item[0])
    r2= sorted(output, key=lambda item:item[1], reverse=True)
    r3= sorted(output, key=lambda item:item[2], reverse=True)
    ds={}
    a=abs(r1[0][0] + r2[0][0])/2
    b=abs(r1[0][1] + r2[0][1])/2
    if a==0: a=0.1
    for item in output:
        d = ((item[0] -a)/a)**2 + ((item[1]-b)/b)**2
        ds[item] = d
    r4 = [k for(k,v) in sorted(ds.items(), key=lambda item:item[1])]

    return Gs[r1[0]], Gs[r2[0]],Gs[r3[0]], Gs[r4[0]]


def bruteforth_remove(p,c, p_c_dic, c_p_dic):
    cands= p_c_dic[p]
    poss = c_p_dic[c]
    for c1 in cands:
        c_p_dic[c1].remove(p)
    for p1 in poss:
        p_c_dic[p1].remove(c)
    del p_c_dic[p]
    del c_p_dic[c]


def bruthForth(p_c_dic, c_p_dic, pos_list):

    pos_list_current = pos_list.copy()
    matched=[]
    if len(pos_list_current) > 0:
        p = pos_list_current.pop()
        c_list = p_c_dic[p].copy()
        if len(c_list)==0:
            return [-1]
        else:
            for c in c_list:
                M=[(p,c)]
                p_c_dic_current={item:p_c_dic[item].copy() for item in p_c_dic}
                c_p_dic_current={item:c_p_dic[item].copy() for item in c_p_dic}
                bruteforth_remove(p, c, p_c_dic_current, c_p_dic_current)
                matched_current = bruthForth(p_c_dic_current, c_p_dic_current, pos_list_current)
                for item in matched_current:
                    if item != -1:
                        item.extend(M)
                        matched.append(item)
    else:
        return [[]]
    if matched==[]:
        return [-1]
    return matched

