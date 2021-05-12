import networkx as nx
import Setup as Setup
import Assignment as FA
import Evaluation as EV



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




def assign_diversity(graph_name_list, method, dir, weight_prob=[],pp=0):
    p_list =['0.1', '0.2', '0.3']
    fitness_list =[1, 2 ,3 ,4]
    kk = 5
    for i in range(kk):
        print(i)
        for graph_name in graph_name_list:
            name = (graph_name.split('/')[-1]).replace('.gpickle', '')
            for f in fitness_list:
                for pr in p_list:
                    flag= False
                    if pp==0:
                        name_new = dir + 'Results/' + name + '(P=' + pr + ')(f=' + str(
                            f) + ')(method=' + str(
                            method) + ')(weight=' + str(weight_prob) + ')(' + str(i) + ')'
                    else:
                        name_new = dir + 'Results/' + name + '(P=' + pr + ')(f=' + str(
                            f) + ')(method=' + str(
                            method) + ')(weight=' + str(pp) + ')(' + str(i) + ')'
                    try:
                        nx.read_gpickle(name_new + '.gpickle')
                    except:
                        flag=True

                    if flag:
                        G, position_list, candidate_dic, fitness_dic = Setup.read_sampled_graphs(dir, name,pr,i,f)
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


dir= 'DS/'

graph_name_list = [['CC(M)'], ['CC(H)'], ['RT(M)'], ['RT(H)'], ['Nor(L)'], ['Nor(M)'], ['Nor(H)'],  ['DO(H)'], ['FO(H)'], ['SF(M)'],['SF(H)'], ['SF(L)']]


print(graph_name_list)
gen_samples(dir,graph_name_list)
#no threshold results of FairEmployeeAssignment and baseline methods
methods =[1,2,5,6,7,8]
for method in methods:
    print(method)
    assign_diversity(graph_name_list, method=method, dir=dir, weight_prob=[1,1,0])

#bruteforth results
methods = [3,4]
for method in methods:
    print(method)
    assign_diversity_bruteforth(graph_name_list, method=method, dir=dir, weight_prob=[1,1,0])
#results with threshold for FairEmployeeAssignment
t=[2,0.05, 0.1, 0.2]
for k in t:
    assign_diversity(graph_name_list, method=1, dir=dir, weight_prob=[1,1,1],pp=k)

#evaluation
for name in graph_name_list:
    EV.measure(name, dir)
    EV.measure_threshold(name, dir)
    EV.measure_brute(name, dir)


EV.generate_appendix_tables(dir, graph_name_list)
EV.generate_plots_exp1_per(dir, graph_name_list)
EV.generate_table_exp1(dir, graph_name_list)
EV.generate_plots_exp2(dir, graph_name_list)

