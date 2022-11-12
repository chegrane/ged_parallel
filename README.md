# **ged_parallel** : Solving Graph Edit Distance (ged) in parallel.
Graph Edit Distance (GED) is a well-known measure used in the graph matching to measure the similarity/dissimilarity between two graphs by computing the minimum cost of edit operations needed to transform one graph into another. This process, Which appears to be simple, is known NP-hard and time consuming since the search space is increasing exponentially. One way to optimally solve this problem is by using Branch and Bound (B&B) algorithms, Which reduce the computation time required to explore the whole search space by performing an implicit enumeration of the search space instead of an exhaustive one based on a pruning technique. nevertheless, They remain inefficient when dealing with large problem instances due to the impractical running time needed to explore the whole search space. To overcome this issue, We propose in [this paper](https://www.sciencedirect.com/science/article/pii/S0167819122000734) three parallel B&B approaches based on shared memory to exploit the multi-core CPU processors: First, a work-stealing approach where several instances of the B&B algorithm explore a single search tree concurrently achieving speedups up to 24× faster than the sequential version. Second, a tree-based approach where multiple parts of the search tree are explored simultaneously by independent B&B instances achieving speedups up to 28×. Finally, Due to the irregular nature of the GED problem, two load-balancing strategies are proposed to ensure a fair workload between parallel processes achieving impressive speedups up to 300×. all experiments have been carried out on well-known datasets.

- Our paper title: ***Efficient parallel branch-and-bound approaches for exact graph edit distance problem***
- Our paper link: https://www.sciencedirect.com/science/article/pii/S0167819122000734

# Algorithms:
- Serial B&B algorithm: in subdolder *Exact_GED_BB_DF*
- Work-Stealing parallel B&B approach: in subdolder *Exat_GED_BB_DF_v1_parallel*
- Tree-based parallel B&B approach: in subdolder *Exact_GED_BB_DF_v2_parallel (high_level)*
- Tree-based parallel B&B approach with Load-balancing strategies: in subdolder *Exact_GED_BB_DF_v2_parallel (high_level) - with-load balancing*
- Tree-based parallel B&B approach with k level: in subdolder *Exact_GED_BB_DF_v2_parallel (k_level) - with-load balancing*


Each of the algorithms is implemented in java. The jar files are available in the subfolder `[algorithm_name]/out/artifacts/ged_parallel_jar/...`.

## run the algorithms:
```bash	
java -jar algorithm_file.jar c_nd_sub c_nd_del_ins c_edge_sub c_edge_del_ins file_path_g1 file_path_g2 path_output test_name amount_RunTime_Seconds NB_threads
```
Parameters:
- `c_nd_sub`: cost of node substitution
- `c_nd_del_ins`: cost of node deletion and insertion
- `c_edge_sub`: cost of edge substitution
- `c_edge_del_ins`: cost of edge deletion and insertion
- `file_path_g1`: path to the first graph in GXL format
- `file_path_g2`: path to the second graph in GXL format
- `path_output`: path to the output csv file
- `test_name`: TUDadaset for ["benzene", "MUTAG", "AIDS", "aspirin", "TRIANGLES", "MSRC_21"]. For otheer, you can use : GREC, PATH, MAO, MUTA, CMU.

# Dataset:
All datasets are in Graph exchange Language [GXL](http://www.gupro.de/GXL/) format.
In our exprements we use two datasets:
- 1) PAH, MAO, Alkane, Acyclic, and GREC, CMU and MUTA;   wich can be downloaded from [ICPR 2016 - Graph Distance Contest](https://gdc2016.greyc.fr/gdc-c1.tar.gz) 

- 2) [TUDataset](https://chrsmrrs.github.io/datasets/), Since there are different datasets with different properties, you can download a specific dataset corresponding to your need from [TUDataset download](https://chrsmrrs.github.io/datasets/docs/datasets/).
The TUDataset is not in the GXL format, so we need to convert it to GXL format. For that, we write a python script to do that `parse_graphs_tudatasets_to_gxl.py`.
For our experiments, we used the following datasets: benzene, MUTAG, AIDS, aspirin, TRIANGLES, MSRC_21.


# Experiments:
To execute the experiments, we use the main script `test_GED_scripts.py` where we generate all the combinations and settings. For TUDataset, you can use the script as follow:
```bash
nohup python test_GED_script.py dataset_name time_sec algorithm.jar setting > log_file &
```
With the following parameters:
- `dataset_name`: benzene, MUTAG, AIDS, aspirin, TRIANGLES, MSRC_21, or all (for all at the same time).
- `time_sec`: the time in seconds to run the experiments.
- `algorithm.jar`: the path to the jar file of the algorithm.
- `setting`: s1, s2, s3 (for setting 1 , 2 or 3).
- `log_file`: the path to the log file.

To use cluster, we use the script `ged_test_script.sh` for job array and `ged_test_script_one_job.sh` for one job on slurm scheduler.


# Citation
If you use our work, please cite our paper by using the following bibtex entry:
```
@article{DABAH2022102984,
title = {Efficient parallel branch-and-bound approaches for exact graph edit distance problem},
journal = {Parallel Computing},
volume = {114},
pages = {102984},
year = {2022},
issn = {0167-8191},
doi = {https://doi.org/10.1016/j.parco.2022.102984},
url = {https://www.sciencedirect.com/science/article/pii/S0167819122000734},
author = {Adel Dabah and Ibrahim Chegrane and Saïd Yahiaoui and Ahcene Bendjoudi and Nadia Nouali-Taboudjemat},
keywords = {Parallel branch-and-bound, Graph matching, Graph edit distance}
}
```
