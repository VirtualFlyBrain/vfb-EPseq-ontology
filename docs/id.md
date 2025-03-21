

# Slot: id


_Identifier for the entity. FlyBase identifiers should be prefixed with 'FlyBase:'._





URI: [http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/:id](http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/:id)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ExpressionPattern](ExpressionPattern.md) |  |  no  |
| [Dataset](Dataset.md) |  |  no  |
| [Assay](Assay.md) |  |  no  |
| [Sample](Sample.md) |  |  no  |
| [DatasetEP](DatasetEP.md) | Avoids a keyerror from attempting to use Dataset class from VFB_scRNAseq_sche... |  no  |
| [Thing](Thing.md) |  |  no  |
| [Cluster](Cluster.md) |  |  no  |
| [Publication](Publication.md) |  |  no  |
| [Clustering](Clustering.md) |  |  no  |
| [Class](Class.md) |  |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/:id |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/:id |




## LinkML Source

<details>
```yaml
name: id
description: Identifier for the entity. FlyBase identifiers should be prefixed with
  'FlyBase:'.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
identifier: true
alias: id
domain_of:
- Thing
range: uriorcurie
required: true

```
</details>