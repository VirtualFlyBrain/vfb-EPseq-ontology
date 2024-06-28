

# Slot: publication


_Publication associated with the Dataset._



URI: [dcterms:references](http://purl.org/dc/terms/references)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetEP](DatasetEP.md) | Avoids a keyerror from attempting to use Dataset class from VFB_scRNAseq_sche... |  no  |
| [Dataset](Dataset.md) |  |  no  |







## Properties

* Range: [Publication](Publication.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | AnnotationAssertion( dcterms:references {id} {V} ) |



### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## LinkML Source

<details>
```yaml
name: publication
annotations:
  owl.fstring:
    tag: owl.fstring
    value: AnnotationAssertion( dcterms:references {id} {V} )
description: Publication associated with the Dataset.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: dcterms:references
alias: publication
owner: Dataset
domain_of:
- Dataset
range: Publication

```
</details>