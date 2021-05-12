import networkx as nx
import SupportGroup as SG
import PreProcess as PP
import FairEA as FA


import IPOPT as OP
import BruteForth as BF
import MaxFitness as MF
import Random as RM
import MaxWeightMatching as WM






def assignment(candidate_dic, position_list, fitness_dic, G, method, weight_probability=[1, 1, 1], kk=0):
    matched_1=[]
    #step 1: support group
    if weight_probability[2]==1:
        matched_1 = PP.pre_assignment(candidate_dic, position_list, fitness_dic, G)
        if weight_probability[2] == 1:
            if kk != 0:
                matched_1.extend(SG.support_group_assignment(candidate_dic, position_list, fitness_dic, G, p=kk))
            else:
                matched_1.extend(SG.support_group_assignment(candidate_dic, position_list, fitness_dic, G))
        weight_probability[2] =0

    #step 2: assigning remaining candidates to remaining positions
    if len(position_list)>0:
        #FairEmployeeAssignment
        if method == 1:
            G_out, M = FA.assignment_fairea(candidate_dic.copy(), position_list.copy(), fitness_dic.copy(), G.copy(),
                                 weight_probability=weight_probability, version=4, kk=kk, local=True)
        # random
        elif method == 2:
            G_out, M = RM.assignment_random(candidate_dic.copy(), position_list.copy(), fitness_dic.copy(), G.copy())
        # bruth_forth with two objectives
        elif method == 3:
            return BF.assignmentBruthForth1(candidate_dic.copy(), position_list.copy(), fitness_dic.copy(), G.copy())
        # bruth_forth with three objectives
        elif method == 4:
            return BF.assignmentBruthForth2(candidate_dic.copy(), position_list.copy(), fitness_dic.copy(), G.copy())
        #IPOPT
        elif method == 5:
            G_out, M = OP.assignment_simple_gekko(candidate_dic.copy(), position_list.copy(), fitness_dic.copy(),
                                                  G.copy())
        # hungrian
        elif method == 6:
            G_out, M = WM.assignment_max_weight(candidate_dic.copy(), position_list.copy(), fitness_dic.copy(), G.copy(),
                                             weight_probability=weight_probability, version=3)
        # max fitness
        elif method == 7:
            G_out, M = MF.assignment_simple(candidate_dic.copy(), fitness_dic.copy(), G.copy())

        # min fitness
        elif method == 8:
            G_out, M = MF.assignment_simple(candidate_dic.copy(), fitness_dic.copy(), G.copy(), reverse=True)
        if M == []:
            return nx.Graph(), []

        else:
            M = list(M)
            M.extend(matched_1)
            return G_out, set(M)
    else:
        return G, matched_1




    return stats


