

# Slot: associated_clustering 


_Clustering (FBlc ID) that the Cluster belongs to._





URI: [BFO:0000050](http://purl.obolibrary.org/obo/BFO_0000050)
Alias: associated_clustering

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Cluster](Cluster.md) |  |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Clustering](Clustering.md) |
| Domain Of | [Cluster](Cluster.md) |
| Slot URI | [BFO:0000050](http://purl.obolibrary.org/obo/BFO_0000050) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Owner | [Cluster](Cluster.md) |












## Identifier and Mapping Information



### Annotations

| property | value |
| --- | --- |
| owl | ObjectPropertyAssertion |




### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | BFO:0000050 |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/associated_clustering |




## LinkML Source

<details>
```yaml
name: associated_clustering
annotations:
  owl:
    tag: owl
    value: ObjectPropertyAssertion
description: Clustering (FBlc ID) that the Cluster belongs to.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: BFO:0000050
alias: associated_clustering
owner: Cluster
domain_of:
- Cluster
range: Clustering

```
</details>