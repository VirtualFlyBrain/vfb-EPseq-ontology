# script for basic reformatting of sample metadata files - may need tweaking for each dataset
from bs4 import BeautifulSoup
import sys
import pandas as pd
from vfb_connect.cross_server_tools import VfbConnect
vc_dev = VfbConnect(neo_endpoint='http://pdb-dev.virtualflybrain.org')
vc_kb = VfbConnect(neo_endpoint='http://kb.virtualflybrain.org')

dataset = sys.argv[1]
infile = "../data_files/%s/%s_sample_metadata.xml" % (dataset, dataset)
outfile = "../data_files/%s/%s_sample_metadata.tsv" % (dataset, dataset)

with open(infile) as fp:
    soup = BeautifulSoup(fp, 'xml')
"""
pretty_soup = soup.prettify()
with open(infile, "w") as file:
    file.write(pretty_soup)
"""
class Sample:
    # Class to hold sample metadata (not giving a 'title' for now) - convert driver_symbol to VFB id later.
    def __init__(self, id='', name='', driver_symbol='', sample_tissue='', sex='', stage='', associated_dataset='', associated_assay=''):
        self.id = id
        self.name = name
        self.driver_symbol = driver_symbol
        self.sample_tissue = sample_tissue
        self.sex = sex
        self.stage = stage
        self.associated_dataset = associated_dataset
        self.associated_assay = associated_assay
    def make_table_row(self):
        data = {'id':[self.id], 'name':[self.name], 'driver_symbol':[self.driver_symbol], 'sample_tissue':[self.sample_tissue], 'sex':[self.sex], 'stage':[self.stage], 'associated_dataset':[self.associated_dataset], 'associated_assay':[self.associated_assay], 'neo_label':['Sample']}
        return pd.DataFrame.from_dict(data=data, orient='columns').set_index('id')

# NEED TO MODIFY THIS FOR EACH DATASET
sample_data = pd.DataFrame()
for s in soup.find_all('BioSample'):
    # make sure there is a driver before making row
    if s.Attributes.find(attribute_name='external driver id').string.strip() == 'NA':
        continue
    else:
        sample = Sample(id = 'NCBI_SAM:' + s['accession'])
        sample.name = s.Description.Title.string.strip()
        sample.sample_tissue = s.Attributes.find(attribute_name='tissue').string.strip()
        #sample.sex =
        sample.stage = 'FBdv:00005369'
        sample.associated_dataset = 'NCBI_PRJ:' + dataset
        sample.driver_symbol = s.Attributes.find(attribute_name='external driver id').string.strip()
        #sample.associated_assay =

    new_row = sample.make_table_row()
    sample_data = pd.concat([sample_data, new_row])

# map tissues to FBbt
fbbt_dict = {'head': 'FBbt:00000004', 'dissected opticlobe after lamina removal':'FBbt:00003701', 'lamina dissected from optic lobe': 'FBbt:00003708'}
sample_data['sample_tissue'] = sample_data['sample_tissue'].map(fbbt_dict)

# convert driver symbols to IDs

# get VFB XP IDs based on 'external driver id'
unmatched_symbols = []
def get_vfb_id(key, unmatched_list=unmatched_symbols):
    try:
        return vc_kb.lookup[key]
    except(KeyError):
        try:
            return vc_dev.lookup[key]
        except(KeyError):
            unmatched_list.append(key)

sample_data['driver'] = sample_data['driver_symbol'].apply(get_vfb_id)
unmatched_symbols = set(unmatched_symbols)
print(unmatched_symbols)
sample_data.to_csv(outfile, sep='\t')


# need:
# id, driver, associated_dataset, label, neo_label (=Sample)
# (sample_tissue), (associated_assay), (stage), (sex)
