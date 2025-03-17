

# Slot: filtered_gene_count


_Total number of distinct genes associated with the entity after filtering by extent._





URI: [neo_custom:filtered_gene_count](http://n2o.neo/custom/filtered_gene_count)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Cluster](Cluster.md) |  |  no  |
| [Dataset](Dataset.md) |  |  no  |
| [DatasetEP](DatasetEP.md) | Avoids a keyerror from attempting to use Dataset class from VFB_scRNAseq_sche... |  no  |







## Properties

* Range: [Integer](Integer.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl | AnnotationProperty |



### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | neo_custom:filtered_gene_count |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/:filtered_gene_count |




## LinkML Source

<details>
```yaml
name: filtered_gene_count
annotations:
  owl:
    tag: owl
    value: AnnotationProperty
description: Total number of distinct genes associated with the entity after filtering
  by extent.
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: neo_custom:filtered_gene_count
alias: filtered_gene_count
domain_of:
- Dataset
- Cluster
range: integer

```
</details>