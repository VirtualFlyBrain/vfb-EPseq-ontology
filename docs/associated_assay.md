

# Slot: associated_assay


_Assay(s) that use this sample. Multiple IDs should be separated with '|' or in different rows._



URI: [RO:0002352](http://purl.obolibrary.org/obo/RO_0002352)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ExpressionPattern](ExpressionPattern.md) |  |  no  |
| [Sample](Sample.md) |  |  no  |







## Properties

* Range: [Assay](Assay.md)

* Multivalued: True





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl | ObjectPropertyAssertion |



### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## LinkML Source

<details>
```yaml
name: associated_assay
annotations:
  owl:
    tag: owl
    value: ObjectPropertyAssertion
description: Assay(s) that use this sample. Multiple IDs should be separated with
  '|' or in different rows.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: RO:0002352
multivalued: true
alias: associated_assay
owner: Sample
domain_of:
- Sample
range: Assay

```
</details>