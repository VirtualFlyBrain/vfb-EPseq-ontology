

# Slot: licence 


_Licence for the Dataset (all CC-BY 4.0 for scExpressionAtlas)._





URI: [dc:licence](http://purl.org/dc/terms/licence)
Alias: licence

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetEP](DatasetEP.md) | Avoids a keyerror from attempting to use Dataset class from VFB_scRNAseq_sche... |  no  |
| [Dataset](Dataset.md) |  |  no  |







## Properties

* Range: [Thing](Thing.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | AnnotationAssertion( dc:licence {id} {V} ) |




### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | dc:licence |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/licence |




## LinkML Source

<details>
```yaml
name: licence
annotations:
  owl.fstring:
    tag: owl.fstring
    value: AnnotationAssertion( dc:licence {id} {V} )
description: Licence for the Dataset (all CC-BY 4.0 for scExpressionAtlas).
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: dc:licence
alias: licence
owner: Dataset
domain_of:
- Dataset
range: Thing

```
</details>