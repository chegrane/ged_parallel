# Created by ibra on 4/4/2021
import csv
import os
import subprocess
import sys
from xml.etree import ElementTree

from subprocess import Popen, PIPE

nb_iteration = 1
is_dynamic = 0
k_best = 10

amount_RunTime_Seconds = 100
NB_threads = 20

exe_jar_file = "ged.jar" # to be changed to the method entred by the user as a parameter argument

nb_graphs_test = 20 # number of graphs to be tested in the dataset

setting = "s1"  # can be: s1, s2, s3, sall (all settings)


def get_number_lines_file(file_path):
    # first, check if the file exist
    if not os.path.isfile(file_path):
        print("file " + file_path + " does not exist")
        return 0
    # then, check if the file is empty
    if os.stat(file_path).st_size == 0:
        print("file " + file_path + " is empty")
        return 0
    # compute the number of lines in the file
    with open(file_path, 'r') as f:
        for i, l in enumerate(f):
            pass
    return i + 1


# we have GED file separated by ";" that contain 8 columns
# we are intrested only in the first 3 columns: g1_file_path, g2_file_path, ged
# we need to all g1_file_path, g2_file_path, ged
def get_g1_g2_ged_from_csv(file_path):
    list_g1_g2_ged = []
    with open(file_path, 'r', newline='', encoding='utf-8') as input:
        csv_input = csv.reader(input, delimiter=';')  # g1, g2
        for line in csv_input:
            g1, g2, ged = list(line)[0:3]
            list_g1_g2_ged.append((g1,g2,ged))

    return list_g1_g2_ged



def get_file_name_XMLfile(file_path: str) -> list:
    from xml.dom.minidom import parse
    import xml.dom.minidom

    dom = xml.dom.minidom.parse(file_path)
    collection = dom.documentElement
    files = collection.getElementsByTagName("print")

    list_files = [f.getAttribute("file") for f in files]

    return list_files


def get_file_name_csv(file_path):
    list_files = []

    with open(file_path, 'r', newline='', encoding='utf-8') as input:
        csv_input = csv.reader(input, delimiter=';')  # g1, g2
        next(csv_input)  # skip the first line, because it contain only title
        for line in csv_input:
            g1, g2 = list(line)  # each line contains tow graph file name
            list_files.append(g1)
            list_files.append(g2)

    return list_files


def get_file_name_simple(file_path):
    list_files = []

    with open(file_path) as f:
        next(f)  # remove the first line , because it contain only title
        for line in f:
            list_files.append(line)

    return list_files


# get all files in the directory that end with .gxl
def get_all_files_in_directory(directory_path: str, ext=".gxl") -> list:
    list_files = []
    for file in os.listdir(directory_path):
        if file.endswith(ext):
            list_files.append(file)

    return list_files

# get all files complete path in the directory that end with .gxl
def get_all_files_in_directory_complete_path(directory_path: str, ext=".gxl") -> list:
    list_files = []
    for file in os.listdir(directory_path):
        if file.endswith(ext):
            list_files.append( os.path.join(directory_path, file))

    return list_files


# subprocess call and wait for the process to finish
def subprocess_call_wait(my_command_args):
    if sys.platform == "linux" or sys.platform == "linux2":
        my_command_args = ["/bin/sh", "-c"] + my_command_args
        my_command_args = ["/bin/sh", "-c"] + [" ".join(my_command_args)] + my_command_args
    subprocess.call(my_command_args)


# test subprocess_call_wait with sleep command in windows
def test_subprocess_call_wait():
    for i in range(0, 5):
        print("test_subprocess_call_wait : " + str(i))
        my_command_args = ["timeout", "5"]
        #subprocess_call_wait(my_command_args)
        run(my_command_args, shell=True)


# for version before python 3.5
def run(*popenargs, **kwargs):
    input = kwargs.pop("input", None)
    check = kwargs.pop("handle", False)

    if input is not None:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = subprocess.PIPE

    process = subprocess.Popen(*popenargs, **kwargs)
    try:
        stdout, stderr = process.communicate(input)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise subprocess.CalledProcessError(
            retcode, process.args, output=stdout, stderr=stderr)
    return retcode, stdout, stderr


##def launch_test(my_Command_args, file_path_g1, file_path_g2, path_output):
def launch_test(cmd_args):
    # print(cmd_args)
    if sys.platform == "linux" or sys.platform == "linux2":
        # cmd_args = ["/bin/sh", "-c"] + cmd_args
        # cmd_args = ["/bin/sh", "-c"] + [" ".join(cmd_args)] + cmd_args
        cmd_args = " ".join(cmd_args)
    #subprocess.run(cmd_args, shell=True)
    run(cmd_args, shell=True)
    # check if python version is lower than 3.5 (for subprocess.run) then use subprocess.call



# test all combinations
def test_all_combinations_k_best(c_node_sub: int, c_node_del_ins: int, c_edge_sub: int, c_edge_del_ins: int,
                                 directory_path_input: str, directory_path_output: str, list_files: list,
                                 test_name: str,
                                 setting: str):
    #nb_combination = 200
    nb_combination = 210 # this for mao, we take 210 (maybe we can take less, maybe 204), that we can delet the same graph with itself, and we get at the end 200 diffirents graph combination.
    idx_nb_combination = 0

    file_separator = os.path.sep

    path_output = directory_path_output + file_separator + "test__{}_{}.csv".format(test_name, setting)

    for i in range(len(list_files) - 1):
        # for j in range(i + 1, len(list_files)):
        for j in range(i, len(list_files)):  # test the file with itself
            file_path_g1 = directory_path_input + file_separator + list_files[i]
            file_path_g2 = directory_path_input + file_separator + list_files[j]

            exe_jar_file = R"C:\Users\ibra\IdeaProjects\dynamic_kbest_GED\out\artifacts\dynamic_kbest_GED_jar\dynamic_kbest_GED.jar"
            if sys.platform == "linux" or sys.platform == "linux2":
                exe_jar_file = "dynamic_kbest_GED.jar"

            my_command_args = ["java", "-jar",
                               exe_jar_file,
                               str(c_node_sub), str(c_node_del_ins), str(c_edge_sub), str(c_edge_del_ins),
                               file_path_g1, file_path_g2, path_output, test_name]

            launch_test(my_command_args)

            # ony for mao dataset, we limit to nb_combination
            if (test_name == "mao"):
                idx_nb_combination += 1
                if (idx_nb_combination >= nb_combination):
                    break
        if test_name == "mao" and idx_nb_combination >= nb_combination:
            break


def get_graph_name_from_path(graph_path:str):
    # graph path is like:
    # Final_results:thread-3:/home/daba/GED_datasets/TUDataset/benzene/gxl/benzene_graph_1.gxl
    # or : /home/daba/GED_datasets/TUDataset/benzene/gxl/benzene_graph_1.gxl
    # return benzene_graph_1.gxl"
    return graph_path.split(os.path.sep)[-1]


def get_combination_not_treated_yet(file_path_treated, list_general_combination):
    # first, check if the file exist
    if not os.path.isfile(file_path_treated):
        print("file " + file_path_treated + " does not exist")
        return list_general_combination
    # then, check if the file is empty
    if os.stat(file_path_treated).st_size == 0:
        print("file " + file_path_treated + " is empty")
        return list_general_combination

    set_combination_treated = set()
    list_combination_not_treated_yet = []

    # Read the file as csv file with ";" as separator
    with open(file_path_treated, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        # for each line, we get the combination already treated
        for row in reader:
            # we get the combination not treated yet, and add it to a set
            g1 = get_graph_name_from_path(row[0])
            g2 = get_graph_name_from_path(row[1])
            set_combination_treated.add((g1, g2))

    # for each combination in list_general_combination, we check if it is not in the set_combination_treated
    for combination_path in list_general_combination:
        g1 = get_graph_name_from_path(combination_path[0])
        g2 = get_graph_name_from_path(combination_path[1])
        if (g1, g2) not in set_combination_treated:
            list_combination_not_treated_yet.append(combination_path)

    return list_combination_not_treated_yet


# test given list of given combination as pair (file1, file2)
def test_given_combinations_list_k_best(c_node_sub: int, c_node_del_ins: int, c_edge_sub: int, c_edge_del_ins: int,
                                 list_combinations_files: list, directory_path_output: str,
                                 test_name: str,
                                 setting: str):

    path_output = directory_path_output + os.path.sep + "test__{}_{}.csv".format(test_name, setting)

    #exe_jar_file = R"C:\Users\ibra\OneDrive - USherbrooke\CERIST\GED-code\GED-code\Exact_GED_BB_DF_v2_parallel (high_level) - with-load balancing\out\artifacts\Exact_GED_BB_parallel_HL_LB_jar\Exact_GED_BB_DF_high_level_with_load_balancing.jar"
    #if sys.platform == "linux" or sys.platform == "linux2":
    #    exe_jar_file = "Exact_GED_BB_DF_parallel_high_level.jar"

    nb_combination_already_treated = get_number_lines_file(path_output) # in case we already have some result in the file
    list_combinations_files = get_combination_not_treated_yet(path_output, list_combinations_files)
    print("len list_combinations_files: " + str(len(list_combinations_files)))
    print(list_combinations_files)

    #for file_path_g1, file_path_g2 in list_combinations_files[nb_combination_already_treated:]:
    for file_path_g1, file_path_g2 in list_combinations_files:
        my_command_args = ["java", "-jar",
                           exe_jar_file,
                           str(c_node_sub), str(c_node_del_ins), str(c_edge_sub), str(c_edge_del_ins),
                           file_path_g1, file_path_g2, path_output, test_name,
                           str(amount_RunTime_Seconds), str(NB_threads)]

        print(" launch : ", my_command_args, "\n")
        launch_test(my_command_args)


# test given list of given combination as tuple (file1, file2, ub_ged(file1, file2))
def test_given_combinations_with_UB_k_best(c_node_sub: int, c_node_del_ins: int, c_edge_sub: int, c_edge_del_ins: int,
                                 list_combinations_files_UB: list, directory_path_output: str,
                                 test_name: str,
                                 setting: str):

    path_output = directory_path_output + os.path.sep + "test__{}_{}.csv".format(test_name, setting)

    exe_jar_file = "Exact_GED_BB_DF_high_level_with_load_balancing_UB_kbest.jar"

    for file_path_g1, file_path_g2, UB_ged in list_combinations_files_UB:
        my_command_args = ["java", "-jar",
                           exe_jar_file,
                           str(c_node_sub), str(c_node_del_ins), str(c_edge_sub), str(c_edge_del_ins),
                           file_path_g1, file_path_g2, path_output, test_name,
                           str(amount_RunTime_Seconds), str(NB_threads), str(UB_ged)]

        print(" launch : ", my_command_args, "\n")
        launch_test(my_command_args)



def test_given_combinations_list(c_node_sub: int, c_node_del_ins: int, c_edge_sub: int, c_edge_del_ins: int,
                                        list_combinations_files: list, directory_path_output: str,
                                        test_name: str,
                                        setting: str,
                                        amount_RunTime_Seconds: int,
                                        NB_threads: int,
                                        exe_jar_file: str):

    path_output = directory_path_output + os.path.sep + "test__{}_{}.csv".format(test_name, setting)

    for file_path_g1, file_path_g2 in list_combinations_files:
        my_command_args = ["java", "-jar",
                           exe_jar_file,
                           str(c_node_sub), str(c_node_del_ins), str(c_edge_sub), str(c_edge_del_ins),
                           file_path_g1, file_path_g2, path_output, test_name,
                           str(amount_RunTime_Seconds), str(NB_threads)]

        #print(my_command_args, "\n")
        launch_test(my_command_args)


def read_args():
    test_benchmark = "MUTA"
    nb_thread = 1

    list_dataste_name = ["ALL", "CMU", "MUTA", "GREC", "acyclic", "alkane", "mao", "PATH"]

    if len(sys.argv) >= 2:
        test_benchmark = sys.argv[1]
        nb_thread = int(sys.argv[2])

    if (test_benchmark not in list_dataste_name):
        print(" bad arguments ... write as input :")
        print("  ALL : to test all benchmarks")
        print("  CMU : to test CMU benchmarks")
        print("  GREC : to test GREC benchmarks")
        print("  MUTA : to test MUTA benchmarks")
        print("  acyclic : to test the for benchmarks : acyclic")
        print("  alkane : to test the for benchmarks : alkane")
        print("  mao : to test the for benchmarks : mao")
        print("  PATH : to test the for benchmarks : pah")

        sys.exit(-1)

    return test_benchmark, nb_thread


def read_benchmark_name_args():
    test_benchmark = "ALL"

    list_dataste_name = ["ALL", "CMU", "MUTA", "GREC", "acyclic", "alkane", "mao", "PATH"]

    if len(sys.argv) >= 1:
        test_benchmark = sys.argv[1]

    if (test_benchmark not in list_dataste_name):
        print(" bad arguments ... write as input :")
        print("  ALL : to test all benchmarks")
        print("  CMU : to test CMU benchmarks")
        print("  GREC : to test GREC benchmarks")
        print("  MUTA : to test MUTA benchmarks")
        print("  acyclic : to test the for benchmarks : acyclic")
        print("  alkane : to test the for benchmarks : alkane")
        print("  mao : to test the for benchmarks : mao")
        print("  PATH : to test the for benchmarks : pah")

        sys.exit(-1)

    return test_benchmark


def grec(root_directory_input, root_directory_output, nb_thread_=1):
    subdirectory = os.path.join("GREC-GED", "GREC")
    directory_file_input = os.path.join(root_directory_input, subdirectory)
    directory_file_path = os.path.join(root_directory_input, "GREC-GED", "GREC-subsets")

    for i in [5, 10, 15, 20]:
    #for i in [20]:
        file_path = directory_file_path + os.path.sep + "train" + str(i) + ".cxl"
        list_files = get_file_name_XMLfile(file_path)
        test_size = "train_"+str(i)

        directory_path_output = root_directory_output + os.path.sep + subdirectory + os.path.sep + (
                "train" + str(i))

        test_all_combinations_k_best(2, 4, 1, 1, directory_file_input, directory_path_output, list_files, "GREC",
                                     test_size+"_setting_1")

        print(" test_GREC --train" + str(i) + ".cxl setting_1-- finished")

        directory_path_output = root_directory_output + os.path.sep + subdirectory + os.path.sep + (
                "train" + str(i))
        test_all_combinations_k_best(2, 4, 1, 2, directory_file_input, directory_path_output, list_files, "GREC",
                                     test_size+"_setting_2")
        print(" test_GREC --train" + str(i) + ".cxl setting_2-- finished")

        directory_path_output = root_directory_output + os.path.sep + subdirectory + os.path.sep + (
                "train" + str(i))
        test_all_combinations_k_best(6, 2, 3, 1, directory_file_input, directory_path_output, list_files, "GREC",
                                     test_size+"_setting_3")
        print(" test_GREC --train" + str(i) + ".cxl setting_3-- finished")


def path_acyclic_alkane_mao(root_directory_input, root_directory_output,
                            data_set_name="acyclic"):
    subdirectory = data_set_name
    directory_file_input = os.path.join(root_directory_input, subdirectory)
    file_name_contain_graph_file = "dataset.cxl"
    file_path = directory_file_input + os.path.sep + file_name_contain_graph_file

    list_files = get_file_name_XMLfile(file_path)

    directory_path_output = root_directory_output + os.path.sep + subdirectory

    test_all_combinations_k_best(2, 4, 1, 1, directory_file_input, directory_path_output, list_files, "PATH",
                                 "setting_1")

    print(" test_ {} setting_1-- finished".format(data_set_name))

    directory_path_output = root_directory_output + os.path.sep + subdirectory
    test_all_combinations_k_best(2, 4, 1, 2, directory_file_input, directory_path_output, list_files, "PATH",
                                 "setting_2")
    print(" test_ {} setting_2-- finished".format(data_set_name))

    directory_path_output = root_directory_output + os.path.sep + subdirectory
    test_all_combinations_k_best(6, 2, 3, 1, directory_file_input, directory_path_output, list_files, "PATH",
                                 "setting_3")
    print(" test_ {} setting_3-- finished".format(data_set_name))


def muta(root_directory_input, root_directory_output):
    subdirectory = "MUTA-GED" + os.path.sep + "Mutagenicity"
    directory_file_input = os.path.join(root_directory_input, subdirectory)
    file_name_contain_graph_file = "mixed-graphs.cxl"
    test_size = "mixed-graphs"

    list_test_name = ["train10",
                      "train20",
                      "train30",
                      "train40",
                      "train50",
                      "train60",
                      "train70"#,
                      #"mixed-graphs"
                      ]

    #for test_size in list_test_name:
    for test_size in ["mixed-graphs"]:
        file_name_contain_graph_file = test_size + ".cxl"
        directory_file_path = root_directory_input + os.path.sep + "MUTA-GED" + os.path.sep + "Mutagenicity-subsets"
        file_path = directory_file_path + os.path.sep + file_name_contain_graph_file

        list_files = get_file_name_XMLfile(file_path)

        directory_path_output = root_directory_output + os.path.sep + subdirectory

        test_all_combinations_k_best(2, 4, 1, 1, directory_file_input, directory_path_output, list_files, "MUTA",
                                     test_size+"_setting_1")

        print(" test_ MUTA", test_size, " setting_1-- finished")

        directory_path_output = root_directory_output + os.path.sep + subdirectory
        test_all_combinations_k_best(2, 4, 1, 2, directory_file_input, directory_path_output, list_files, "MUTA",
                                     test_size+"_setting_2")
        print(" test_ MUTA", test_size, " setting_2-- finished")

        directory_path_output = root_directory_output + os.path.sep + subdirectory
        test_all_combinations_k_best(6, 2, 3, 1, directory_file_input, directory_path_output, list_files, "MUTA",
                                     test_size+"_setting_3")
        print(" test_ MUTA", test_size, " setting_3-- finished")


# sort the list of files lexicographically (by the file name)
def sort_list_files(list_files):
    list_files.sort()
    return list_files

# sort the list of files by the id of the file in the file name
# the id is the number after the last "_" (before the extension)
def sort_list_files_by_id(list_files):
    list_files.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
    return list_files


# TUDataset:
# test each file with itself, and with file after it only.
def tudataset(root_directory_input, root_directory_output):

    # get all files in the directory
    list_files = get_all_files_in_directory_complete_path(root_directory_input)
    #list_files = sort_list_files(list_files)  # in windows, the file name are sorted, in linux not.
    # sort the list of files by the id of the file in the file name
    list_files = sort_list_files_by_id(list_files)

    # choose the first 20 files
    list_files = list_files[0:nb_graphs_test]

    # construct the combination of test files
    pair_test_files = []
    for idx, file_name in enumerate(list_files):
        # file with itself
        ## pair_test_files.append((file_name, file_name))
        # file with next file
        if idx < len(list_files) - 1:
            pair_test_files.append((file_name, list_files[idx + 1]))

    # print("len pair_test_files: ", len(pair_test_files))

    # test setting 1
    if setting == "s1" or setting == "sall":
        test_given_combinations_list_k_best(2, 4, 1, 1, pair_test_files, root_directory_output, "TUDataset","_setting_1")
        print(" test_ setting_1-- finished")

    # test setting 2
    if setting == "s2" or setting == "sall":
        test_given_combinations_list_k_best(2, 4, 1, 2, pair_test_files, root_directory_output, "TUDataset","_setting_2")
        print(" test_ setting_2-- finished")

    # test setting 3
    if setting == "s3" or setting == "sall":
        test_given_combinations_list_k_best(6, 2, 3, 1, pair_test_files, root_directory_output, "TUDataset","_setting_3")
        print(" test_ setting_3-- finished")


def tudataset_test(dataset_name):

    #if dataset_name not in ["AIDS", "benzene", "MUTAG","TRIANGLES"]:
    #    print("Error: dataset_name is not in ['AIDS', 'benzene', MUTAG,'TRIANGLES']")
    #    dataset_name = "AIDS"

    root_directory_input = R"C:\Users\ibra\Desktop\{}\gxl".format(dataset_name)
    if sys.platform == "linux" or sys.platform == "linux2":
        root_directory_input = "/home/ichegrane/GED_datasets/TUDataset/{}/gxl".format(dataset_name)  # ibnbadis
        #root_directory_input = "/data/chei2402/ibra/GED/TUDataset/{}/gxl".format(dataset_name)  # Goglu

    # get method name from method_name.jar (exe_jar_file) without the .jar
    method_name = exe_jar_file.split(".")[0]

    root_directory_output = "Result_TUDataset_{}_t{}/{}".format(method_name,amount_RunTime_Seconds,dataset_name)

    tudataset(root_directory_input, root_directory_output)


def tudataset_test_UB_kbest(dataset_name):

    root_directory_input = "/home/ichegrane/GED_parallel/Result_TUDataset_GED_k_best/{}".format(dataset_name)  # ibnbadis

    root_directory_output = "Result_TUDataset_GED_parallel_UB_kbest/{}".format(dataset_name)

    # test setting 1
    file_path_setting_1 = root_directory_input + os.path.sep + "test__TUDataset__setting_1.csv"
    list_g1_g2_ged_set1 = get_g1_g2_ged_from_csv(file_path_setting_1)
    test_given_combinations_with_UB_k_best(2, 4, 1, 1, list_g1_g2_ged_set1, root_directory_output, "TUDataset",
                                        "_setting_1")
    print(" test_ {} setting_1-- finished".format(dataset_name))

    # test setting 2
    file_path_setting_2 = root_directory_input + os.path.sep + "test__TUDataset__setting_2.csv"
    list_g1_g2_ged_set2 = get_g1_g2_ged_from_csv(file_path_setting_2)
    test_given_combinations_with_UB_k_best(2, 4, 1, 2, list_g1_g2_ged_set2, root_directory_output, "TUDataset", "_setting_2")
    print(" test_ {} setting_2-- finished".format(dataset_name))

    # test setting 3
    file_path_setting_3 = root_directory_input + os.path.sep + "test__TUDataset__setting_3.csv"
    list_g1_g2_ged_set3 = get_g1_g2_ged_from_csv(file_path_setting_3)
    test_given_combinations_with_UB_k_best(6, 2, 3, 1, list_g1_g2_ged_set3, root_directory_output, "TUDataset","_setting_3")
    print(" test_ {} setting_3-- finished".format(dataset_name))



def tudataset_all_benchmarcks():
    list_dataset_name = ["benzene", "MUTAG", "AIDS", "aspirin", "TRIANGLES", "MSRC_21"]
    for dataset_name in list_dataset_name:
        print("test the dataset: ", dataset_name, "---- start ---- ")
        tudataset_test(dataset_name)
        print("test the dataset: ", dataset_name, "---- finished ---- ")



def main():
    # test_benchmark, amount_run_time_s, nb_thread_ = read_args()
    # test_benchmark = read_benchmark_name_args()
    #test_benchmark = "MUTA"
    #test_benchmark = "GREC"
    #test_benchmark = "PATH"
    #test_benchmark = "acyclic"
    #test_benchmark = "alkane"
    #test_benchmark = "mao"

    list_test = [
        "MUTA",
        "GREC",
        "PATH",
        "acyclic",
        "alkane",
        "mao"
    ]

    root_directory_input = R"C:\Users\ibra\OneDrive - USherbrooke\CERIST\Ibra Chegrane Docs\Datasets adapted to the challenge\gdc-c1"
    if sys.platform == "linux" or sys.platform == "linux2":
        root_directory_input = "gdc-c1"  # linux

    root_directory_output = "Result_Grec_GED_dyn_kbest"

    for test_benchmark in list_test:
    #for test_benchmark in ["MUTA"]:
        if test_benchmark == "GREC":
            grec(root_directory_input, root_directory_output)
        elif test_benchmark == "PATH":
            path_acyclic_alkane_mao(root_directory_input, root_directory_output, "path")
        elif test_benchmark == "acyclic" or test_benchmark == "mao" or test_benchmark == "alkane":
            path_acyclic_alkane_mao(root_directory_input, root_directory_output, test_benchmark)
        elif test_benchmark == "MUTA":
            muta(root_directory_input, root_directory_output)


def test_get_g1_g2_ged():
    path_file = R"C:\Users\ibra\OneDrive - USherbrooke\CERIST\experiments_GED_parallel_TUDataset\Result_TUDataset_GED_k_best\AIDS\test__TUDataset__setting_1.csv"
    list_g1_g2_ged = get_g1_g2_ged_from_csv(path_file)

    for g1g2ged in list_g1_g2_ged:
        print("g1 : ", g1g2ged[0])
        print("g2 : ", g1g2ged[1])
        print("ged : ", g1g2ged[2])
        print("----------------------------")

if __name__ == '__main__':
    #main() # this for dataset: "MUTA", "GREC","PATH","acyclic","alkane", "mao"

    dataset_name = sys.argv[1]  # can be "benzene", "MUTAG", "AIDS", "aspirin", "TRIANGLES", "MSRC_21", or all
    amount_RunTime_Seconds = sys.argv[2]
    exe_jar_file = sys.argv[3]
    setting = sys.argv[4] # s1, s2, s3, sall

    print(" Method ({}) begin testing with input dataset ({}) and time ({}) sec for setting ({})".format(exe_jar_file,dataset_name,amount_RunTime_Seconds,setting))

    if dataset_name == "all":
        tudataset_all_benchmarcks()
    else:
        tudataset_test(dataset_name)

