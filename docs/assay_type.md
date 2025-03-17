

# Slot: assay_type


_Assay type (FBcv ID) for the Dataset, this will probably be 'FBcv:0009000' ('single-cell RNA-seq')._





URI: [OBI:0000312](http://purl.obolibrary.org/obo/OBI_0000312)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetEP](DatasetEP.md) | Avoids a keyerror from attempting to use Dataset class from VFB_scRNAseq_sche... |  no  |
| [Dataset](Dataset.md) |  |  no  |







## Properties

* Range: [Thing](Thing.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | ClassAssertion( ObjectSomeValuesFrom( OBI:0000312 {V} ) {id} ) |



### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | OBI:0000312 |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/:assay_type |




## LinkML Source

<details>
```yaml
name: assay_type
annotations:
  owl.fstring:
    tag: owl.fstring
    value: ClassAssertion( ObjectSomeValuesFrom( OBI:0000312 {V} ) {id} )
description: Assay type (FBcv ID) for the Dataset, this will probably be 'FBcv:0009000'
  ('single-cell RNA-seq').
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: OBI:0000312
alias: assay_type
owner: Dataset
domain_of:
- Dataset
range: Thing

```
</details>