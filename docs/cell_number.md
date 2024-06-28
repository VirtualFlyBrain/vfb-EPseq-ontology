

# Slot: cell_number


_The number of cells in the Cluster (as integer)._



URI: [BAO:0002811](http://www.bioassayontology.org/bao#BAO_0002811)



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
| owl.fstring | DataPropertyAssertion( BAO:0002811 {id} {cell_number} ^^xsd:integer ) |



### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## LinkML Source

<details>
```yaml
name: cell_number
annotations:
  owl.fstring:
    tag: owl.fstring
    value: DataPropertyAssertion( BAO:0002811 {id} {cell_number} ^^xsd:integer )
description: The number of cells in the Cluster (as integer).
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: BAO:0002811
alias: cell_number
owner: Cluster
domain_of:
- Cluster
range: integer

```
</details>