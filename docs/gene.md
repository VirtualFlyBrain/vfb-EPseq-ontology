

# Slot: gene


_A gene (FBgn ID) that is expressed by the entity. Max one gene per tsv row alongside its expression_level, expression_extent (for scRNAseq clusters) and hide_in_terminfo (=true)._





URI: [RO:0002292](http://purl.obolibrary.org/obo/RO_0002292)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Cluster](Cluster.md) |  |  no  |
| [ExpressionPattern](ExpressionPattern.md) |  |  no  |







## Properties

* Range: [Thing](Thing.md)





## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.template | {% if gene %}
ClassAssertion ( 
    Annotation ( neo_custom:hide_in_terminfo {{hide_in_terminfo}} ) 
    Annotation ( neo_custom:expression_level {{expression_level}} ) 
    {% if expression_extent %}
    Annotation ( neo_custom:expression_extent {{expression_extent}} ) 
    {% endif %}
    ObjectSomeValuesFrom ( RO:0002292 {{gene}}) {{id}})
{% endif %} |



### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | RO:0002292 |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/:gene |




## LinkML Source

<details>
```yaml
name: gene
annotations:
  owl.template:
    tag: owl.template
    value: "{% if gene %}\nClassAssertion ( \n    Annotation ( neo_custom:hide_in_terminfo\
      \ {{hide_in_terminfo}} ) \n    Annotation ( neo_custom:expression_level {{expression_level}}\
      \ ) \n    {% if expression_extent %}\n    Annotation ( neo_custom:expression_extent\
      \ {{expression_extent}} ) \n    {% endif %}\n    ObjectSomeValuesFrom ( RO:0002292\
      \ {{gene}}) {{id}})\n{% endif %}"
description: A gene (FBgn ID) that is expressed by the entity. Max one gene per tsv
  row alongside its expression_level, expression_extent (for scRNAseq clusters) and
  hide_in_terminfo (=true).
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
rank: 1000
slot_uri: RO:0002292
alias: gene
domain_of:
- ExpressionPattern
- Cluster
range: Thing

```
</details>