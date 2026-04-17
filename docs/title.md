

# Slot: title 


_Short description of the entity._





URI: [IAO:0000115](http://purl.obolibrary.org/obo/IAO_0000115)
Alias: title

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Cluster](Cluster.md) |  |  no  |
| [Sample](Sample.md) |  |  no  |
| [Assay](Assay.md) |  |  no  |
| [Clustering](Clustering.md) |  |  no  |
| [DatasetEP](DatasetEP.md) | Avoids a keyerror from attempting to use Dataset class from VFB_scRNAseq_sche... |  no  |
| [ExpressionPattern](ExpressionPattern.md) |  |  no  |
| [Class](Class.md) |  |  no  |
| [Dataset](Dataset.md) |  |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [Class](Class.md) |
| Slot URI | [IAO:0000115](http://purl.obolibrary.org/obo/IAO_0000115) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Recommended | Yes |










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
| self | IAO:0000115 |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/title |




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