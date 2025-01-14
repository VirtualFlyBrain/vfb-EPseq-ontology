

# Slot: sample_tissue


_Tissue(s) (FBbt IDs) in the sample. Multiple IDs should be separated with '|' or in different rows. Maps as an overlaps relationship rather than part_of due to imprecision of dissection._





URI: [RO:0002131](http://purl.obolibrary.org/obo/RO_0002131)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ExpressionPattern](ExpressionPattern.md) |  |  no  |
| [Sample](Sample.md) |  |  no  |







## Properties

* Range: [Thing](Thing.md)

* Multivalued: True





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | ClassAssertion( ObjectSomeValuesFrom( RO:0002131 {V} ) {id} ) |



### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | RO:0002131 |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/:sample_tissue |




## LinkML Source

<details>
```yaml
name: sample_tissue
annotations:
  owl.fstring:
    tag: owl.fstring
    value: ClassAssertion( ObjectSomeValuesFrom( RO:0002131 {V} ) {id} )
description: Tissue(s) (FBbt IDs) in the sample. Multiple IDs should be separated
  with '|' or in different rows. Maps as an overlaps relationship rather than part_of
  due to imprecision of dissection.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: RO:0002131
alias: sample_tissue
owner: Sample
domain_of:
- Sample
range: Thing
multivalued: true

```
</details>