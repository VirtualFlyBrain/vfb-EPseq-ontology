import pandas as pd
pd.set_option('display.max_columns', 10)
import glob
import re

# ids to modify
mapping = pd.read_csv('tmp/id_validation_table.txt', sep='\t', low_memory=False)
changed_ids = mapping[~mapping['#submitted_item'].isin(mapping['validated_id'])]
changed_ids = changed_ids.set_index('#submitted_item', verify_integrity=True)
replacement_dict = changed_ids['validated_id'].to_dict()

exp_files = glob.glob('expression_data/*.owl')

regex = re.compile("|".join(replacement_dict))

for f in exp_files:
    dataset = f.split('_')[1]
    # check whether file already contains both old and new terms for any entity
    with open((f + '.fbgns.tmp'), 'r') as genes:
        gene_list = [l.strip() for l in genes.readlines()]
    old_exists = changed_ids[changed_ids.index.isin(gene_list)]
    old_and_new = old_exists[old_exists['validated_id'].isin(gene_list)]
    if len(old_and_new) > 0: # file already has an old ID and its replacement
        print(f'Old and new ids for same entity in use in {dataset}:')
        print(old_and_new)
        print(f'Not updating file {f} - please check and edit manually.')
        raise ValueError("Usage of old and replacement gene IDs in same file!")
    if len(old_exists) == 0:
        print(f'nothing to update in {f}')
    else:
        with open(f, "r") as infile, open(f + '-processed.txt', "w+") as outfile:
            for line in infile:
                outfile.write(regex.sub(lambda m: replacement_dict[m.group()], line))
            print(f'{f} updated!')
