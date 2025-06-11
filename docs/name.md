

# Slot: name 


_Short systematic label for the entity._





URI: [rdfs:label](http://www.w3.org/2000/01/rdf-schema#label)
Alias: name

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetEP](DatasetEP.md) | Avoids a keyerror from attempting to use Dataset class from VFB_scRNAseq_sche... |  no  |
| [Cluster](Cluster.md) |  |  no  |
| [Sample](Sample.md) |  |  no  |
| [ExpressionPattern](ExpressionPattern.md) |  |  no  |
| [Dataset](Dataset.md) |  |  no  |
| [Assay](Assay.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [Clustering](Clustering.md) |  |  no  |







## Properties

* Range: [String](String.md)

* Recommended: True





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl | AnnotationAssertion |




### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | rdfs:label |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/name |




## LinkML Source

<details>
```yaml
name: name
annotations:
  owl:
    tag: owl
    value: AnnotationAssertion
description: Short systematic label for the entity.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: rdfs:label
alias: name
domain_of:
- Class
range: string
recommended: true

```
</details>