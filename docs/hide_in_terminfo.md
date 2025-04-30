

# Slot: hide_in_terminfo


_Flag to hide expression edges in VFB Term Info pane. Range must be string - boolean changes capitalisation and does not add datatype anyway._





URI: [neo_custom:hide_in_terminfo](http://n2o.neo/custom/hide_in_terminfo)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Cluster](Cluster.md) |  |  no  |
| [ExpressionPattern](ExpressionPattern.md) |  |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | neo_custom:hide_in_terminfo |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/:hide_in_terminfo |




## LinkML Source

<details>
```yaml
name: hide_in_terminfo
description: Flag to hide expression edges in VFB Term Info pane. Range must be string
  - boolean changes capitalisation and does not add datatype anyway.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: neo_custom:hide_in_terminfo
alias: hide_in_terminfo
domain_of:
- ExpressionPattern
- Cluster
range: string

```
</details>