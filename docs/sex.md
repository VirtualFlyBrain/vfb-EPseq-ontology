

# Slot: sex 


_Sex for the entity. Should be 'male' or 'female'._





URI: [BFO:0000050](http://purl.obolibrary.org/obo/BFO_0000050)
Alias: sex

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Cluster](Cluster.md) |  |  no  |
| [ExpressionPattern](ExpressionPattern.md) |  |  no  |
| [Sample](Sample.md) |  |  no  |







## Properties

* Range: [SexOptions](SexOptions.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | ClassAssertion( ObjectSomeValuesFrom( BFO:0000050 {V} ) {id} ) |




### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | BFO:0000050 |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/sex |




## LinkML Source

<details>
```yaml
name: sex
annotations:
  owl.fstring:
    tag: owl.fstring
    value: ClassAssertion( ObjectSomeValuesFrom( BFO:0000050 {V} ) {id} )
description: Sex for the entity. Should be 'male' or 'female'.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: BFO:0000050
alias: sex
domain_of:
- Sample
- Cluster
range: sex_options

```
</details>