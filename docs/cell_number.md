

# Slot: cell_number 


_The number of cells in the Cluster (as integer)._





URI: [neo_custom:cell_count](http://n2o.neo/custom/cell_count)
Alias: cell_number

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Cluster](Cluster.md) |  |  no  |







## Properties

* Range: [Integer](Integer.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl | AnnotationProperty |




### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | neo_custom:cell_count |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/cell_number |




## LinkML Source

<details>
```yaml
name: cell_number
annotations:
  owl:
    tag: owl
    value: AnnotationProperty
description: The number of cells in the Cluster (as integer).
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: neo_custom:cell_count
alias: cell_number
owner: Cluster
domain_of:
- Cluster
range: integer

```
</details>