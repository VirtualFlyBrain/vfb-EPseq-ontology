

# Slot: accession 


_Accession of the Dataset at the given Site._





URI: [neo_custom:accession](http://n2o.neo/custom/accession)
Alias: accession

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Dataset](Dataset.md) |  |  no  |
| [DatasetEP](DatasetEP.md) | Avoids a keyerror from attempting to use Dataset class from VFB_scRNAseq_sche... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [Dataset](Dataset.md) |
| Slot URI | [neo_custom:accession](http://n2o.neo/custom/accession) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Owner | [Dataset](Dataset.md) |












## Identifier and Mapping Information





### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | neo_custom:accession |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/accession |




## LinkML Source

<details>
```yaml
name: accession
description: Accession of the Dataset at the given Site.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: neo_custom:accession
alias: accession
owner: Dataset
domain_of:
- Dataset
range: string

```
</details>