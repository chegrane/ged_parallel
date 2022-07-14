"""
TUDatasets :    https://chrsmrrs.github.io/datasets/
github: https://github.com/chrsmrrs/tudataset
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
File Format
The data sets have the following format (replace DS by the name of the data set):

Let

n = total number of nodes
m = total number of edges
N = number of graphs
1- DS_A.txt (m lines): sparse (block diagonal) adjacency matrix for all graphs, each line corresponds to (row, col) resp. (node_id, node_id). All graphs are undirected. Hence, DS_A.txt contains two entries for each edge.
2- DS_graph_indicator.txt (n lines): column vector of graph identifiers for all nodes of all graphs, the value in the i-th line is the graph_id of the node with node_id i
3- DS_graph_labels.txt (N lines): class labels for all graphs in the data set, the value in the i-th line is the class label of the graph with graph_id i
4- DS_node_labels.txt (n lines): column vector of node labels, the value in the i-th line corresponds to the node with node_id i

There are optional files if the respective information is available:

- DS_edge_labels.txt (m lines; same size as DS_A_sparse.txt): labels for the edges in DS_A_sparse.txt
- DS_edge_attributes.txt (m lines; same size as DS_A.txt): attributes for the edges in DS_A.txt
- DS_node_attributes.txt (n lines): matrix of node attributes, the comma seperated values in the i-th line is the attribute vector of the node with node_id i
- DS_graph_attributes.txt (N lines): regression values for all graphs in the data set, the value in the i-th line is the attribute of the graph with graph_id i

The datasets can also we easily accessed from popular graph deep libraries, see here (https://chrsmrrs.github.io/datasets/docs/deep/).
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

GXL (Graph eXchange Language) : https://en.wikipedia.org/wiki/GXL
GXL : https://userpages.uni-koblenz.de/~ist/GXL/index.php


"""
import os.path

"""
DS_A.txt (m lines): sparse (block diagonal) adjacency matrix for all graphs, each line corresponds to (row, col) resp. (node_id, node_id). All graphs are undirected. Hence, DS_A.txt contains two entries for each edge.
Example:
1, 2
2, 1
1, 6
6, 1
2, 3
3, 2
....

For each 2 successive lines, read only the first line.
store in map of id, list of ids. which is node and its list of adjacency. 
"""


def read_adjacency_matrix_for_all_graphs_as_adjacency_list(file_name):
    with open(file_name, "r") as f:
        edges_adjacency_list = {}
        for line in f:
            # A) get first line only
            first_line = line.strip().split(",")
            nd_id_from = int(first_line[0])
            nd_id_to = int(first_line[1])
            if nd_id_from not in edges_adjacency_list:
                edges_adjacency_list[nd_id_from] = []
            edges_adjacency_list[nd_id_from].append(nd_id_to)

            # B) skip the second line
            next(f)

    return edges_adjacency_list


"""
DS_graph_indicator.txt (n lines): column vector of graph identifiers for all nodes of all graphs, 
the value in the i-th line is the graph_id of the node with node_id i
Example:
1  # graph_id 1 for the node with node_id 1
1  # graph_id 1 for the node with node_id 2
1  # graph_id 1 for the node with node_id 3
...# graph_id 1 for the node with node_id i (i-th node)
2  # graph_id 2 for the node with node_id j (line number)
2  # graph_id 2 for the node with node_id j+1
2  # graph_id 2 for the node with node_id j+2
...# graph_id 2 for the node with node_id j+k (k-th node)

Create a map of graph_id, list of node_ids, where:
- key is graph_id (the digit ine the line)
- value is list of node_ids (the node_id is the line number)
"""
def read_graph_indicator(file_DS_graph_indicator):
    with open(file_DS_graph_indicator, "r") as f:
        graph_indicator = {}
        for id_node, line in enumerate(f, start=1):
            graph_id = int(line.strip())
            if graph_id not in graph_indicator:
                graph_indicator[graph_id] = []
            graph_indicator[graph_id].append(id_node)

    return graph_indicator



"""
DS_graph_labels.txt (N lines): class labels for all graphs in the data set, 
the value in the i-th line is the class label of the graph with graph_id i
Example:
0  # class label 0 for the graph with graph_id 1 (line 1)
1  # class label 1 for the graph with graph_id 2 (line 2)
0  # class label 0 for the graph with graph_id 3  (line 3)
1  # class label 1 for the graph with graph_id 4  (line 4)

Create a simple array of class labels, where:
the value at index i is the class label for the graph with graph_id (i+1), because we use 0 based index.
"""

def read_graph_labels(file_DS_graph_labels):
    with open(file_DS_graph_labels, "r") as f:
        graph_labels = []
        for line in f:
            graph_labels.append(line.strip())

    return graph_labels


"""
DS_node_labels.txt (n lines): column vector of node labels, 
the value in the i-th line corresponds to the node with node_id i
Example:
0  # node label 0 for the node with node_id 1
1  # node label 1 for the node with node_id 2
0  # node label 0 for the node with node_id 3
0  # node label 0 for the node with node_id 4

Create a simple array of nodes labels, where:
the value at index i is the node label for the node with node_id (i+1), because we use 0 based index.

"""

def read_node_labels(file_DS_node_labels):
    with open(file_DS_node_labels, "r") as f:
        node_labels = []
        for line in f:
            node_labels.append(line.strip())

    return node_labels


"""
DS_edge_labels.txt (m lines; same size as DS_A_sparse.txt): 
labels for the edges in DS_A_sparse.txt (DS_A_sparse.txt is DS_A.txt)
Example:
DS_A.txt    DS_edge_labels.txt
1, 2		0   # edge label 0 for the edge (1,2)
2, 1		0   # edge label 0 for the edge (2,1)
1, 6		1   # edge label 1 for the edge (1,6)
6, 1		1   # edge label 1 for the edge (6,1)
2, 3		1   # edge label 1 for the edge (2,3)
3, 2		1   # edge label 1 for the edge (3,2)

each line in DS_A.txt corresponds to the line in DS_edge_labels.txt

For each 2 successive lines, read only the first line.
store in map of id, list of ids.
- key : first node id
- value : list of pair of (second node id, edge label)   

"""

def read_edges_adjacency_list_labels(file_DS_A, file_DS_edge_labels):

    with open(file_DS_A, "r") as f_A, open(file_DS_edge_labels, "r") as f_edge_labels:
        edges_adjacency_labels = {}
        for line_A, line_edge_labels in zip(f_A, f_edge_labels):
            # A) get first line only
            first_line_A = line_A.strip().split(",")
            nd_id_from = int(first_line_A[0])
            nd_id_to = int(first_line_A[1])
            edge_label = line_edge_labels.strip()

            if nd_id_from not in edges_adjacency_labels:
                edges_adjacency_labels[nd_id_from] = []
            edges_adjacency_labels[nd_id_from].append((nd_id_to, edge_label))

            # B) skip the second line
            next(f_A)
            next(f_edge_labels)

    return edges_adjacency_labels


"""
DS_node_attributes.txt (n lines): matrix of node attributes, 
the comma seperated values in the i-th line is the attribute vector of the node with node_id i
Example:
1.0, 0.0, 9.776700019836426, -3.5490000247955322 # node attribute vector for the node with node_id 1
1.0, 0.0, 8.910699844360352, -3.0490000247955322 # node attribute vector for the node with node_id 2
.... etc
values are floats.

we can read the file as a matrix of n rows and m columns, where:
- n is the number of nodes
- m is the number of attributes (a vector of 4 attributes in the line)

"""

def read_node_attributes(file_DS_node_attributes):
    with open(file_DS_node_attributes, "r") as f:
        node_attributes = []
        for line in f:
            node_attributes.append(line.strip().split(","))

    return node_attributes


def create_node(nd_id, nd_label, nd_attributes):
    nd = ""
    nd += "<node id=\"{}\">".format(nd_id) + "\n"
    nd += "<attr name=\"label\"><int>{}</int> </attr>".format(nd_label) + "\n"
    for idx, att in enumerate(nd_attributes):
        nd += "<attr name=\"attr_{}\"><float>{}</float> </attr>".format(idx,att) + "\n"
    nd += "</node>" + "\n"

    return nd


def create_edge(nd_id_from, nd_id_to, edge_label, edge_attributes):
    edge = ""
    edge += "<edge from=\"{}\" to=\"{}\">".format(nd_id_from, nd_id_to) + "\n"
    edge += "<attr name=\"label\"><int>{}</int> </attr>".format(edge_label) + "\n"
    for idx, att in enumerate(edge_attributes):
        edge += "<attr name=\"attr_{}\"><float>{}</float> </attr>".format(idx,att) + "\n"
    edge += "</edge>" + "\n"

    return edge


def graph_begin_end(gr_id, gr_label):
    gr_begin = ""
    gr_begin += "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + "\n"
    gr_begin += "<!DOCTYPE gxl SYSTEM \"http://www.gupro.de/GXL/gxl-1.0.dtd\">" + "\n"
    gr_begin += "<gxl>" + "\n"
    gr_begin += "<graph id=\"_{}\" edgeids=\"true\" edgemode=\"undirected\">".format(gr_id) + "\n" # add "_" to id : example (_1) to avoid conflict with id of nodes when loading for gxl
    gr_begin += "<attr name=\"label\"><int>{}</int> </attr>".format(gr_label) + "\n"    # graph label te is int

    gr_end = "</graph>" + "\n"
    gr_end += "</gxl>" + "\n"

    return gr_begin, gr_end


"""
in GXL, we have garph tag that contain id; we can add attribute to it to specify the graph label
<attr name="label"><int>1</int></attr>
but I dont know how to do it in GXL.

we can also, give the graph id for the file name, and the label in the id inside the graph tag.
any way, in our case, we don't need to specify the graph label, because we dn't do machine learning.
"""
def generate_graphs(gr_ids, gr_labels, node_labels, node_attributes, edges_adjacency_labels, data_set_name, dir_output):
    """
    :param gr_ids: map of graph id to list of node ids gr_id: [nd_id_1, nd_id_2, ...]
    :param gr_labels: an array where the value at index i is the class label for the graph with graph_id (i+1)
    :param node_labels:
    :param node_attributes:
    :param edges_adjacency_list:
    :param edge_labels:
    :return:
    """

    for gr_id, list_nodes in gr_ids.items():
        gr_label = gr_labels[gr_id - 1]
        gr_begin, gr_end = graph_begin_end(gr_id, gr_label)

        gr = ""
        gr += gr_begin

        # create nodes
        for nd_id in list_nodes:
            nd_label = node_labels[nd_id - 1]
            nd_attributes = node_attributes[nd_id - 1]
            gr += create_node(nd_id, nd_label, nd_attributes)

        # create edges
        for nd_id_from in list_nodes:
            # check if nd_id_from has any adjacency list
            if nd_id_from in edges_adjacency_labels:
                for nd_id_to, edge_label in edges_adjacency_labels[nd_id_from]:
                    edge_attributes = [] # we don't have any edge attributes
                    gr += create_edge(nd_id_from, nd_id_to, edge_label, edge_attributes)
            else:
                print("nd_id_from: {} has no adjacency list".format(nd_id_from))
                continue

        gr += gr_end

        # write the graph to file
        file_name = "{}_graph_{}.gxl".format(data_set_name, gr_id)
        with open(os.path.join(dir_output,file_name), "w") as f:
            f.write(gr)


"""
we generate x graphs only, and each graph has y nodes only.
this is because we want to generate graphs that can be solved by exact GED is reasonable time.
"""
def generate_x_graphs_y_nodes(gr_ids, gr_labels, node_labels, node_attributes, edges_adjacency_labels, data_set_name, dir_output,
                              nb_graphs,nb_nodes_per_graph):
    """
    :param gr_ids: map of graph id to list of node ids gr_id: [nd_id_1, nd_id_2, ...]
    :param gr_labels: an array where the value at index i is the class label for the graph with graph_id (i+1)
    :param node_labels:
    :param node_attributes:
    :param edges_adjacency_list:
    :param edge_labels:
    :param nb_graphs: number of graphs to generate
    :param nb_nodes_per_graph: number of nodes per graph
    :return:
    """

    nb_graphs_generated = 0

    for gr_id, list_nodes in gr_ids.items():
        #print("we are in the graph {}".format(gr_id))

        if nb_graphs_generated >= nb_graphs:
            break
        if len(list_nodes) > 21 or len(list_nodes) < 13 :
        #if len(list_nodes) != nb_nodes_per_graph:
            continue

        nb_graphs_generated += 1

        print("graph {} accepted for generation, we are in the graph {},  nb nds: {}".format(gr_id,nb_graphs_generated,len(list_nodes)))

        gr_label = gr_labels[gr_id - 1]
        gr_begin, gr_end = graph_begin_end(gr_id, gr_label)

        gr = ""
        gr += gr_begin

        # create nodes
        for nd_id in list_nodes:
            nd_label = node_labels[nd_id - 1]
            nd_attributes = node_attributes[nd_id - 1]
            gr += create_node(nd_id, nd_label, nd_attributes)

        # create edges
        for nd_id_from in list_nodes:
            # check if nd_id_from has any adjacency list
            if nd_id_from in edges_adjacency_labels:
                for nd_id_to, edge_label in edges_adjacency_labels[nd_id_from]:
                    edge_attributes = [] # we don't have any edge attributes
                    gr += create_edge(nd_id_from, nd_id_to, edge_label, edge_attributes)
            else:
                print("nd_id_from: {} has no adjacency list".format(nd_id_from))
                continue

        gr += gr_end

        # write the graph to file
        file_name = "{}_graph_{}.gxl".format(data_set_name, gr_id)
        with open(os.path.join(dir_output,file_name), "w") as f:
            f.write(gr)


"""
we generate x graphs only, and each graph has y nodes only.
no edge labels.
"""
def generate_x_graphs_y_nodes_no_edge_labels(gr_ids, gr_labels, node_labels, node_attributes, edges_adjacency, data_set_name, dir_output,
                              nb_graphs,nb_nodes_per_graph):
    """
    :param gr_ids: map of graph id to list of node ids gr_id: [nd_id_1, nd_id_2, ...]
    :param gr_labels: an array where the value at index i is the class label for the graph with graph_id (i+1)
    :param node_labels:
    :param node_attributes:
    :param edges_adjacency_list:
    :param edge_labels:
    :param nb_graphs: number of graphs to generate
    :param nb_nodes_per_graph: number of nodes per graph
    :return:
    """

    nb_graphs_generated = 0
    unique_edge_label = 0 # a unique edge label for all edges in the graph (like there is no edge)

    for gr_id, list_nodes in gr_ids.items():

        if nb_graphs_generated >= nb_graphs:
            break
        if len(list_nodes) > 77 or len(list_nodes) < 70 :
        #if len(list_nodes) != nb_nodes_per_graph:
            continue

        nb_graphs_generated += 1

        print("graph {} accepted for generation, we are in the graph {},  nb nds: {}".format(gr_id,nb_graphs_generated,len(list_nodes)))

        gr_label = gr_labels[gr_id - 1]
        gr_begin, gr_end = graph_begin_end(gr_id, gr_label)

        gr = ""
        gr += gr_begin

        # create nodes
        for nd_id in list_nodes:
            nd_label = node_labels[nd_id - 1]
            nd_attributes = node_attributes[nd_id - 1]
            gr += create_node(nd_id, nd_label, nd_attributes)

        # create edges
        for nd_id_from in list_nodes:
            # check if nd_id_from has any adjacency list
            if nd_id_from in edges_adjacency:
                for nd_id_to in edges_adjacency[nd_id_from]:
                    edge_attributes = [] # we don't have any edge attributes
                    gr += create_edge(nd_id_from, nd_id_to, unique_edge_label, edge_attributes)
            else:
                print("nd_id_from: {} has no adjacency list".format(nd_id_from))
                continue

        gr += gr_end

        # write the graph to file
        file_name = "{}_graph_{}.gxl".format(data_set_name, gr_id)
        with open(os.path.join(dir_output,file_name), "w") as f:
            f.write(gr)




# test: compar keys from two dicts
def compare_keys(dict1, dict2):
    for key in dict1:
        if key not in dict2:
            print("key {} not in dict2".format(key))
            return False

    print("keys are the same")
    return True


# create dir if not exist
def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def main():

    data_set_name = "MSRC_21"

    data_set_dir = R"C:\Users\ibra\OneDrive - USherbrooke\CERIST\TUDataset\{}".format(data_set_name)
    res_dir_output = R"C:\Users\ibra\OneDrive - USherbrooke\CERIST\TUDataset\{}\gxl".format(data_set_name)

    nb_graphs = 100
    nb_nodes_per_graph = 77
    is_edge_label = False
    is_graph_label = True
    is_node_attributes = False
    is_node_labels = True
    create_dir(res_dir_output)
    file_DS_A = os.path.join(data_set_dir, data_set_name + "_A.txt")
    file_DS_graph_indicator = os.path.join(data_set_dir, data_set_name + "_graph_indicator.txt")
    file_DS_graph_labels = os.path.join(data_set_dir, data_set_name + "_graph_labels.txt")
    file_DS_node_labels =  os.path.join(data_set_dir, data_set_name + "_node_labels.txt")
    file_DS_edge_labels = os.path.join(data_set_dir, data_set_name + "_edge_labels.txt")
    file_DS_node_attributes = os.path.join(data_set_dir, data_set_name + "_node_attributes.txt")


    # read graph indicator
    graph_indicator = read_graph_indicator(file_DS_graph_indicator)
    print("len graph indicator : ", len(graph_indicator))

    # compute the total number of nodes in all graphs
    nb_total_nodes = 0
    for list_nodes in graph_indicator.values():
        nb_total_nodes += len(list_nodes)
    print("nb total nodes: ", nb_total_nodes)

    if is_graph_label:
        # read graph labels
        graph_labels = read_graph_labels(file_DS_graph_labels)
        #print(graph_labels)
    else:
        graph_labels = [0]*len(graph_indicator) # all graphs have the same label

    print("len graph label: ", len(graph_labels))

    if is_node_labels:
        # read node labels
        node_labels = read_node_labels(file_DS_node_labels)
        print("len node labels: ", len(node_labels))
    else:
        node_labels = [0]*nb_total_nodes # all nodes have the same label, this is not good

    if is_node_attributes:
        # read node attributes
        node_attributes = read_node_attributes(file_DS_node_attributes)
    else:
        node_attributes = [[]]*len(node_labels) # empty node attributes

    # generate graphs
    if is_edge_label:
        # read edge labels and adjacency list
        edges_adjacency_labels = read_edges_adjacency_list_labels(file_DS_A, file_DS_edge_labels)
        print(" len(edges_adjacency_labels) : ", len(edges_adjacency_labels))
        # print(edges_adjacency_labels, sep="\n")

        # generate graphs
        generate_x_graphs_y_nodes(graph_indicator,
                        graph_labels,
                        node_labels,
                        node_attributes,
                        edges_adjacency_labels,
                        data_set_name,
                        res_dir_output,
                        nb_graphs,
                        nb_nodes_per_graph)
    else: # no edge labels
        # read adjacency list only
        edges_adjacency_list = read_adjacency_matrix_for_all_graphs_as_adjacency_list(file_DS_A)
        print(" len(edges_adjacency_list) : ", len(edges_adjacency_list))
        # print(edges_adjacency_list)

        # generate graphs
        generate_x_graphs_y_nodes_no_edge_labels(graph_indicator,
                                  graph_labels,
                                  node_labels,
                                  node_attributes,
                                  edges_adjacency_list,
                                  data_set_name,
                                  res_dir_output,
                                  nb_graphs,
                                  nb_nodes_per_graph)


if __name__ == '__main__':
    main()