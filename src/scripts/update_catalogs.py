import os
from bs4 import BeautifulSoup

class Catalog:
    
    def __init__(self, filename, path_to_root):
        self.filename = filename
        self.path_to_root = path_to_root
        
        with open(filename, 'r') as file:
            self.soup = BeautifulSoup(file, 'xml')
    
    def update_metadata_ontologies(self, project_id):
        """Add any new entries for upper (project metatdata) ontologies."""
        
        purl = f"http://virtualflybrain.org/data/VFB/OWL/VFB_EPseq_{project_id}.owl"
        
        exist_check = self.soup.find('uri', {"name": purl})
        if not exist_check:
            self.soup.catalog.group.append(
                self.soup.new_tag('uri', attrs={
                    "id": "User Entered Import Resolution",
                    "name": purl,
                    "uri" : f"{self.path_to_root}ontology_files/VFB_EPseq_{project_id}.owl"}))


    def update_expression_ontologies(self, project_id):
        """Add any new entries for expression ontologies."""
        
        exp_chunks = [filename.split('_')[2].replace('.owl', '')  for filename in os.listdir("expression_data") if (filename.endswith('.owl') and filename.split('_')[1]==project_id)]
        
        for chunk in exp_chunks:
            purl = f"http://purl.obolibrary.org/obo/VFB_EPseq/expression_data/dataset_{project_id}_{chunk}.owl"
            
            exist_check = self.soup.find('uri', {"name": purl})
            if not exist_check:
                self.soup.catalog.group.append(
                    self.soup.new_tag('uri', attrs={
                        "id": "User Entered Import Resolution",
                        "name": purl,
                        "uri" : f"{self.path_to_root}expression_data/dataset_{project_id}_{chunk}.owl"}))


    def update_external_imports(self, project_id):
        """Add any new entries for ontologies of external terms."""

        purl = f"http://purl.obolibrary.org/obo/VFB_EPseq/imports/{project_id}_import.owl"
        
        exist_check = self.soup.find('uri', {"name": purl})
        if not exist_check:
            # Update upper_catalog only if the tag doesn't exist
            self.soup.catalog.group.append(
                self.soup.new_tag('uri', attrs={
                    "id": "User Entered Import Resolution",
                    "name": purl,
                    "uri" : f"{self.path_to_root}imports/{project_id}_import.owl"}))


    def write_file(self):
        with open(self.filename, 'w') as file:
            file.write(self.soup.prettify())


if __name__ == "__main__":
    
    upper_catalog = Catalog(filename = "catalog-v001.xml", path_to_root = "")
    lower_catalog = Catalog(filename = "ontology_files/catalog-v001.xml", path_to_root = "../")
    
    # internal ontologies must already be in ontology_files and expression_data
    datasets = [filename.split('_')[2].replace('.owl', '')  for filename in os.listdir("ontology_files") if filename.endswith('.owl')]
    
    for dataset in datasets:
        upper_catalog.update_metadata_ontologies(dataset)
        upper_catalog.update_expression_ontologies(dataset)
        upper_catalog.update_external_imports(dataset)
        upper_catalog.write_file()
        lower_catalog.update_expression_ontologies(dataset)
        lower_catalog.update_external_imports(dataset)
        lower_catalog.write_file()


