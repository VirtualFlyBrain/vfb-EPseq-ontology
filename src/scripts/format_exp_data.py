# script for basic reformatting of expression data files - may need tweaking for each dataset
import sys
import pandas as pd

dataset = sys.argv[1]
infile = "../data_files/%s/%s_tpm.tsv" % (dataset, dataset)
outfile = "../data_files/%s/%s_expression_formatted.tsv" % (dataset, dataset)
metadata = "../data_files/%s/%s_sample_metadata.tsv" % (dataset, dataset)

exp_df = pd.read_csv(infile, sep='\t').set_index('gene_id')
meta_df = pd.read_csv(metadata, sep='\t')

# rename columns
exp_df.rename(columns=dict(zip(meta_df["name"], meta_df["id"])), inplace=True)
exp_df.drop('gene_name', axis=1, inplace=True)

# turn samples into another layer of row index
exp_values = exp_df.stack(future_stack=True).dropna()

# filter for expression > 0
exp_values = exp_values[exp_values>0]
# make dataframe, amend colnames, add hide_in_term_info column
exp_df = exp_values.to_frame(name='expression_level').reset_index()
exp_df.rename(columns={'gene_id':'gene', 'level_1': 'id'}, inplace=True)
# keep only rows with FBgn IDs
exp_df = exp_df[exp_df['gene'].str.startswith('FBgn')]
# prefix gene IDs
exp_df['gene'] = exp_df['gene'].apply(lambda x: x.replace('FBgn', 'FlyBase:FBgn'))
# drop samples that are not in meta_df (these have been excluded)
exp_df = exp_df[exp_df['id'].isin(meta_df['id'])]
exp_df['hide_in_terminfo'] = 'true'
#exp_df['count_type'] = 'TPM'

exp_df.to_csv(outfile, sep='\t', index=None)
