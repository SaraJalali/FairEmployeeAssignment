import networkx as nx
import random as random
from random import sample



#For consistency we make sure that the network as an attribute names 'att
def pre_process(G):
    '''
    :param G: Graph with an attribute of any name
    :return: Graph with an attribute named 'att
    '''
    a= list(G.nodes.data())
    att_name = list((list(G.nodes.data())[0])[1].keys())[0]
    atts = nx.get_node_attributes(G, att_name)
    nx.set_node_attributes(G, atts, 'att')

    # change nodes to be string instead of integer for the sake of compatibility
    node_list = list(G.nodes())
    if type(node_list[0]) != str:
        new_G = nx.Graph()
        new_node_list =[str(item) for item in node_list]
        edge_list = list(G.edges())
        new_edge_list = [(str(u), str(v)) for (u,v) in edge_list]
        new_G.add_edges_from(new_edge_list)
        new_G.add_nodes_from(new_node_list)
        att_name_list = list((list(G.nodes.data())[0])[1].keys())
        for att_name in att_name_list:
            att_dic = nx.get_node_attributes(G, att_name)
            new_att_dic={str(u):v for (u,v) in att_dic.items()}
            nx.set_node_attributes(new_G, new_att_dic, att_name )
        G= new_G



    return G

#sample p percents of nodes randomly
def sample_open_positions(G, p):
    '''
    :param G: Graph with n nodes
    :param p: percentage of open positions
    :return: a list of sampled nodes
    '''
    nodes =G.nodes.data()
    k = int(len(G) * p)
    return sample(nodes, k)


'''
For defining the pool of candidates we consider two cases: 
(1) a pool of candidates equal to the number of open positions. For attributes of candidates, 
we simply use the at- tributes of the individuals who had been in those positions before they were made open; 
(2) a pool of candidates equal to two times the number of open positions wherein we duplicate the pool from the first case.
'''
def simulate_candidate_pool(P, k=1):
    '''

    :param P: list of open positions with their attributes
    :param k: size of pool is k times size of P
    :return: final open positions and candidates with their attribute
    '''

    att_list= [item['att'] for (_,item) in P]
    position_list=[item for (item,_) in P]

    key_list = ['c' + str(i) for i in range(len(P))]
    candidate_dict = dict(zip(key_list, att_list))

    if k==2:
        key_list = ['c' + str(i) for i in range(len(P), 2 * len(P))]
        candidate_dict.update(dict(zip(key_list, att_list)))

    return position_list, candidate_dict


#generate empty positions and candidates
def generate_PC(G, p, k):
    '''
      :param G: Graph with n nodes
      :param p: percentage of open positions
       :param k: size of pool is k times size of candidates
    :return: final open positions and candidates with their attribute
    '''
    positions = sample_open_positions(G, p)
    return simulate_candidate_pool(positions, k)


'''
We consider fitness functions F1 and F2, defined as follows. For both, we first create a random one-to-one matching
between open positions and candidates. 
We set F(pi,cj) = 1 if position pi and candidate cj are matched.
For fitness function F1, for each candidate cj, we set F(p∗,cj) = 1 for 4 random positions p∗. 
For fitness function F2, for each candidate cj , we set F (p∗, cj ) = 1 for 4 positions p∗ 
with smallest path distance to pi (the position that is already fit for cj ). 
'''

#it should be updaed for k =2 it is slow
def generate_fitness_function(G, P, C, method='F1', is_weighted = False):
    #create a random one-to-one matching between open positions and candidates
    randomCandidates = sample(C, len(P))
    F = list(zip(randomCandidates, P))
    P_set = set(P)

    #For fitness function F1, for each candidate cj, we set F(p∗,cj) = 1 for 4 random positions
    if method =='F1':
        for u in C:
            randomPositions = sample(P, 4)
            F_current = list(zip([u]*4, randomPositions))
            F.extend(F_current)
    #For fitness function F2, for each candidate cj , we set F (p∗, cj ) = 1 for 4 positions p∗
    #with smallest path distance to pi (the position that is already fit for cj )
    elif method =='F2':
        for i in range(len(P)):
            u = randomCandidates[i]
            v = P[i]
            selectedPositions=[]
            chosen =[v]
            neighs= list(G.neighbors(v))
            chosen = set(chosen)
            while len(selectedPositions)<4 and len(neighs)>0:
                v = neighs.pop()
                chosen.add(v)
                bool1 = False
                if v in P_set and v not in chosen:
                    chosen.add(v)
                    selectedPositions.append(v)
                    bool1 = True
                newCands = set(G.neighbors(v)) -chosen
                newCands = newCands - set(neighs)
                if bool1:
                    neighs.extend(list(newCands))
                else:
                    neighs = list(newCands) + neighs
                #neighs.extend(list(newCands))
            if len(selectedPositions)<4:
                m = 4 - len(selectedPositions)
                randomPositions = sample(P, m)
                selectedPositions.extend(randomPositions)
            F_current = list(zip([u] * len(selectedPositions), selectedPositions))
            F.extend(F_current)

    if is_weighted:
        F = [(i,j, random.uniform(0, 1)) for (i,j) in F]

    return F

def post_process(G):
    ## if there is any attribute equal to None remove the node
    atts = nx.get_node_attributes(G,'att')
    nodes=[]
    for att in atts:
        if atts[att]!='None':
            nodes.append(att)
    return nx.subgraph(G,nodes)
    ########

def setup(G, p=0.1, k=1, method='F1'):
    G = pre_process(G)
    G = post_process(G)

    P, C = generate_PC(G, p=p, k=k)
    ###
    atts = nx.get_node_attributes(G, 'att')
    for u in P:
        atts[u]='None'
    nx.set_node_attributes(G,atts,'att')
    ##

    F = generate_fitness_function(G, P, list(C.keys()), method=method)

    return G, P, C, F

def save_sampled_graphs(dir, G, name):
    G = pre_process(G)
    G1 = post_process(G)


    percent_list = [0.1, 0.2, 0.3]

    for p in percent_list:
        for i in range(100):
            G = G1.copy()
            position_list, candidate_dict = generate_PC(G, p=p, k=1)
            # number of candidates = number of positions
            candidate_dict_1 = candidate_dict
            # number of candidates = two times the number of positions
            key_list = ['c' + str(i) for i in range(len(candidate_dict_1), 2 * len(candidate_dict_1))]
            candidate_dict_2 = dict(zip(key_list, candidate_dict_1.values()))
            candidate_dict_2.update(candidate_dict_1)
            attribute_dict = nx.get_node_attributes(G, 'att')
            ###save candidate dics into file:
            file1 = open(dir + 'dic/' + name + '(P=' + str(p) + ')(' + str(i) + ')(k=1).txt', 'w')
            for k, v in candidate_dict_1.items():
                file1.write(str(k) + "      " + str(v) + "\n")
            file1.close()
            file1 = open(dir + 'dic/' + name + '(P=' + str(p) + ')(' + str(i) + ')(k=2).txt', 'w')
            for k, v in candidate_dict_2.items():
                file1.write(str(k) + "      " + str(v) + "\n")
            file1.close()

            for u in position_list:
                attribute_dict[u] = 'None'
            nx.set_node_attributes(G, attribute_dict, 'att')
            nx.write_gpickle(G, dir + '/samples/' + name + '(P=' + str(p) + ')(' + str(i) + ").gpickle")
            F = generate_fitness_function(G, position_list, list(candidate_dict_1.keys()), method='F1',
                                          is_weighted=True)
            file1 = open(dir + 'fitness/' + name + '(P=' + str(p) + ')(' + str(i) + ')(k=1)(f=1).txt',
                         'w')
            for (u, v, w) in F:
                file1.writelines(str(u) + '\t' + str(v) + '\t' + str(round(w, 1)) + '\n')
            file1.close()
            F = generate_fitness_function(G, position_list, list(candidate_dict_1.keys()), method='F2',
                                          is_weighted=True)
            file1 = open(dir + 'fitness/' + name + '(P=' + str(p) + ')(' + str(i) + ')(k=1)(f=2).txt',
                         'w')
            for (u, v, w) in F:
                file1.writelines(str(u) + '\t' + str(v) + '\t' + str(round(w, 1)) + '\n')
            file1.close()
            F = generate_fitness_function(G, position_list, list(candidate_dict_2.keys()), method='F1',
                                          is_weighted=True)
            file1 = open(dir + 'fitness/' + name + '(P=' + str(p) + ')(' + str(i) + ')(k=2)(f=1).txt',
                         'w')
            for (u, v, w) in F:
                file1.writelines(str(u) + '\t' + str(v) + '\t' + str(round(w, 1)) + '\n')
            file1.close()
            F = generate_fitness_function(G, position_list, list(candidate_dict_2.keys()), method='F2',
                                          is_weighted=True)
            file1 = open(dir + 'fitness/' + name + '(P=' + str(p) + ')(' + str(i) + ')(k=2)(f=2).txt',
                         'w')
            for (u, v, w) in F:
                file1.writelines(str(u) + '\t' + str(v) + '\t' + str(round(w, 1)) + '\n')
            file1.close()


def read_sampled_graphs(dir, name, pr, i, fitness):
    f = dir + 'samples/' + name + '(P=' + pr + ')(' + str(i) + ').gpickle'
    G = nx.read_gpickle(f)

    candidate_dic = {}
    if fitness<3:
        try:
            with open(dir + 'dic/' + name + '(P=' + pr + ')(' + str(i) + ')(k=1).txt') as f:
                for line in f:
                    (key, val) = line.split()
                    candidate_dic[key] = val
        except:
            with open(dir + 'dic/' + name + '(P=' + pr + ')(' + str(i) + ')(k=1)-Sara’s MacBook Pro.txt') as f:
                for line in f:
                    (key, val) = line.split()
                    candidate_dic[key] = val
    else:
        try:
            with open(dir + 'dic/' + name + '(P=' + pr + ')(' + str(i) + ')(k=2).txt') as f:
                for line in f:
                    (key, val) = line.split()
                    candidate_dic[key] = val
        except:
            with open(dir + 'dic/' + name + '(P=' + pr + ')(' + str(i) + ')(k=2)-Sara’s MacBook Pro.txt') as f:
                for line in f:
                    (key, val) = line.split()
                    candidate_dic[key] = val

    fitness_dic = {}
    position_list = set()

    if fitness ==1:
        try:
            with open(dir + 'fitness/' + name + '(P=' + pr + ')(' + str(i) + ')(k=1)(f=1).txt') as f:
                for line in f:
                    (c, p, w) = line.split()
                    fitness_dic[(c, p)] = float(w)
                    position_list.add(p)
        except:
            with open(dir + 'fitness/' + name + '(P=' + pr + ')(' + str(i) + ')(k=1)(f=1)-Sara’s MacBook Pro.txt') as f:
                for line in f:
                    (c, p, w) = line.split()
                    fitness_dic[(c, p)] = float(w)
                    position_list.add(p)

    elif fitness ==2:
        try:
            with open(dir + 'fitness/' + name + '(P=' + pr + ')(' + str(i) + ')(k=1)(f=2).txt') as f:
                for line in f:
                    (c, p, w) = line.split()
                    fitness_dic[(c, p)] = float(w)
                    position_list.add(p)
        except:
            with open(dir + 'fitness/' + name + '(P=' + pr + ')(' + str(i) + ')(k=1)(f=2)-Sara’s MacBook Pro.txt') as f:
                for line in f:
                    (c, p, w) = line.split()
                    fitness_dic[(c, p)] = float(w)
                    position_list.add(p)

    elif fitness ==3:
        try:
            with open(dir + 'fitness/' + name + '(P=' + pr + ')(' + str(i) + ')(k=2)(f=1).txt') as f:
                for line in f:
                    (c, p, w) = line.split()
                    fitness_dic[(c, p)] = float(w)
                    position_list.add(p)
        except:
            with open(dir + 'fitness/' + name + '(P=' + pr + ')(' + str(i) + ')(k=2)(f=1)-Sara’s MacBook Pro.txt') as f:
                for line in f:
                    (c, p, w) = line.split()
                    fitness_dic[(c, p)] = float(w)
                    position_list.add(p)
    elif fitness ==4:
        try:
            with open(dir + 'fitness/' + name + '(P=' + pr + ')(' + str(i) + ')(k=2)(f=2).txt') as f:
                for line in f:
                    (c, p, w) = line.split()
                    fitness_dic[(c, p)] = float(w)
                    position_list.add(p)
        except:
            with open(dir + 'fitness/' + name + '(P=' + pr + ')(' + str(i) + ')(k=2)(f=2)-Sara’s MacBook Pro.txt') as f:
                for line in f:
                    (c, p, w) = line.split()
                    fitness_dic[(c, p)] = float(w)
                    position_list.add(p)


    position_list = list(position_list)

    return G, position_list, candidate_dic, fitness_dic








