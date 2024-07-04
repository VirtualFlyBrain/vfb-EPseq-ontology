import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("dataset", help="dataset to process", type=str)
args = parser.parse_args()
dataset = args.dataset
row_limit = 3000 # limit each tsv to this many rows
group_size = 100 # limit each expression (owl) file to this many samples

# EXPRESSION DATA
expression_data = pd.read_csv("../data_files/%s/%s_expression_FINAL.tsv" % (dataset, dataset), sep='\t')

# max split dataset samples into groups of no more than group_size
samples = sorted(expression_data['id'].unique())

sample_groups = -(-len(samples) // group_size) # number of ontologies to make (when merging ofns)
sample_grouping_dict = {}
while sample_groups > 0:
    start = (sample_groups-1) * group_size
    end = sample_groups * group_size
    if end > len(samples):
        end = len(samples)
    sample_grouping_dict.update({s:sample_groups for s in samples[start:end]})
    sample_groups = sample_groups - 1

# make a a tsv for each sample
print(str(len(samples)) + ' samples')
for s in samples:
    sample_data = expression_data[expression_data['id']==s]
    sample_data = sample_data.assign(hide_in_terminfo = 'true')
    sample_id = s.replace("NCBI_SAM:", "")
    dataset_group = sample_grouping_dict[s]
    chunk_counter = -(-len(sample_data) // row_limit) # number of chunks to split file
    while chunk_counter > 0:
        start = (chunk_counter-1) * row_limit
        end = chunk_counter * row_limit
        if end > len(sample_data):
            end = len(sample_data)
        sample_data_chunk = sample_data[start:end]
        sample_data_chunk.to_csv("expression_data/dataset_%s_%s-sample_%s_chunk_%s.tsv" %(dataset, dataset_group, sample_id, chunk_counter), sep='\t', index=None)
        chunk_counter = chunk_counter - 1
