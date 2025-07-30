

# Slot: site 


_VFB site node curie. The site must be created in VFB and added to the dictionary in ../scripts/process_site_data.py to successfully map from FB data._





URI: [oboInOwl:hasDbXref](http://www.geneontology.org/formats/oboInOwl#hasDbXref)
Alias: site

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Dataset](Dataset.md) |  |  no  |
| [DatasetEP](DatasetEP.md) | Avoids a keyerror from attempting to use Dataset class from VFB_scRNAseq_sche... |  no  |







## Properties

* Range: [Thing](Thing.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | AnnotationAssertion( Annotation( neo_custom:accession {accession} ) oboInOwl:hasDbXref {id} {V} ) |




### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | oboInOwl:hasDbXref |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/site |




## LinkML Source

<details>
```yaml
name: site
annotations:
  owl.fstring:
    tag: owl.fstring
    value: AnnotationAssertion( Annotation( neo_custom:accession {accession} ) oboInOwl:hasDbXref
      {id} {V} )
description: VFB site node curie. The site must be created in VFB and added to the
  dictionary in ../scripts/process_site_data.py to successfully map from FB data.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: oboInOwl:hasDbXref
alias: site
owner: Dataset
domain_of:
- Dataset
range: Thing

```
</details>