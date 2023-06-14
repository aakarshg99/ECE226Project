# ECE226Project
GNN-NAS Project

### How To Run
Due to the large resource requirements of GNN-NAS you will need a GPU to run this project. Given that we have added a Jupyter Notebook file that can easily run the code by cloning the repo to your Google Drive and running from there. Steps to get it working,
* Download Run_From_Notebook.ipynb
* Upload to Google Colab
* Run the cells (You will need to sign in to your google account)

Otherwise if you would like to clone and set up the repo yourself then to create the benchmarks for the cora dataset run the following after you are set up,
python path/to/repo/code/search-cora.py
and for the pubmed dataset,
python path/to/repo/code/search-pubmed.py

### Output
Output architectures and metrics will be printed to standard out as well as saved in cora_bench.txt and pubmed_bench.txt. The format of the output is as follows,

Architecture  (0 -> T, 1 -> P)
Validation Accuracy, Test Accuracy
Number of Parameters
Latency


### Troubleshooting
If you have any path issues for the dataset then alter the path on line 35 of search_cora.py/search_pubmed.py accordingly. 
