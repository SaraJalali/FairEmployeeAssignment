import networkx as nx
import Setup as Setup
import Assignment as FA
import Evaluation as EV
import statistics as st
from community import community_louvain
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

#step1 : read datasets and generate samples with

def gen_samples(dir,graph_name_list):
    for name in graph_name_list:
        print(name)
        graph_dir = dir +'datasets/' + name + '.gpickle'
        G = nx.read_gpickle(graph_dir)
        gender2 = nx.get_node_attributes(G, 'att')
        if len(gender2) == 0:
            gender1 = nx.get_node_attributes(G, 'gender')
            nx.set_node_attributes(G, gender1, 'att')
        Setup.save_sampled_graphs(dir, G, name)

def gen_fitness(name, position_list,candidate_dic):
    position_dic = dict(zip(position_list, candidate_dic.keys()))
    if 'CC' in name:
        dir1 = dir + 'datasets/2.txt'
    else:
        dir1 = dir + 'datasets/1.txt'

    with open(dir1, 'r') as f:
        line = f.readline()
        att = line.split()
        l = range(1, len(att)+1)
        l= [str(item) for item in l]
        att_dic= dict(zip(l, att))

    output={}
    for i in position_dic.keys():
        cand = position_dic[i]
        for j in position_dic.keys():
            if att_dic[i] == att_dic[j]:
                output[(cand,str(j))] =1.0

    return output

def gen_fitness_team(name, position_list,candidate_dic,G):
    communities = community_louvain.best_partition(G)
    position_dic = dict(zip(position_list, candidate_dic.keys()))
    if 'CC' in name:
        dir1 = dir + 'datasets/2.txt'
    else:
        dir1 = dir + 'datasets/1.txt'

    with open(dir1, 'r') as f:
        line = f.readline()
        att = line.split()
        l = range(1, len(att)+1)
        l= [str(item) for item in l]
        att_dic= dict(zip(l, att))

    output={}
    for i in position_dic.keys():
        cand = position_dic[i]
        for j in position_dic.keys():
            if att_dic[i] == att_dic[j] and communities[i]==communities[j]:
                output[(cand,str(j))] =1.0

    return output




def assign_diversity(graph_name_list, method, dir, weight_prob=[],pp=0):
    p_list =['0.1', '0.2', '0.3']
    kk = 100
    for i in range(kk):
        print(i)
        for name in graph_name_list:
            G1 = nx.read_gpickle(dir + 'datasets/' + name + '.gpickle')
            G1 = Setup.pre_process(G1)
            for pr in p_list:
                G = G1.copy()
                position_list, candidate_dic = Setup.generate_PC(G.copy(), p=float(pr),k=1)
                att= nx.get_node_attributes(G, 'att')
                for node in position_list:
                    att[node] ='None'
                nx.set_node_attributes(G, att, 'att')
                position_list = [str(item) for item in position_list]
                fitness_dic = gen_fitness_team(name,position_list,candidate_dic,G)
                if pp == 0:
                    name_new = dir + 'Results/' + name + '(P=' + pr + ')(f=' + str(
                        1) + ')(method=' + str(
                        method) + ')(weight=' + str(weight_prob) + ')(' + str(i) + ')'
                else:
                    name_new = dir + 'Results/' + name + '(P=' + pr + ')(f=' + str(
                        1) + ')(method=' + str(
                        method) + ')(weight=' + str(pp) + ')(' + str(i) + ')'

                G_new, M = FA.assignment(candidate_dic.copy(), position_list.copy(),
                                                 fitness_dic.copy(),G,method=method, weight_probability=weight_prob.copy(),kk=pp)
                file = open(name_new + '.txt', 'w')
                for (u, v) in M:
                    file.writelines(str(u) + '\t' + str(v) + '\n')
                file.close()
                nx.write_gpickle(G_new, name_new + '.gpickle')


def assign_diversity_bruteforth(graph_name_list, method, dir, weight_prob=[]):
    p_list = ['0.1']
    fitness_list = [1,2]
    kk = 2
    for graph_name in graph_name_list:
        name = (graph_name.split('/')[-1]).replace('.gpickle', '')
        print('#####################################################')
        print(name)
        for f in fitness_list:
            print('#####################################################')
            print(f)
            for pr in p_list:
                print('#####################################################')
                print(pr)
                for i in range(kk):
                    print(i)
                    flag= False
                    weight_prob1 = [1,1,0]
                    name_new = dir + 'Results/' + name + '(P=' + pr + ')(f=' + str(
                        f) + ')(method=' + str(
                        40) + ')(weight=' + str(weight_prob1) + ')(' + str(i) + ')'
                    try:
                        nx.read_gpickle(name_new + '.gpickle')
                    except:
                        flag=True

                    if flag:
                        G, position_list, candidate_dic, fitness_dic = Setup.read_sampled_graphs(dir, name,pr,i,f)
                        Gs = FA.assignment(candidate_dic.copy(), position_list.copy(),
                                                 fitness_dic.copy(),G,method=method, weight_probability=weight_prob)

                        j = 0
                        for G_new, M in Gs:
                            name_new = dir + 'Results/' + name + '(P=' + pr + ')(f=' + str(
                                f) + ')(method=' + str(
                                method) + str(j) + ')(weight=' + str(weight_prob) + ')(' + str(
                                i) + ')'  # .gpickle'
                            j += 1
                            file = open(name_new + '.txt', 'w')

                            for (u, v) in M:
                                file.writelines(str(u) + '\t' + str(v) + '\n')
                            file.close()

                            nx.write_gpickle(G_new, name_new + '.gpickle')


#evaluation
def measure_threshold(graph_name, dir):
    p_list = ['0.1', '0.2', '0.3']

    fitness_list = [1]
    kk = 100
    final_file = open(dir + 'stats/stat_'+ graph_name+'_threshold.txt' ,'w')
    for f in fitness_list:
        for pr in p_list:
            print(pr)
            results2 = [[[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []]]
            for i in range(kk):
                G, position_list, candidate_dic, fitness_dic = Setup.read_sampled_graphs(dir, graph_name, pr, i, f)
                weights = [2, 0.05, 0.1, 0.2]
                kkk = len(weights)
                for j in range(kkk):
                    method = 1
                    weight_prob = weights[j]
                    fil = 'Results'

                    f2 = dir + fil + '/' + graph_name + '(P=' + pr + ')(f=' + str(f) + ')(method=' + str(
                        method) + ')(weight=' + str(
                        weight_prob) + ')(' + str(i) + ')'  # .gpickle'
                    try:
                        G2 = nx.read_gpickle(f2 + '.gpickle')

                        M = []
                        with open(f2 + '.txt') as ff:
                            content = ff.readlines()
                            for item in content:
                                u = item.split('\t')
                                M.append((u[0], u[1].split('\n')[0]))

                        ff.close()

                        if len(M) > 0:
                            stats = EV.evaluate(G2, set(position_list), fitness_dic, matched=M, success=True)
                            results2[j][0].append(stats[0])
                            results2[j][1].append(stats[1])
                            results2[j][2].append(stats[2])

                    except:
                        print(f2)

            for i in range(len(results2[0])):
                for j in range(kkk):
                    if len(results2[j][i]) > 0:
                        results2[j][i] = round(st.mean(results2[j][i]), 2)
                    else:
                        results2[j][i] = -1

            final_file.writelines('#########################' + '\n')
            final_file.writelines('fitness:          ' + str(f) + '\n')
            final_file.writelines('Probability:      ' + str(pr) + '\n')

            for ll in range(kkk):
                item = results2[ll]
                final_file.writelines(str(weights[ll]))
                ll += 1
                final_file.writelines(str(item) + '\n')


def measure(graph_name, dir):
    p_list = ['0.1', '0.2', '0.3']

    fitness_list = [1]
    kk = 100
    final_file = open(dir + 'stats/stat_'+ graph_name+'.txt' ,'w')
    for f in fitness_list:
        for pr in p_list:
            print(pr)
            results1 = [[], [], []]
            results2 = [[[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []],
                        [[], [], []]]
            for i in range(kk):
                G, position_list, candidate_dic, fitness_dic = Setup.read_sampled_graphs(dir, graph_name, pr, i, f)
                nodes = []
                gender = nx.get_node_attributes(G, 'att')
                for u in G.nodes():
                    if gender[u] != 'None':
                        nodes.append(u)

                G0 = nx.read_gpickle(dir + 'datasets/' + name + '.gpickle')

                if len(G0) > 0:
                    stats = EV.evaluate(G0, set(position_list), fitness_dic, success=False)
                    results1[0].append(stats[0])
                    results1[1].append(stats[1])
                    results1[2].append(stats[2])

                methods = [1]
                kkk = len(methods)
                for j in range(kkk):
                    method = methods[j]
                    weight_prob = [1, 1, 0]
                    fil = 'Results'

                    f2 = dir + fil + '/' + graph_name + '(P=' + pr + ')(f=' + str(f) + ')(method=' + str(
                        method) + ')(weight=' + str(
                        weight_prob) + ')(' + str(i) + ')'  # .gpickle'
                    try:
                        G2 = nx.read_gpickle(f2 + '.gpickle')

                        M = []
                        with open(f2 + '.txt') as ff:
                            content = ff.readlines()
                            for item in content:
                                u = item.split('\t')
                                M.append((u[0], u[1].split('\n')[0]))

                        ff.close()

                        if len(M) > 0:
                            stats = EV.evaluate(G2, set(position_list), fitness_dic, matched=M, success=True)
                            results2[j][0].append(stats[0])
                            results2[j][1].append(stats[1])
                            results2[j][2].append(stats[2])

                    except:
                        print(f2)

            for i in range(len(results1)):
                results1[i] = round(st.mean(results1[i]), 2)

            for i in range(len(results2[0])):
                for j in range(kkk):
                    if len(results2[j][i]) > 0:
                        results2[j][i] = round(st.mean(results2[j][i]), 2)
                    else:
                        results2[j][i] = -1

            final_file.writelines('#########################' + '\n')
            final_file.writelines('fitness:          ' + str(f) + '\n')
            final_file.writelines('Probability:      ' + str(pr) + '\n')

            final_file.writelines('Before' + '\n')
            final_file.writelines(str(results1) + '\n')
            final_file.writelines('after' + '\n')
            for ll in range(kkk):
                item = results2[ll]
                final_file.writelines(str(methods[ll]))
                ll += 1
                final_file.writelines(str(item) + '\n')



def generate_plots(dir,graph_name_list):
    jj=-1
    for name in graph_name_list:
        print(name)
        jj+=1
        file_2 = dir + 'stats/stat_' + name + '_threshold.txt'
        lines=[[], [],[],[],[], []]

        nots = [0]
        with open(file_2) as fp:
            line = fp.readline()
            cnt = -1
            while line:
                cnt += 1
                i = cnt % 7
                if i not in nots:
                    line = line.split('[')[-1]
                    line = line.split(']')[0]
                    line = line.split(',')
                    line = [float(line[0]), float(line[2])]


                    if i == 1:
                        lines[0].append(line)
                    elif i == 2:
                        lines[1].append(line)
                    elif i == 3:
                        lines[2].append(line)
                    elif i == 4:
                        lines[3].append(line)
                    elif i == 5:
                        lines[4].append(line)
                    elif i == 6:
                        lines[5].append(line)
                    elif i == 7:
                        lines[6].append(line)
                line = fp.readline()


        width = 0.2
        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=20)
        plt.rc('axes', titlesize=30)  # fontsize of the axes title
        plt.rc('axes', labelsize=30)

        l = lines
        if True:
            for j in range(3):
                data2 = [
                (l[0][j][0]),(l[1][j][0]), (l[2][j][0]), (l[3][j][0]), (l[4][j][0]), (l[5][j][0])
                ]

                data3 = [(l[0][j][-1]),(l[1][j][-1]), (l[2][j][-1]), (l[3][j][-1]), (l[4][j][-1]), (l[5][j][-1])]

                plt.bar(np.arange(len(data2)) , data2, width=width)
                plt.bar(np.arange(len(data3)) + width, data3, width=width)

                plt.xticks(np.arange(len(data2)) + width, ['org','0', '2', '0.05|ki|', '0.1|ki|', '0.2|ki|'])

                plt.title(graph_name_list[jj])
                plt.savefig(dir + 'plots/' + name + '(' + str(j) + ').png')
                plt.savefig(dir + 'plots/' + name + '(' + str(j) + ').pdf')
                plt.close()



dir= 'DS/'

graph_name_list = ['CC(M)', 'CC(H)', 'RT(M)', 'RT(H)']


'''
print(graph_name_list)
#gen_samples(dir,graph_name_list)
#no threshold results of FairEmployeeAssignment and baseline methods
methods =[1]
for method in methods:
    print(method)
    assign_diversity(graph_name_list, method=1, dir=dir, weight_prob=[1,1,0])

t=[2,0.05, 0.1, 0.2]
for k in t:
    print("k====" +str(k))
    assign_diversity(graph_name_list, method=1, dir=dir, weight_prob=[1,1,1],pp=k)




for name in graph_name_list:
    measure(name, dir)
    measure_threshold(name, dir)
'''

generate_plots(dir, graph_name_list)

