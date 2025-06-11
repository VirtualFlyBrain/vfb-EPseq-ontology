

# Slot: associated_dataset 


_Dataset (FBlc ID) that the Sample or Cluster belongs to._





URI: [dc:source](http://purl.org/dc/terms/source)
Alias: associated_dataset

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Cluster](Cluster.md) |  |  no  |
| [Sample](Sample.md) |  |  no  |
| [ExpressionPattern](ExpressionPattern.md) |  |  no  |
| [Assay](Assay.md) |  |  no  |
| [Clustering](Clustering.md) |  |  no  |







## Properties

* Range: [Dataset](Dataset.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | AnnotationAssertion( dc:source {id} {V} ) |




### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dc:source |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/associated_dataset |




## LinkML Source

<details>
```yaml
name: associated_dataset
annotations:
  owl.fstring:
    tag: owl.fstring
    value: AnnotationAssertion( dc:source {id} {V} )
description: Dataset (FBlc ID) that the Sample or Cluster belongs to.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: dc:source
alias: associated_dataset
domain_of:
- Sample
- Assay
- Clustering
- Cluster
range: Dataset

```
</details>