

# Slot: title


_Short description of the entity._



URI: [IAO:0000115](http://purl.obolibrary.org/obo/IAO_0000115)



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
name: title
annotations:
  owl:
    tag: owl
    value: AnnotationAssertion
description: Short description of the entity.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: IAO:0000115
alias: title
domain_of:
- Class
range: string
recommended: true

```
</details>