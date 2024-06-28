import glob
import sys

# dataset should be either 'src' or the ID of a dataset
dataset = sys.argv[1]

if dataset == 'src':
    ds_info = ''
    ds_ann_info = ' Each dataset is annotated with its source publication and GEO accession.'
    purl_filename = 'VFB_EPseq'
    ontology_file = 'VFB_EPseq-edit.ofn'
else:
    ds_info = f' for dataset {dataset}'
    ds_ann_info = ''
    purl_filename = f'VFB_EPseq_{dataset}'
    ontology_file = f'ontology_files/{dataset}_header.ofn'

ontology_lines = []
ontology_lines.extend([
'Prefix(:=<http://virtualflybrain.org/data/VFB/OWL/VFB_EPseq.owl#>)',
'Prefix(owl:=<http://www.w3.org/2002/07/owl#>)',
'Prefix(rdf:=<http://www.w3.org/1999/02/22-rdf-syntax-ns#>)',
'Prefix(xml:=<http://www.w3.org/XML/1998/namespace>)',
'Prefix(xsd:=<http://www.w3.org/2001/XMLSchema#>)',
'Prefix(rdfs:=<http://www.w3.org/2000/01/rdf-schema#>)',
'',
'',
f'Ontology(<http://virtualflybrain.org/data/VFB/OWL/{purl_filename}.owl>',
])

# import all files in the ontology_files folder to src ontology
if dataset == 'src':
    import_ont_files = glob.glob('ontology_files/*.owl')
    import_ont_statements = ['Import(<http://virtualflybrain.org/data/VFB/OWL/%s>)' % o.replace('ontology_files/', '') for o in import_ont_files]
    ontology_lines.extend(import_ont_statements)
    ontology_lines.extend(['Import(<http://purl.obolibrary.org/obo/VFB_EPseq/imports/merged_import.owl>)'])

# import ds-specific external and expression ontologies to dataset ontologies
else:
    import_ext_statement = [f'Import(<http://purl.obolibrary.org/obo/VFB_EPseq/imports/{dataset}_import.owl>)']
    ontology_lines.extend(import_ext_statement)
    import_exp_files = glob.glob('expression_data/*.owl')
    import_exp_statements = ['Import(<http://purl.obolibrary.org/obo/VFB_EPseq/%s>)' % o for o in import_exp_files if dataset in o]
    ontology_lines.extend(import_exp_statements)

ontology_lines.extend([
f'Annotation(<http://purl.org/dc/elements/1.1/description> "An ontology of Drosophila melanogaster driver expression pattern RNAseq data{ds_info}. This information is from published datasets taken from GEO.{ds_ann_info}"^^xsd:string)',
f'Annotation(<http://purl.org/dc/elements/1.1/title> "VFB expression pattern RNAseq Ontology{ds_info}"^^xsd:string)',
'Annotation(<http://purl.org/dc/terms/license> <https://creativecommons.org/licenses/by/4.0/>)',
'',
'Declaration(AnnotationProperty(<http://purl.org/dc/elements/1.1/description>))',
'Declaration(AnnotationProperty(<http://purl.org/dc/elements/1.1/title>))',
'Declaration(AnnotationProperty(<http://purl.org/dc/terms/license>))',
')'
])

with open(ontology_file, 'w+') as file:
    file.write('\n'.join(ontology_lines) + '\n')
