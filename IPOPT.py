import networkx as nx
from gekko import GEKKO
import sys




def assignment_simple_gekko2(candidate_dic, position_list , fitness_dic, G):

    m = GEKKO()
    m.options.SOLVER = 1
    m.options.MAX_MEMORY = 3000000# APOPT is an MINLP solver

    # optional solver settings with APOPT
    m.solver_options = ['minlp_maximum_iterations 1000', \
                        # minlp iterations with integer solution
                        'minlp_max_iter_with_int_sol 10', \
                        # treat minlp as nlp
                        'minlp_as_nlp 0', \
                        # nlp sub-problem max iterations
                        'nlp_maximum_iterations 500', \
                        # 1 = depth first, 2 = breadth first
                        'minlp_branch_method 1', \
                        # maximum deviation from whole number
                        'minlp_integer_tol 0.05', \
                        # covergence tolerance
                        'minlp_gap_tol 0.01']
    X = m.Array(m.Var, len(fitness_dic), integer=True)
    for xi in X:
        xi.value = 0
        xi.lower = 0
        xi.upper = 1

    fitness_index_dic= dict(zip(fitness_dic.keys(), range(len(fitness_dic))))

    weight_list =list(fitness_dic.values())
    weight_list = [float(item) for item in weight_list]
    candidate_pair_list = list(fitness_dic.keys())

    objective =sum ([X[i]*weight_list[i] for i in range(len(weight_list))])
    objective.NAME = simplify_Objective(objective.NAME, len(X))
    m.Maximize(objective)


    pos_cand_dic = {}
    cand_pos_dic = {}
    for i in range(len(candidate_pair_list)):
        (c,p) = candidate_pair_list[i]
        if p in pos_cand_dic:
            pos_cand_dic[p].append(c)
        else:
            pos_cand_dic[p] = [c]

        if c in cand_pos_dic:
            cand_pos_dic[c].append(p)
        else:
            cand_pos_dic[c] = [p]


    score_tuple_dic = neighbor_info(G, position_list)


    for p, cands in pos_cand_dic.items():
        indices=[]
        (mm,ff) = score_tuple_dic[p]
        m_ind =[]
        f_ind =[]
        for c in cands:
            i = fitness_index_dic[(c,p)]
            indices.append(i)
            if candidate_dic[c] =='male':
                m_ind.append(i)
            else:
                f_ind.append(i)

        #constraint
        z = sum([X[i] for i in indices])
        z.NAME = simplify_Objective(z.NAME, len(X))
        m.Equation(z == 1)


        a1 = mm-ff
        a2 = ff-mm
        o1 =  sum([X[i] for i in m_ind])
        o2 = sum([X[i] for i in f_ind])

        if len(m_ind)>0:
            o1.NAME = simplify_Objective(o1.NAME, len(X))
        if len(f_ind)>0:
            o2.NAME = simplify_Objective(o2.NAME, len(X))

        m.Minimize(a1+o1+ (-1)*(o2))
        m.Minimize(a2+o2+ (-1)*(o1))
        x=0


    for c, pos in cand_pos_dic.items():
        indices=[]
        for p in pos:
            i = fitness_index_dic[(c,p)]
            indices.append(i)
        z = sum([X[i] for i in indices])
        z.NAME = simplify_Objective(z.NAME, len(X))
        m.Equation(z == 1)
    try:
        m.solve(disp=False)
        result = X.copy()
        result_list = [item.value[0] for item in result]

        G_output = G.copy()
        att_dic = nx.get_node_attributes(G_output, 'att')

        score = 0.0
        matched = []
        for i in range(len(result)):
            if result_list[i] == 1:
                (c, p) = candidate_pair_list[i]
                matched.append((c, p))
                score += float(fitness_dic[(c, p)])
                att_dic[p] = candidate_dic[c]

        nx.set_node_attributes(G_output, att_dic, 'att')

        #print(matched)
    except:
        return G ,[]
    return G_output, matched


def assignment_simple_gekko(candidate_dic, position_list , fitness_dic, G):
    gender = nx.get_node_attributes(G, 'att')
    m = GEKKO()
    m.options.SOLVER = 1
    m.options.MAX_MEMORY = 30000000# APOPT is an MINLP solver

    # optional solver settings with APOPT
    m.solver_options = ['minlp_maximum_iterations 1000', \
                        # minlp iterations with integer solution
                        'minlp_max_iter_with_int_sol 10', \
                        # treat minlp as nlp
                        'minlp_as_nlp 0', \
                        # nlp sub-problem max iterations
                        'nlp_maximum_iterations 500', \
                        # 1 = depth first, 2 = breadth first
                        'minlp_branch_method 1', \
                        # maximum deviation from whole number
                        'minlp_integer_tol 0.05', \
                        # covergence tolerance
                        'minlp_gap_tol 0.01']
    X = m.Array(m.Var, len(fitness_dic), integer=True)
    for xi in X:
        xi.value = 0
        xi.lower = 0
        xi.upper = 1

    fitness_index_dic= dict(zip(fitness_dic.keys(), range(len(fitness_dic))))

    weight_list =list(fitness_dic.values())
    weight_list = [float(item) for item in weight_list]
    candidate_pair_list = list(fitness_dic.keys())

    objective =sum ([X[i]*weight_list[i] for i in range(len(weight_list))])
    objective.NAME = simplify_Objective(objective.NAME, len(X))
    m.Maximize(objective)


    pos_cand_dic = {}
    cand_pos_dic = {}
    for i in range(len(candidate_pair_list)):
        (c,p) = candidate_pair_list[i]
        if p in pos_cand_dic:
            pos_cand_dic[p].append(c)
        else:
            pos_cand_dic[p] = [c]

        if c in cand_pos_dic:
            cand_pos_dic[c].append(p)
        else:
            cand_pos_dic[c] = [p]


    score_tuple_dic = neighbor_info(G)

    for p in G.nodes():
        neighs = G[p]
        pos = []
        for v in neighs:
            if gender[v] == 'None':
                pos.append(v)
        if len(pos) > 0:
            (mm, ff) = score_tuple_dic[p]
            m_ind = []
            f_ind = []
            indices = []
            for u in pos:
                if u in pos_cand_dic:
                    cands = pos_cand_dic[u]
                    for c in cands:
                        i = fitness_index_dic[(c, u)]
                        indices.append(i)
                        if candidate_dic[c] == 'male':
                            m_ind.append(i)
                        else:
                            f_ind.append(i)


            a1 = mm - ff
            a2 = ff - mm
            o1 = sum([X[i] for i in m_ind])
            o2 = sum([X[i] for i in f_ind])

            if len(m_ind) > 0:
                o1.NAME = simplify_Objective(o1.NAME, len(X))
            if len(f_ind) > 0:
                o2.NAME = simplify_Objective(o2.NAME, len(X))

            m.Minimize(a1 + o1 + (-1) * (o2))
            m.Minimize(a2 + o2 + (-1) * (o1))





    for c, pos in cand_pos_dic.items():
        indices=[]
        for p in pos:
            i = fitness_index_dic[(c,p)]
            indices.append(i)
            # constraint
        z = sum([X[i] for i in indices])
        z.NAME = simplify_Objective(z.NAME, len(X))
        m.Equation(z == 1)

    for p, cand in pos_cand_dic.items():
        indices=[]
        for c in cand:
            i = fitness_index_dic[(c, p)]
            indices.append(i)
            # constraint
        z = sum([X[i] for i in indices])
        z.NAME = simplify_Objective(z.NAME, len(X))
        m.Equation(z == 1)

    ###

    ###


    #m.solve(disp=False)
    try:
    #if True:
        m.solve(disp=False)
        result = X.copy()
        result_list = [item.value[0] for item in result]

        G_output = G.copy()
        att_dic = nx.get_node_attributes(G_output, 'att')

        score = 0.0
        matched = []
        for i in range(len(result)):
            if result_list[i] == 1:
                (c, p) = candidate_pair_list[i]
                matched.append((c, p))
                score += float(fitness_dic[(c, p)])
                att_dic[p] = candidate_dic[c]

        nx.set_node_attributes(G_output, att_dic, 'att')

        #print(matched)
    except:
        return G ,[]
    return G_output, matched


def assignment_simple_gekko_(candidate_dic, position_list , fitness_dic, G):

    gender = nx.get_node_attributes(G, 'att')
    gender.update(candidate_dic)
    gender_list = list(gender.values())
    m = gender_list.count('male')
    f = gender_list.count('female')
    t= float(m+f)
    m = m/t
    f = f/t
    p1 = m*m*t
    p2 = m*f*t*2
    p3 = f*f*t

    m = GEKKO()
    m.options.SOLVER = 1
    m.options.MAX_MEMORY = 3000000# APOPT is an MINLP solver

    # optional solver settings with APOPT
    m.solver_options = ['minlp_maximum_iterations 1000', \
                        # minlp iterations with integer solution
                        'minlp_max_iter_with_int_sol 10', \
                        # treat minlp as nlp
                        'minlp_as_nlp 0', \
                        # nlp sub-problem max iterations
                        'nlp_maximum_iterations 500', \
                        # 1 = depth first, 2 = breadth first
                        'minlp_branch_method 1', \
                        # maximum deviation from whole number
                        'minlp_integer_tol 0.05', \
                        # covergence tolerance
                        'minlp_gap_tol 0.01']
    X = m.Array(m.Var, len(fitness_dic), integer=True)
    for xi in X:
        xi.value = 0
        xi.lower = 0
        xi.upper = 1

    fitness_index_dic= dict(zip(fitness_dic.keys(), range(len(fitness_dic))))

    weight_list =list(fitness_dic.values())
    weight_list = [float(item) for item in weight_list]
    candidate_pair_list = list(fitness_dic.keys())

    objective =sum ([X[i]*weight_list[i] for i in range(len(weight_list))])
    objective.NAME = simplify_Objective(objective.NAME, len(X))
    m.Maximize(objective)


    pos_cand_dic = {}
    cand_pos_dic = {}
    for i in range(len(candidate_pair_list)):
        (c,p) = candidate_pair_list[i]
        if p in pos_cand_dic:
            pos_cand_dic[p].append(c)
        else:
            pos_cand_dic[p] = [c]

        if c in cand_pos_dic:
            cand_pos_dic[c].append(p)
        else:
            cand_pos_dic[c] = [p]


    mm_count =0
    mf_count =0
    ff_count =0

    mm_count_ind = []
    mf_count_ind = []
    ff_count_ind = []

    mm_count_= []
    mf_count_ = []
    ff_count_ = []
    for p in G.nodes():
        neighs = G[p]
        neighs =[item  for item in neighs if item>p]
        if gender[p] == 'male':
            for v in neighs:
                if gender[v] == 'male':
                    mm_count +=1
                elif gender[v] == 'female':
                    mf_count +=1
                else:
                    cands = pos_cand_dic[v]
                    for c in cands:
                        i = fitness_index_dic[(c, v)]
                        if candidate_dic[c] == 'male':
                            mm_count_ind.append(i)
                        else:
                            mf_count_ind.append(i)
        elif gender[p] == 'female':
            for v in neighs:
                if gender[v] == 'male':
                    mf_count += 1
                elif gender[v] == 'female':
                    ff_count += 1
                else:
                    cands = pos_cand_dic[v]
                    for c in cands:
                        i = fitness_index_dic[(c, v)]
                        if candidate_dic[c] == 'male':
                            mf_count_ind.append(i)
                        else:
                            ff_count_ind.append(i)
        else:
            cands = pos_cand_dic[p]
            m_ind = []
            f_ind = []
            for c in cands:
                i = fitness_index_dic[(c, p)]
                if candidate_dic[c] == 'male':
                    m_ind.append(i)
                else:
                    f_ind.append(i)
            m_p = sum([X[i] for i in m_ind])
            f_p = sum([X[i] for i in f_ind])

            if len(m_ind) > 0:
                m_p.NAME = simplify_Objective(m_p.NAME, len(X))
            if len(f_ind) > 0:
                f_p.NAME = simplify_Objective(f_p.NAME, len(X))

            m1=0
            f1=0
            m1_ind=[]
            f1_ind=[]
            for v in neighs:
                if gender[v] == 'male':
                    m1 += 1
                elif gender[v] == 'female':
                    f1 += 1
                else:
                    cands = pos_cand_dic[v]
                    for c in cands:
                        i = fitness_index_dic[(c, v)]
                        if candidate_dic[c] == 'male':
                            m1_ind.append(i)
                        else:
                            f1_ind.append(i)

            m1_p = sum([X[i] for i in m1_ind])+m1
            f1_p = sum([X[i] for i in f1_ind])+f1

            if len(m1_ind) > 0:
                m1_p.NAME = simplify_Objective(m1_p.NAME, len(X))
            if len(f1_ind) > 0:
                f1_p.NAME = simplify_Objective(f1_p.NAME, len(X))

            if len(m_ind)>0 and (len(m1_ind) > 0 or m1 !=0):
                mm_count_.append(m_p * m1_p)
            if len(m_ind)>0 and (len(f1_ind) > 0 or f1 !=0):
                mf_count_.append(m_p * f1_p)
            if len(f_ind)>0 and (len(m1_ind) > 0 or m1 !=0):
                mf_count_.append(f_p * m1_p)
            if len(f_ind)>0 and (len(f1_ind) > 0 or f1 !=0):
                ff_count_.append(f_p * f1_p)







    ###
    mm_count__ = sum([X[i] for i in mm_count_ind])
    mf_count__ = sum([X[i] for i in mf_count_ind])
    ff_count__ = sum([X[i] for i in ff_count_ind])

    mm_count_ = sum(mm_count_)
    mf_count_ = sum(mf_count_)
    ff_count_ = sum(ff_count_)

    mm_count = mm_count_ + mm_count__ + mm_count
    ff_count = ff_count_ + ff_count__ + ff_count
    mf_count = mf_count_ + mf_count__ + mf_count

    m.Minimize(mm_count - p1)
    m.Minimize(p1 - mm_count)
    m.Minimize(mf_count - p2)
    m.Minimize(p2 - mf_count)
    m.Minimize(ff_count - p3)
    m.Minimize(p3 - ff_count)
    for c, pos in cand_pos_dic.items():
        indices=[]
        for p in pos:
            i = fitness_index_dic[(c,p)]
            indices.append(i)
            # constraint
        z = sum([X[i] for i in indices])
        z.NAME = simplify_Objective(z.NAME, len(X))
        m.Equation(z == 1)

    if True:
        m.solve(disp=False)
        result = X.copy()
        result_list = [item.value[0] for item in result]

        G_output = G.copy()
        att_dic = nx.get_node_attributes(G_output, 'att')

        score = 0.0
        matched = []
        for i in range(len(result)):
            if result_list[i] == 1:
                (c, p) = candidate_pair_list[i]
                matched.append((c, p))
                score += float(fitness_dic[(c, p)])
                att_dic[p] = candidate_dic[c]

        nx.set_node_attributes(G_output, att_dic, 'att')
    return G_output, matched



def neighbor_info(G):
    score_tuple_dic={}
    gender=nx.get_node_attributes(G,'att')
    for u in G.nodes():
        m=0
        f=0
        neighs = G[u]
        for v in neighs:
            if gender[v] =='male':
                m+=1
            elif gender[v] =='female':
                f+=1
        score_tuple_dic[u]=(m,f)
    return score_tuple_dic


def simplify(obj,cont_vars, final=False):
    dict={}
    constant =0
    splitted = obj.split('+')
    if len(splitted)==1:
        return splitted[0]
    for item in splitted:
        items = item.split('*')
        vars = []
        numbers = []
        for u in items:
            if u in cont_vars:
                vars.append(u)
            elif u != '':
                numbers.append(u)
        if len(vars)>0 or len(numbers)>0:
            num_out = 1
            for item in numbers:
               # if item == 'int_v1001':
               #     x=0
                num_out *= float(item)

            if num_out !=0:
                if len(vars) == 0:
                    constant += num_out
                else:
                    vars = sorted(vars)
                    varss = [vars[0]]
                    for i in range(1, len(vars)):
                        varss.append('*' + vars[i])
                    varss =''.join(varss)
                    if varss in dict:
                        dict[varss] += num_out
                    else:
                        dict[varss] = num_out

    constant= round(constant,3)
    if int(constant)- constant==0:
        constant = int(constant)
    output=[str(constant)]

    if final:
        for (u, v) in dict.items():
            if v != 0:
                if v == 1:
                    output.append('+' + u)
                elif v < 0:
                    v = round(v, 3)
                    if (int(v) - v) == 0:
                        v = int(v)
                    if v== -1:
                        output.append('-' + u)
                    else:
                        output.append(str(v) + '*' + u)
                else:
                    v = round(v, 3)
                    if (int(v) - v) == 0:
                        v = int(v)
                    output.append('+' + str(v) + '*' + u)
    else:
        for (u, v) in dict.items():
            if v != 0:
                if v == 1:
                    output.append('+' + u)
                else:
                    v = round(v, 3)
                    if (int(v) - v) == 0:
                        v = int(v)
                    output.append('+' + u + '*' + str(v))

    return ''.join(output)


def multi(left,right):
    splitted_left = left.split('+')
    splitted_right = right.split('+')

    output=['0']
    for l in splitted_left:
        for r in splitted_right:
            if (l != '0' and l != '0.0') and (r !='0' and l !='0.0'):
                #output+=
                output.append('+' + l + '*' + r)
    output=''.join(output)
    return output

def simplify_Objective(obj, n = 1000, final=False):
    cont_vars =set()
    for i in range(n):
        cont_vars.add('int_v'+str(i+1))
    obj+= '.'
    stack=[]
    operands= {'+', '-', '*', '**', '/', '%', '//', '('}
    par = {'(', ')'}
    i=-1
    while i <len(obj)-2:
        i+=1
        v1 = obj[i]
        v2 = obj[i+1]
        if v1 in operands:
            stack.append(v1)
        elif v1 == ')':
            temp = []
            v3 = stack.pop()
            while v3 != '(':
                temp.append(v3)
                v3 = stack.pop()
            #temp = ''.join(temp)
            #temp = simplify(temp, cont_vars)
            if temp[-1] == '-' and len(temp)>1:
                temp[-2]= '+' + negate(temp[-2])
                temp = temp[:-1]
            if len(temp) == 3 and temp[1] =='*':
                temp = multi(temp[2], temp[0])
                stack.append(temp)
                #stack.append(simplify(temp,cont_vars))
            elif len(temp) == 3 and temp[1] =='+':
                if temp[0] == '0':
                    stack.append(temp[2])
                   # stack.append(simplify(temp[2], cont_vars))
                elif temp[2] == '0':
                    stack.append(temp[0])
                    #stack.append(simplify(temp[0], cont_vars))
                else:
                    t= ''.join(reversed(temp))
                    stack.append(t)
                    #stack.append(simplify(t, cont_vars))
            elif len(temp) == 3 and temp[1] =='-':
                if temp[2] == '0':
                   # stack.append(simplify(temp[0], cont_vars))
                    stack.append(temp[0])
                elif temp[0] == '0':
                    stack.append(temp[2])
                   # stack.append(simplify(temp[2], cont_vars))
                else:
                    temp[0] = negate(temp[0])
                    temp[1] = '+'
                    t= ''.join(reversed(temp))
                    stack.append(t)
                   # stack.append(simplify(t, cont_vars))
            elif '-' in temp:
                ind = temp.index('-')
                temp[ind] = '+'
                temp[ind-1] = negate(temp[ind-1])
            else:
                t = ''.join(reversed(temp))
               # stack.append(simplify(t,cont_vars))
                stack.append(t)
        else:
            temp =''
            while v2 not in operands and v2 not in par and i <len(obj)-2:
                temp += v1
                i+=1
                v1 = obj[i]
                v2 = obj[i + 1]
            temp += v1
            if temp[0].isdigit():
                if not temp[-1].isdigit():
                    temp = temp[:-1]
                temp= float(temp)
                temp = round(temp,3)
                if temp-int(temp)==0:
                    temp= int(temp)
                temp = str(temp)
            elif temp[0]=='p':
                temp='0'
            stack.append(temp)
            #stack.append(simplify(temp, cont_vars))

    output = ''.join(stack)
    return simplify(output,cont_vars, final)



def assignment_simple_nx(candidate_dic, position_list , fitness_dic, G, constraint =False):

    edge_list= [(u,v,float(w)) for ((u,v),w) in fitness_dic.items()]


    B = nx.Graph()
    B.add_weighted_edges_from(edge_list)
    result_list = list(nx.max_weight_matching(B))

    G_output = G.copy()
    score=0.0
    att_dic = nx.get_node_attributes(G_output, 'att')
    for (u, v) in result_list:
        (c, p) = (u,v) if u in candidate_dic else (v,u)
        att_dic[p] = candidate_dic[c]
        score += float(fitness_dic[(c, p)])

    nx.set_node_attributes(G_output, att_dic, 'att')

    return G_output, score

'''
candidate_dic ={'c1':'male', 'c2':'female'}
position_list =[1,2]
fitness_dic = {('c1', 1):1, ('c1',2): 0.3, ('c2',1):0.9, ('c2',2):0.6}
G= nx.Graph()
G.add_edges_from([(1,2),(2,3),(1,3),(3,4)])
gender = {1:'None', 2:'None', 3:'male', 4:'female'}
nx.set_node_attributes(G, gender, 'att')

assignment_simple_gekko(candidate_dic, position_list , fitness_dic, G)
'''