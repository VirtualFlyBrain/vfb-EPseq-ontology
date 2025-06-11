

# Slot: associated_sample_for_assay 


_Input sample(s) for the scRNAseq assay. Multiple IDs should be separated with '|' or in different rows._





URI: [RO:0002233](http://purl.obolibrary.org/obo/RO_0002233)
Alias: associated_sample_for_assay

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Assay](Assay.md) |  |  no  |







## Properties

* Range: [Sample](Sample.md)

* Multivalued: True





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
| self | RO:0002233 |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/associated_sample_for_assay |




## LinkML Source

<details>
```yaml
name: associated_sample_for_assay
annotations:
  owl:
    tag: owl
    value: ObjectPropertyAssertion
description: Input sample(s) for the scRNAseq assay. Multiple IDs should be separated
  with '|' or in different rows.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: RO:0002233
alias: associated_sample_for_assay
owner: Assay
domain_of:
- Assay
range: Sample
multivalued: true

```
</details>