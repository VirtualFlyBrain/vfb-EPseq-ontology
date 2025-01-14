

# Slot: cell_type


_Anatomy (FBbt IDs) for the Cluster. Multiple IDs should be separated with '|'._





URI: [RO:0002473](http://purl.obolibrary.org/obo/RO_0002473)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Cluster](Cluster.md) |  |  no  |







## Properties

* Range: [Thing](Thing.md)

* Multivalued: True





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | ClassAssertion( ObjectSomeValuesFrom( RO:0002473 {V} ) {id} ) |



### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | RO:0002473 |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/:cell_type |




## LinkML Source

<details>
```yaml
name: cell_type
annotations:
  owl.fstring:
    tag: owl.fstring
    value: ClassAssertion( ObjectSomeValuesFrom( RO:0002473 {V} ) {id} )
description: Anatomy (FBbt IDs) for the Cluster. Multiple IDs should be separated
  with '|'.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: RO:0002473
alias: cell_type
owner: Cluster
domain_of:
- Cluster
range: Thing
multivalued: true

```
</details>