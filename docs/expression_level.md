

# Slot: expression_level 


_Level of expression of the given gene._





URI: [neo_custom:expression_level](http://n2o.neo/custom/expression_level)
Alias: expression_level

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Cluster](Cluster.md) |  |  no  |
| [ExpressionPattern](ExpressionPattern.md) |  |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Float](Float.md) |
| Domain Of | [ExpressionPattern](ExpressionPattern.md), [Cluster](Cluster.md) |
| Slot URI | [neo_custom:expression_level](http://n2o.neo/custom/expression_level) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | neo_custom:expression_level |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/expression_level |




## LinkML Source

<details>
```yaml
name: expression_level
description: Level of expression of the given gene.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: neo_custom:expression_level
alias: expression_level
domain_of:
- ExpressionPattern
- Cluster
range: float

```
</details>