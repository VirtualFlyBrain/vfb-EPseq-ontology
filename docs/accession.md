

# Slot: accession


_Accession of the Dataset at the given Site._





URI: [neo_custom:accession](http://n2o.neo/custom/accession)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DatasetEP](DatasetEP.md) | Avoids a keyerror from attempting to use Dataset class from VFB_scRNAseq_sche... |  no  |
| [Dataset](Dataset.md) |  |  no  |







## Properties

* Range: [String](String.md)





## Identifier and Mapping Information







### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | neo_custom:accession |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/:accession |




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