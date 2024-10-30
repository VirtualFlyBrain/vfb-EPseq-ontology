

# Slot: publication


_Publication associated with the Dataset._



URI: [dc:references](http://purl.org/dc/terms/references)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Dataset](Dataset.md) |  |  no  |
| [DatasetEP](DatasetEP.md) | Avoids a keyerror from attempting to use Dataset class from VFB_scRNAseq_sche... |  no  |







## Properties

* Range: [Publication](Publication.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | AnnotationAssertion( dc:references {id} {V} ) |



### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dc:references |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/:publication |




## LinkML Source

<details>
```yaml
name: publication
annotations:
  owl.fstring:
    tag: owl.fstring
    value: AnnotationAssertion( dc:references {id} {V} )
description: Publication associated with the Dataset.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: dc:references
alias: publication
owner: Dataset
domain_of:
- Dataset
range: Publication

```
</details>