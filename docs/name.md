

# Slot: name


_Short systematic label for the entity._



URI: [rdfs:label](http://www.w3.org/2000/01/rdf-schema#label)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Dataset](Dataset.md) |  |  no  |
| [Cluster](Cluster.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [DatasetEP](DatasetEP.md) | Avoids a keyerror from attempting to use Dataset class from VFB_scRNAseq_sche... |  no  |
| [Assay](Assay.md) |  |  no  |
| [ExpressionPattern](ExpressionPattern.md) |  |  no  |
| [Clustering](Clustering.md) |  |  no  |
| [Sample](Sample.md) |  |  no  |







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