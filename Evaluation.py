
import matplotlib.pyplot as plt
import numpy as np
plt.rc('xtick', labelsize=30)
plt.rc('ytick', labelsize=30)
plt.rc('axes', titlesize=30)     # fontsize of the axes title
plt.rc('axes', labelsize=30)    # fontsize of the x and y labels
import statistics as st
import networkx as nx
import Setup as Setup
#import PostProcess as PP
from community import community_louvain
from collections import defaultdict
import math

def evaluate(G, P_set, F, matched=[], success=True):
    score=0
    if success:
        for (u, v) in matched:
            if u in P_set:
                p = u
                c = v
            else:
                c = u
                p = v
            if (c, p) in F:
                score += float(F[(c, p)])


    average1, mean1, communities = support_group_score(G)
    return round(nx.attribute_assortativity_coefficient(G, 'att'),2),\
           round(score,2),\
           round(average1,2)

def support_group_score(G):
    att_dic = nx.get_node_attributes(G, 'att')

    communities = community_louvain.best_partition(G)
    communities_dic = defaultdict(list)
    for key, value in sorted(communities.items()):
        communities_dic[value].append(key)

    results=[]
    min_result=1

    for k, v in communities_dic.items():
        count = 0
        male = 0
        female = 0
        for u in v:
            gen = att_dic[u]
            count += 1
            if gen == 'male':
                male += 1
            elif gen == 'female':
                female += 1
        n1 = male/count
        n2 = female/count

        n = min(n1,n2)
        min_result= min(min_result,n)
        results.append(n)

    return st.mean(results), min_result, communities_dic

def measure_threshold(graph_name, dir):
    p_list = ['0.1', '0.2', '0.3']

    fitness_list = [1, 2, 3, 4]
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
                            stats = evaluate(G2, set(position_list), fitness_dic, matched=M, success=True)
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

    fitness_list = [1, 2, 3, 4]
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

                G0 = G.subgraph(nodes)
                if len(G0) > 0:
                    stats = evaluate(G0, set(position_list), fitness_dic, success=False)
                    results1[0].append(stats[0])
                    results1[1].append(stats[1])
                    results1[2].append(stats[2])

                methods = [1, 2, 5, 6, 7, 8]
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
                            stats = evaluate(G2, set(position_list), fitness_dic, matched=M, success=True)
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



def measure_brute(graph_name, dir):
    p_list = ['0.1']

    fitness_list = [1, 2]
    kk = 100
    final_file = open(dir + 'stats/stats_'+ graph_name+'brut2.txt' ,'w')
    for f in fitness_list:
        for pr in p_list:
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

                G0 = G.subgraph(nodes)
                if len(G0) > 0:
                    stats = evaluate(G0, set(position_list), fitness_dic, success=False)
                    results1[0].append(stats[0])
                    results1[1].append(stats[1])
                    results1[2].append(stats[2])

                methods = [40, 41, 42, 43, 1]
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
                            stats = evaluate(G2, set(position_list), fitness_dic, matched=M, success=True)
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



def generate_appendix_tables(dir, graph_name_list):

    file1 =open(dir +'tables/c1f1.txt', 'w')
    file2 =open(dir +'tables/c1f2.txt', 'w')
    file3 =open(dir +'tables/c2f1.txt', 'w')
    file4 =open(dir +'tables/c2f2.txt', 'w')


    for name in graph_name_list:
        file1.writelines(name + '\n')
        file2.writelines(name + '\n')
        file3.writelines(name + '\n')
        file4.writelines(name + '\n')

        file_1 = dir + 'stats/stat_' + name + '.txt'
        file_2 = dir + 'stats/stat_' + name + '_threshold.txt'
        lines = [[[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []],
                 [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []]]

        j=0
        nots = [1, 2, 3, 4, 6, 0, 11]
        with open(file_1) as fp:
            line = fp.readline()
            cnt = 0
            while line:
                cnt += 1
                i = cnt%12
                j = int((cnt-1)/36)
                if i not in nots:
                    line = line.split('[')[-1]
                    line = line.split(']')[0]
                    line = line.split(',')
                    line = [line[1], line[0], line[2]]
                    line =['&' + item for item in line]
                    line = ''.join(line)
                    if i == 5:
                        lines[j][0].append(line)
                    elif i == 7:
                        lines[j][1].append(line)
                    elif i == 8:
                        lines[j][6].append(line)
                    elif i == 9:
                        lines[j][7].append(line)
                    elif i == 10:
                        lines[j][8].append(line)
                line = fp.readline()

        j = 0
        nots = [1, 2, 3]
        with open(file_2) as fp:
            line = fp.readline()
            cnt = 0
            while line:
                cnt += 1
                i = cnt % 7
                j = int((cnt-1)/21)
                if i not in nots:
                    line = line.split('[')[-1]
                    line = line.split(']')[0]
                    line = line.split(',')
                    line = [line[1], line[0], line[2]]
                    line = ['&' + item for item in line]
                    line = ''.join(line)
                    if i == 4:
                        lines[j][2].append(line)
                    elif i == 5:
                        lines[j][3].append(line)
                    elif i == 6:
                        lines[j][4].append(line)
                    elif i == 0:
                        lines[j][5].append(line)
                line = fp.readline()


        x=0

        current = lines[0]

        for item in current:
            l=''.join(item)
            file1.writelines(l +'\n')

        current = lines[1]
        for item in current:
            l = ''.join(item)
            file2.writelines(l +'\n')

        current = lines[2]
        for item in current:
            l = ''.join(item)
            file3.writelines(l +'\n')

        current = lines[3]
        for item in current:
            l = ''.join(item)
            file4.writelines(l +'\n')


    file1.close()
    file2.close()
    file3.close()
    file4.close()


def generate_plots_exp1_per(dir, graph_name_list):
    #graph_name_list = ['CC(L)', 'CC(H)', 'RT(L)', 'RT(H)', 'Nor(L)', 'Nor(M)', 'nor1high',  'd1(250)', 'f1(250)', 'g0(-1)', 'g0(1)', 'g0(0)',]
    #names = ['CC(M)', 'CC(H)', 'RT(M)', 'RT(H)', 'Nor(L)', 'Nor(M)', 'Nor(H)',  'DO(H)', 'FO(H)', 'SF(M)','SF(H)', 'SF(L)',]
    k=-1
    for name in graph_name_list:
        k+=1
        print(name)
        results = ['1_1', '1_2', '1_3', '2_1', '2_2', '2_3', '3_1', '3_2', '3_3', '4_1', '4_2', '4_3']
        markers =['*', 'h', 'o','^','D', '<','s', 'd','x']
        org=[[],[]]
        fa =[[],[]]
        rnd=[[],[]]
        hng=[[],[]]
        opt=[[],[]]
        high=[[],[]]
        low=[[],[]]
        optim=[[],[]]

        file_1 = dir + 'stats/stat_' + name + '.txt'

        nots = [1, 2, 3, 4, 6]
        with open(file_1) as fp:
            line = fp.readline()
            cnt = 0
            while line:
                cnt += 1
                i = cnt % 12
                j = int((cnt - 1) / 36)
                if i not in nots:
                    line = line.split('[')[-1]
                    line = line.split(']')[0]
                    line = line.split(',')
                    assort =float(line[0])
                    score =float(line[1])
                    if i == 5:
                        org[0].append(assort)
                        org[1].append(score)
                    elif i == 8:
                        rnd[0].append(assort)
                        rnd[1].append(score)
                    elif i == 10:
                        opt[0].append(assort)
                        opt[1].append(score)
                    elif i == 9:
                        hng[0].append(assort)
                        hng[1].append(score)
                    elif i == 11:
                        high[0].append(assort)
                        high[1].append(score)
                        optim[1].append(score)
                    elif i == 0:
                        low[0].append(assort)
                        low[1].append(score)
                    elif i == 7:
                        fa[0].append(assort)
                        fa[1].append(score)
                line = fp.readline()

        for i in range(len(org[0])):
            optim[0].append(min(abs(org[0][i]), abs(rnd[0][i]), abs(opt[0][i]), abs(hng[0][i]), abs(high[0][i]), abs(low[0][i]), abs(fa[0][i])))

        for i in range(len(results)):
            xs=[]
            ys=[]
            if fa[0][i] != -1:
                xs.append((abs(org[0][i]) - abs(optim[0][i]))/abs(org[0][i]))
                ys.append((optim[1][i] - low[1][i]) / (high[1][i] - low[1][i]))
            else:
                xs.append(-1)
                ys.append(-1)
            if fa[0][i] != -1:
                xs.append((abs(org[0][i]) - abs(fa[0][i]))/abs(org[0][i]))
                ys.append((fa[1][i] - low[1][i]) / (high[1][i] - low[1][i]))
            else:
                xs.append(-1)
                ys.append(-1)
            if rnd[0][i] != -1:
                xs.append((abs(org[0][i]) - abs(rnd[0][i]))/abs(org[0][i]))
                ys.append((rnd[1][i] - low[1][i]) / (high[1][i] - low[1][i]))
            else:
                xs.append(-1)
                ys.append(-1)
            if hng[0][i]!= -1:
                xs.append((abs(org[0][i]) - abs(hng[0][i]))/abs(org[0][i]))
                ys.append((hng[1][i] - low[1][i]) / (high[1][i] - low[1][i]))
            else:
                xs.append(-1)
                ys.append(-1)
            if opt[0][i] !=-1:
                xs.append((abs(org[0][i]) - abs(opt[0][i]))/abs(org[0][i]))
                ys.append((opt[1][i] - low[1][i]) / (high[1][i] - low[1][i]))
            else:
                xs.append(-1)
                ys.append(-1)



            for j in range(len(xs)):
                x = [round(xs[j]*100)]
                y = [round(ys[j]*100, 1)]
                if x != [-1] and y != [-1]:
                    plt.scatter(x, y, s=1000, marker=markers[j])


            plt.xlabel('Improvements in Assortativity')
            plt.ylabel('Improvements in Quality')
            plt.title(graph_name_list[k])
            plt.savefig(dir +'plots/2' + name + '(' + results[i] + ').png')
            plt.savefig(dir+'plots/2' + name + '(' + results[i] + ').pdf')
            plt.close()

def generate_table_exp1(dir, graph_name_list):

    file1 =open(dir +'tables/table1.txt', 'w')
    lines_0 = [[[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]],[[],[]],[[],[]],[[],[]]]
    lines_1 = [[[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]],[[],[]],[[],[]],[[],[]]]
    lines_2 = [[[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]],[[],[]],[[],[]],[[],[]]]
    lines_3 = [[[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]],[[],[]],[[],[]],[[],[]]]
    lines_4 = [[[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]],[[],[]],[[],[]],[[],[]]]
    lines_5 = [[[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]],[[],[]],[[],[]],[[],[]]]
    lines_6 = [[[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]],[[],[]],[[],[]],[[],[]]]



    for name in graph_name_list:

        file_1 = dir + 'stats/stat_' + name + '.txt'
        nots = [1, 2, 3, 4, 6]
        with open(file_1) as fp:
            line = fp.readline()
            cnt = 0
            while line:
                cnt += 1
                i = cnt%12
                j = int((cnt-1)/12)
                if i not in nots:
                    line = line.split('[')[-1]
                    line = line.split(']')[0]
                    line = line.split(',')
                    if True:
                        #line = [abs(float(line[3])), abs(float(line[0])), abs(float(line[1]))]
                        if i == 5:
                            lines_0[j][0].append(float(line[0]))
                            lines_0[j][1].append(float(line[1]))
                         #   lines_0[j][2].append(line[2])
                        elif i == 7:
                            lines_1[j][0].append(float(line[0]))
                            lines_1[j][1].append(float(line[1]))
                         #   lines_2[j][2].append(line[2])
                        elif i == 8:
                            lines_2[j][0].append(float(line[0]))
                            lines_2[j][1].append(float(line[1]))
                        #    lines_4[j][2].append(line[2])
                        elif i == 9:
                            lines_3[j][0].append(float(line[0]))
                            lines_3[j][1].append(float(line[1]))
                         #   lines_3[j][2].append(line[2])
                        elif i == 10:
                            lines_4[j][0].append(float(line[0]))
                            lines_4[j][1].append(float(line[1]))
                        elif i == 11:
                            lines_5[j][0].append(float(line[0]))
                            lines_5[j][1].append(float(line[1]))
                        elif i == 0:
                            lines_6[j][0].append(float(line[0]))
                            lines_6[j][1].append(float(line[1]))
                          #  lines_1[j][2].append(line[2])
                line = fp.readline()

    line_0 =[]
    line_1 =[]
    line_2 =[]
    line_3 =[]
    line_4 =[]


    for i in range(12):
        #x =lines_1[i][0]
        for j in range(len(lines_1[i][0])):
            x= lines_1[i][0][j]
            lines_1[i][0][j] = round((abs(lines_0[i][0][j]) - abs(lines_1[i][0][j])) / abs(lines_0[i][0][j]), 2)
            lines_1[i][1][j] = round((abs(lines_1[i][1][j]) - abs(lines_6[i][1][j])) / (abs(lines_5[i][1][j]) - abs(lines_6[i][1][j])),
                                  2)

            lines_2[i][0][j] = round((abs(lines_0[i][0][j]) - abs(lines_2[i][0][j])) / abs(lines_0[i][0][j]), 2)
            lines_2[i][1][j] = round((abs(lines_2[i][1][j]) - abs(lines_6[i][1][j])) / (abs(lines_5[i][1][j]) - abs(lines_6[i][1][j])),
                                  2)
            lines_3[i][0][j] = round((abs(lines_0[i][0][j]) - abs(lines_3[i][0][j])) / abs(lines_0[i][0][j]), 2)
            lines_3[i][1][j] = round((abs(lines_3[i][1][j]) - abs(lines_6[i][1][j])) / (abs(lines_5[i][1][j]) - abs(lines_6[i][1][j])),
                                  2)
            if lines_4[i][0][j] !=-1:
                lines_4[i][0][j] = round((abs(lines_0[i][0][j]) - abs(lines_4[i][0][j])) / abs(lines_0[i][0][j]), 2)
                lines_4[i][1][j] = round((abs(lines_4[i][1][j]) - abs(lines_6[i][1][j])) / (abs(lines_5[i][1][j]) - abs(lines_6[i][1][j])),
                                  2)

    for item in lines_0:
        l=[]
        for i in item:
            l.append(round(st.mean(i),2)*100)
        line_0.append([l[1],l[0]])


    for item in lines_1:
        l = []
        for i in item:
            l.append(round(st.mean(i),2)*100)
        line_1.append([l[1],l[0]])

    for item in lines_2:
        l = []
        for i in item:
            l.append(round(st.mean(i),2)*100)
        line_2.append([l[1],l[0]])

    for item in lines_3:
        l = []
        for i in item:
            l.append(round(st.mean(i),2)*100)
        line_3.append([l[1], l[0]])

    for item in lines_4:
        l = []
        for i in item:
            i = [x for x in i if x != -1]
            if len(i)>0:
                l.append(round(st.mean(i),2)*100)
            else:
                l=[-1,-1]
        line_4.append([l[1], l[0]])

    i=0
    while i<len(line_0):
        '''
        l1 = line_0[i]
        l1 = ['&' + str(int(l)) for l in l1]
        l2 = line_0[i+1]
        l2 = ['&' + str(int(l))for l in l2]
        l3 = line_0[i+2]
        l3 = ['&' + str(int(l)) for l in l3]
        l = ''.join(l1) + ''.join(l2) +''.join(l3)
        file1.writelines(l + '\n')
        '''

        l1 = line_1[i]
        l1 = ['&' + str(int(l)) for l in l1]
        l2 = line_1[i+1]
        l2 = ['&' + str(int(l)) for l in l2]
        l3 = line_1[i+2]
        l3 = ['&' + str(int(l)) for l in l3]
        l = ''.join(l1) + ''.join(l2) + ''.join(l3)
        file1.writelines(l + '\n')

        l1 = line_2[i]
        l1 = ['&' + str(int(l)) for l in l1]
        l2 = line_2[i+1]
        l2 = ['&' + str(int(l)) for l in l2]
        l3 = line_2[i+2]
        l3 = ['&' + str(int(l)) for l in l3]
        l = ''.join(l1) + ''.join(l2) + ''.join(l3)
        file1.writelines(l + '\n')

        l1 = line_3[i]
        l1 = ['&' + str(int(l)) for l in l1]
        l2 = line_3[i+1]
        l2 = ['&' + str(int(l)) for l in l2]
        l3 = line_3[i+2]
        l3 = ['&' + str(int(l)) for l in l3]
        l = ''.join(l1) + ''.join(l2) + ''.join(l3)
        file1.writelines(l + '\n')

        l1 = line_4[i]
        l1 = ['&' + str(int(l)) for l in l1]
        l2 = line_4[i+1]
        l2 = ['&' + str(int(l)) for l in l2]
        l3 = line_4[i+2]
        l3 = ['&' + str(int(l)) for l in l3]
        l = ''.join(l1) + ''.join(l2) + ''.join(l3)
        file1.writelines(l + '\n')
        i+=3

    file1.close()


def generate_plots_exp2(dir,graph_name_list):
    jj=-1
    for name in graph_name_list:
        print(name)
        jj+=1
        file_1 = dir + 'stats/stat_' + name + '.txt'
        file_2 = dir + 'stats/stat_' + name + '_threshold.txt'
        lines = [[[], [],[],[],[], []],
                 [[], [], [], [], [], []],
                 [[], [], [], [], [], []],
                 [[], [],[],[],[], []]]
        lines_h = [[[], [], []],
                 [[], [], []],
                 [[], [], []],
                 [[], [], []]]
        lines_l = [[[], [], []],
                 [[], [], []],
                 [[], [], []],
                 [[], [], []]]

        j=0
        with open(file_1) as fp:
            line = fp.readline()
            cnt = 0
            while line:
                cnt += 1
                i = cnt%12
                j = int((cnt-1)/36)
                if i ==7:
                    line = line.split('[')[-1]
                    line = line.split(']')[0]
                    line = line.split(',')
                    line = [float(line[1]), float(line[0]), float(line[2])]
                    #line =['&' + item for item in line]
                    #line = ''.join(line)
                    lines[j][0].append(line)
                elif i == 11:
                    line = line.split('[')[-1]
                    line = line.split(']')[0]
                    line = line.split(',')
                    line = [float(line[1]), float(line[0]), float(line[2])]
                    # line =['&' + item for item in line]
                    # line = ''.join(line)
                    lines_h[j][0].append(line)
                elif i == 0:
                    line = line.split('[')[-1]
                    line = line.split(']')[0]
                    line = line.split(',')
                    line = [float(line[1]), float(line[0]), float(line[2])]
                    # line =['&' + item for item in line]
                    # line = ''.join(line)
                    lines_l[j][0].append(line)
                elif i  ==5:
                    line = line.split('[')[-1]
                    line = line.split(']')[0]
                    line = line.split(',')
                    line = [float(line[1]), float(line[0]), float(line[2])]
                    # line =['&' + item for item in line]
                    # line = ''.join(line)
                    lines[j][-1].append(line)
                line = fp.readline()

        j = 0
        nots = [1, 2, 3]
        with open(file_2) as fp:
            line = fp.readline()
            cnt = 0
            while line:
                cnt += 1
                i = cnt % 7
                j = int((cnt-1)/21)
                if i not in nots:
                    line = line.split('[')[-1]
                    line = line.split(']')[0]
                    line = line.split(',')
                    line = [float(line[1]), float(line[0]), float(line[2])]

                    #line = [float(line[3]), float(line[0]), float(line[1]), float(line[4])]
                    #line = ['&' + item for item in line]
                    #line = ''.join(line)
                    if i == 4:
                        lines[j][1].append(line)
                    elif i == 5:
                        lines[j][2].append(line)
                    elif i == 6:
                        lines[j][3].append(line)
                    elif i == 0:
                        lines[j][4].append(line)
                line = fp.readline()


        for i in range(4):
            for k in range(3):
                for j in range(5):
                    a=  lines_l[i][0][k][0]
                    b= lines_h[i][0][k][0]
                    lines[i][j][k][0] = round((lines[i][j][k][0] - lines_l[i][0][k][0])/(lines_h[i][0][k][0]-lines_l[i][0][k][0]),2)
                    a = lines[i][j][k][1]
                    b = lines[i][-1][k][1]
                    lines[i][j][k][1] = round((abs(lines[i][-1][k][1]) - abs(lines[i][j][k][1]))/abs(lines[i][-1][k][1]) ,2)


       # plt.rc('xtick', labelsize=7)
       # plt.rc('ytick', labelsize=7)
        # plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
        #plt.rc('axes', titlesize=8)  # fontsize of the axes title
        #plt.rc('axes', labelsize=8)
        width = 0.2
        plt.rc('xtick', labelsize=20)
        plt.rc('ytick', labelsize=20)
        plt.rc('axes', titlesize=30)  # fontsize of the axes title
        plt.rc('axes', labelsize=30)

        for i in range(4):
            l = lines[i]
            l = l[:-1]
            for j in range(3):
                data1=[
                   #int(l[-1][j][0]*100),int(l[0][j][0]*100),int(l[1][j][0]*100),int(l[2][j][0]*100),int(l[3][j][0]*100),int(l[4][j][0]*100)
                    int(l[0][j][0] * 100), int(l[1][j][0] * 100), int(l[2][j][0] * 100), int(l[3][j][0] * 100), int(l[4][j][0] * 100)
                ]
                data2 = [
                #int(l[-1][j][1]*100),int(l[0][j][1]*100),int(l[1][j][1]*100), int(l[2][j][1]*100), int(l[3][j][1]*100), int(l[4][j][1]*100)
                int(l[0][j][1]*100),int(l[1][j][1]*100), int(l[2][j][1]*100), int(l[3][j][1]*100), int(l[4][j][1]*100)
                ]

                #data3 = [int(l[-1][j][-1]*100),int(l[0][j][-1]*100),int(l[1][j][-1]*100), int(l[2][j][-1]*100), int(l[3][j][-1]*100), int(l[4][j][-1]*100)]
                data3 = [int(l[0][j][-1]*100),int(l[1][j][-1]*100), int(l[2][j][-1]*100), int(l[3][j][-1]*100), int(l[4][j][-1]*100)]

                plt.bar(np.arange(len(data1)), data1, width=width)
                plt.bar(np.arange(len(data2)) + width, data2, width=width)
                plt.bar(np.arange(len(data3)) + width + width, data3, width=width)
                # plt.bar(np.arange(len(data4)) + width + width + width, data4, width=width)

                #plt.xticks(np.arange(len(data1)) + width, ['Org','0', '2', '0.05*|ki|', '0.1*|ki|', '0.2*|ki|'])
                #plt.xticks(np.arange(len(data1)) + width, ['','', '', '', '', ''])
                plt.xticks(np.arange(len(data1)) + width, ['0', '2', '0.05|ki|', '0.1|ki|', '0.2|ki|'])

                #plt.xlabel("Threshold")
                plt.title(graph_name_list[jj])
                # plt.ylabel("Energy Output (GJ)")
                plt.savefig(dir + 'plots/' + name + '(' + str(i)+str(j) + ').png')
                plt.savefig(dir + 'plots/' + name + '(' + str(i)+str(j) + ').pdf')
                plt.close()


