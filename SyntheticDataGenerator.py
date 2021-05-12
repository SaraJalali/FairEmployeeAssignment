import math
import networkx as nx
import glob
import Setup as Setup
import random





def generate_functional(n, version):
    edges=[(1,2), (1,3), (1,4), (1,5), (1,6), (1,7),
           (2,8), (6,10), (6,11), (7,12),
           (8, 13), (4,14), (5,15), (10,16), (11, 17), (12, 18)]

    s= math.ceil(n/6)

    m= math.ceil(s/10)
    groups= []
    subgroups=[]
    headss=[]


    c=18
    for i in range(6):
        heads = list(range(c+1, c+m+1))
        headss.append(heads)
        group=[]
        subgroup=[]

        for j in range(len(heads)):
            u = heads[j]
            group.append(u)
            for k in range(j+1, len(heads)):
                v= heads[k]
                edges.append((u,v))

        c= heads[-1]
        teams = list(range(c+1, c+s+1))

        c= teams[0]
        for u in heads:
            a=[]
            for j in range(20):
                c+=1
                group.append(c)
                if c<=teams[-1]:
                    edges.append((u, c))
                    a.append(c)
                else:
                    break
            subgroup.append(u)
            for j in range(len(a)):
                u = a[j]
                for k in range(j + 1, len(a)):
                    v = a[k]
                    edges.append((u, v))
        subgroups.append(subgroup)

        c=v

        groups.append(group)

    G = nx.Graph()
    G.add_edges_from(edges)
    nodes = list(G.nodes())

    n = len(G.nodes())
    p = math.ceil(0.3 * n)
    q = n-p
    gender = {}
    if version == 1:
        nodes1 = set(random.sample(nodes, p))
        for u in nodes:
            if u in nodes1:
                gender[u] = 'female'
            else:
                gender[u] = 'male'
    elif version == 2:
        nodes1 = list(range(1,25))
        p1 = math.ceil(0.3 * len(nodes1))
        nodes2 = set(random.sample(nodes1, p1))
        male=0
        female=0
        for u in nodes1:
            if u in nodes2:
                gender[u] = 'female'
                female+=1
            else:
                gender[u] = 'male'
                male+=1
        for u in range(25, nodes[-1]+1):
            if female<p:
                gender[u] = 'female'
                female +=1
            else:
                gender[u] = 'male'

    #all heads are male
    elif version ==3:
        nodes1 = list(range(1, 25))
        for item in headss:
            nodes1.extend(item)
        gender = dict(zip(nodes1,['male']* len(nodes1)))
        male = len(gender)
        nodes2 = set(nodes) - set(nodes1)
        #p1 = math.ceil(len(nodes2)*0.3)
        nodes3 = set(random.sample(nodes2, p))
        female = 0
        for u in nodes:
            if u in nodes3:
                gender[u] = 'female'
                female += 1
            else:
                gender[u] = 'male'
                male += 1

    #two majority groups, 1 minority
    elif version == 4:
        male =0
        female = 0
        head = headss[0]
        group = groups[0]
        nodes1 = head.copy()
        nodes1.extend(group)
        gender = dict(zip(nodes1, ['female']* len(nodes1)))
        female+= len(gender)

        head = headss[1]
        group = groups[1]
        nodes2 = head.copy()
        nodes2.extend(group.copy())
        head = headss[2]
        group = groups[2]
        nodes3 = head.copy()
        nodes3.extend(group.copy())
        nodes2.extend(nodes3)
        gender1 = dict(zip(nodes2, ['male'] * len(nodes2)))
        male += len(gender1)

        gender.update(gender1)

        nodes1.extend(nodes2)

        nodes2 = list(set(nodes) - set(nodes1))
        p = p - female

        gender2 = random.sample(nodes2, p)
        gender3 = list(set(nodes2) - set(gender2))
        gender2 = dict(zip(gender2, ['female']*len(gender2)))
        gender3 = dict(zip(gender3, ['male']*len(gender3)))

        gender.update(gender2)
        gender.update(gender3)


    nx.set_node_attributes(G, gender, 'att')

    nx.set_node_attributes(G, gender, 'gender')
    print('######')
    print(len(gender))
    print(len(G.nodes()))


    return G


def generate_subgroup(leader, n, k):
    edges=[]
    group = list(range(k, k+n))
    for i in group:
        edges.append((leader, i))

    for i in range(len(group)):
        for j in range(i+1, len(group)):
            edges.append((group[i], group[j]))
    return edges, group


def generate_divisional(n, version):
    s = math.ceil(n/50)
    edges=[(1,2), (1,3),(1,4), (1,5),
           (1,6), (1,7)]
    heads=[1,2,3,4,5,6,7]
    k=8

    groups=[]

    group_heads=[]

    new_edges, group = generate_subgroup(1, 15, k)
    heads.extend(group)
    k = group[-1]+1
    edges.extend(new_edges)
    for l in group:
        new_edges, group = generate_subgroup(l, s, k)
        k = group[-1] + 1
        edges.extend(new_edges)
        groups.append(group)
        group_heads.append((l,group))

    new_edges, group = generate_subgroup(5, 12, k)
    heads.extend(group)
    k = group[-1] + 1
    edges.extend(new_edges)
    for l in group:
        new_edges, group = generate_subgroup(l, s, k)
        k = group[-1] + 1
        edges.extend(new_edges)
        groups.append(group)
        group_heads.append((l,group))

    new_edges, group = generate_subgroup(4, 6, k)
    heads.extend(group)
    k = group[-1] + 1
    edges.extend(new_edges)
    for l in group:
        new_edges, group = generate_subgroup(l, s, k)
        k = group[-1] + 1
        edges.extend(new_edges)
        groups.append(group)
        group_heads.append((l,group))


    new_edges, group = generate_subgroup(3, 9, k)
    heads.extend(group)
    k = group[-1] + 1
    edges.extend(new_edges)
    for l in group:
        new_edges, group = generate_subgroup(l, s, k)
        k = group[-1] + 1
        edges.extend(new_edges)

    edges.append((k, 3))
    for i in group:
        edges.append((k, i))
    heads.append(k)

    new_edges, group = generate_subgroup(k, s, k+1)
    edges.extend(new_edges)

    G = nx.Graph()
    G.add_edges_from(edges)
    nodes = list(G.nodes())

    n = len(G.nodes())
    p = math.ceil(0.3 * n)
    q = n-p
    gender = {}
    if version == 1:
        nodes1 = set(random.sample(nodes, p))
        for u in nodes:
            if u in nodes1:
                gender[u] = 'female'
            else:
                gender[u] = 'male'
    elif version == 2:
        female, male = 0,0
        for u in nodes:
            if male<q:
                gender[u] = 'male'
                male +=1
            else:
                gender[u] = 'female'
    #all heads are male
    elif version ==3:

        gender = dict(zip(heads,['male']* len(heads)))
        male = len(gender)
        nodes2 = set(nodes) - set(heads)
        #p1 = math.ceil(len(nodes2)*0.3)
        nodes3 = set(random.sample(nodes2, p))
        female = 0
        for u in nodes:
            if u in nodes3:
                gender[u] = 'female'
                female += 1
            else:
                gender[u] = 'male'
                male += 1
    #two majority groups, 1 minority
    elif version == 4:

        male =0
        female = 0
        rand= list(range(len(group_heads)))
        random.shuffle(rand)
        i=0
        gender={}
        ll=[]
        while male<q/2:
            l, group = group_heads[rand[i]]
            gen = dict(zip(group, ['male']*len(group)))
            gender[l] = 'male'
            gender.update(gen)
            male+= len(group)+1
            ll.append(l)
            i+=1

        while female<p/2:
            l, group = group_heads[rand[i]]
            if l not in ll:
                gen = dict(zip(group, ['female'] * len(group)))
                gender[l] = 'female'
                gender.update(gen)
                female += len(group)
                i += 1


        nodes2 = set(nodes) - set(list(gender.keys()))
        nodes3 = list(random.sample(nodes2, int(p - female)))
        gen = dict(zip(nodes3, ['female']*len(nodes3)))
        gender.update(gen)

        nodes2 = list(set(nodes) - set(list(gender.keys())))
        gen = dict(zip(nodes2, ['male'] * len(nodes2)))
        gender.update(gen)


        '''
        nodes3 = set(random.sample(nodes2, int(p/2)))
        for u in nodes:
            if u in nodes3:
                gender[u] = 'female'
            else:
                gender[u] = 'male'
        '''
    nx.set_node_attributes(G, gender, 'att')
    nx.set_node_attributes(G, gender, 'gender')
  #  print('######')
  #  print(len(gender))
  #  print(len(G))
    return G



def intra_organizational():
    edges = []
    with open('1_3.txt') as f:
        for line in f:
            a = line.split()
            edges.append((int(a[0]), int(a[1])))
    G1 = nx.Graph()
    G1.add_edges_from(edges)
    with open('gender.txt') as f:
        for line in f:
            a = line.split()
            b = []
            for item in a:
                b.append('male' if item == '1' else 'female')
            gender = dict(zip(range(1, len(G1) + 1), b))
            nx.set_node_attributes(G1, gender, 'att1')

    with open('gender.txt') as f:
        for line in f:
            a = line.split()
            b = []
            for item in a:
                b.append('male' if item == '2' else 'female')
            gender = dict(zip(range(1, len(G1) + 1), b))
            nx.set_node_attributes(G1, gender, 'att2')

    with open('gender.txt') as f:
        for line in f:
            a = line.split()
            b = []
            for item in a:
                b.append('male' if item == '3' else 'female')
            gender = dict(zip(range(1, len(G1) + 1), b))
            nx.set_node_attributes(G1, gender, 'att3')
    with open('gender.txt') as f:
        for line in f:
            a = line.split()
            b = []
            for item in a:
                b.append('male' if item == '4' else 'female')
            gender = dict(zip(range(1, len(G1) + 1), b))
            nx.set_node_attributes(G1, gender, 'att4')

    nx.write_gpickle(G1, '2.gpickle')

    print(nx.attribute_assortativity_coefficient(G1, 'att1'))
    print(nx.attribute_assortativity_coefficient(G1, 'att2'))
    print(nx.attribute_assortativity_coefficient(G1, 'att3'))
    print(nx.attribute_assortativity_coefficient(G1, 'att4'))


def generate_samples():
    dir = '/Users/sara/OneDrive - Syracuse University/Results/FairEmployeeAssignment/'

    graph_dir = dir + 'Small/'
    sample_files = [f for f in glob.glob(graph_dir + "**/*.gpickle", recursive=True)]
    sample_files.sort()
    for f in sample_files:
        if True:
            print('########')
            G = nx.read_gpickle(f)
            name = (f.split('/')[-1]).replace('.gpickle', '')
            print(name)
            nx.set_node_attributes(G, nx.get_node_attributes(G, 'gender'), 'att')
            att = nx.get_node_attributes(G, 'gender')
            nx.set_node_attributes(G, att, 'att')
            Setup.save_sampled_graphs(G, name)

def convert():
    G = nx.read_gpickle('2.gpickle')
    print(nx.attribute_assortativity_coefficient(G, 'att1'))
    print(nx.attribute_assortativity_coefficient(G, 'att2'))
    print(nx.attribute_assortativity_coefficient(G, 'att3'))

    edges = G.edges()

    G1 = nx.Graph()
    G1.add_edges_from(edges)
    att = nx.get_node_attributes(G, 'att1')
    nx.set_node_attributes(G1, att, 'att')
    print(nx.attribute_assortativity_coefficient(G1, 'att'))

    G2 = nx.Graph()
    G2.add_edges_from(edges)
    att = nx.get_node_attributes(G, 'att2')
    nx.set_node_attributes(G2, att, 'att')
    print(nx.attribute_assortativity_coefficient(G2, 'att'))

    G3 = nx.Graph()
    G3.add_edges_from(edges)
    att = nx.get_node_attributes(G, 'att3')
    nx.set_node_attributes(G3, att, 'att')
    print(nx.attribute_assortativity_coefficient(G3, 'att'))

    G4 = nx.Graph()
    G4.add_edges_from(edges)
    att = nx.get_node_attributes(G, 'att4')
    nx.set_node_attributes(G4, att, 'att')
    print(nx.attribute_assortativity_coefficient(G4, 'att'))

    nx.write_gpickle(G1, 'intra2_1.gpickle')
    nx.write_gpickle(G2, 'intra2_2.gpickle')
    nx.write_gpickle(G3, 'intra2_3.gpickle')
    nx.write_gpickle(G4, 'intra2_4.gpickle')


ns = [250, 500, 1000]
for n in ns:

    print('##############')
    G = generate_functional(n, 2)
    print(nx.attribute_assortativity_coefficient(G, 'att'))
    print(nx.attribute_assortativity_coefficient(G, 'gender'))
    nx.write_gpickle(G, 'f1(' + str(n) + ').gpickle')
    G = generate_functional(n, 4)
    print(nx.attribute_assortativity_coefficient(G, 'att'))
    print(nx.attribute_assortativity_coefficient(G, 'gender'))
    nx.write_gpickle(G, 'f2(' + str(n) + ').gpickle')
    G = generate_functional(n, 3)
    print(nx.attribute_assortativity_coefficient(G, 'att'))
    print(nx.attribute_assortativity_coefficient(G, 'gender'))
    nx.write_gpickle(G, 'f3(' + str(n) + ').gpickle')

    G = generate_divisional(n, 2)
    print(nx.attribute_assortativity_coefficient(G, 'att'))
    print(nx.attribute_assortativity_coefficient(G, 'gender'))
    nx.write_gpickle(G, 'd1(' + str(n) + ').gpickle')
    G = generate_divisional(n, 4)
    print(nx.attribute_assortativity_coefficient(G, 'att'))
    print(nx.attribute_assortativity_coefficient(G, 'gender'))
    nx.write_gpickle(G, 'd2(' + str(n) + ').gpickle')
    G = generate_divisional(n, 3)
    print(nx.attribute_assortativity_coefficient(G, 'att'))
    print(nx.attribute_assortativity_coefficient(G, 'gender'))
    nx.write_gpickle(G, 'd3(' + str(n) + ').gpickle')


#generate_samples()