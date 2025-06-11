

# Class: Assay 



URI: [FBcv:0003025](http://purl.obolibrary.org/obo/FBcv_0003025)






```mermaid
 classDiagram
    class Assay
    click Assay href "../Assay"
      Class <|-- Assay
        click Class href "../Class"
      
      Assay : associated_dataset
        
          
    
        
        
        Assay --> "0..1" Dataset : associated_dataset
        click Dataset href "../Dataset"
    

        
      Assay : associated_sample_for_assay
        
          
    
        
        
        Assay --> "*" Sample : associated_sample_for_assay
        click Sample href "../Sample"
    

        
      Assay : id
        
      Assay : method
        
          
    
        
        
        Assay --> "0..1" Thing : method
        click Thing href "../Thing"
    

        
      Assay : name
        
      Assay : neo_label
        
      Assay : title
        
      
```





## Inheritance
* [Thing](Thing.md)
    * [Class](Class.md)
        * **Assay**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [associated_dataset](associated_dataset.md) | 0..1 <br/> [Dataset](Dataset.md) | Dataset (FBlc ID) that the Sample or Cluster belongs to | direct |
| [neo_label](neo_label.md) | 0..1 <br/> [String](String.md) | neo4j node label to add to entity | direct |
| [method](method.md) | 0..1 <br/> [Thing](Thing.md) | Method used for the assay - currently getting any direct subclass of FBcv:000... | direct |
| [associated_sample_for_assay](associated_sample_for_assay.md) | * <br/> [Sample](Sample.md) | Input sample(s) for the scRNAseq assay | direct |
| [name](name.md) | 0..1 _recommended_ <br/> [String](String.md) | Short systematic label for the entity | [Class](Class.md) |
| [title](title.md) | 0..1 _recommended_ <br/> [String](String.md) | Short description of the entity | [Class](Class.md) |
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) | Identifier for the entity | [Thing](Thing.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [ExpressionPattern](ExpressionPattern.md) | [associated_assay](associated_assay.md) | range | [Assay](Assay.md) |
| [Sample](Sample.md) | [associated_assay](associated_assay.md) | range | [Assay](Assay.md) |






## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| owl.fstring | ClassAssertion( FBcv:0003025 {id} ) |




### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | FBcv:0003025 |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/Assay |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Assay
annotations:
  owl.fstring:
    tag: owl.fstring
    value: ClassAssertion( FBcv:0003025 {id} )
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
is_a: Class
slots:
- associated_dataset
- neo_label
attributes:
  method:
    name: method
    annotations:
      owl.fstring:
        tag: owl.fstring
        value: ClassAssertion( ObjectSomeValuesFrom( BAO:0000212 {V} ) {id} )
    description: Method used for the assay - currently getting any direct subclass
      of FBcv:0009005 'single-cell library sequencing' for scRNAseq data.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    slot_uri: BAO:0000212
    domain_of:
    - Assay
    range: Thing
    multivalued: false
  associated_sample_for_assay:
    name: associated_sample_for_assay
    annotations:
      owl:
        tag: owl
        value: ObjectPropertyAssertion
    description: Input sample(s) for the scRNAseq assay. Multiple IDs should be separated
      with '|' or in different rows.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    slot_uri: RO:0002233
    domain_of:
    - Assay
    range: Sample
    multivalued: true
class_uri: FBcv:0003025

```
</details>

### Induced

<details>
```yaml
name: Assay
annotations:
  owl.fstring:
    tag: owl.fstring
    value: ClassAssertion( FBcv:0003025 {id} )
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
is_a: Class
attributes:
  method:
    name: method
    annotations:
      owl.fstring:
        tag: owl.fstring
        value: ClassAssertion( ObjectSomeValuesFrom( BAO:0000212 {V} ) {id} )
    description: Method used for the assay - currently getting any direct subclass
      of FBcv:0009005 'single-cell library sequencing' for scRNAseq data.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    slot_uri: BAO:0000212
    alias: method
    owner: Assay
    domain_of:
    - Assay
    range: Thing
    multivalued: false
  associated_sample_for_assay:
    name: associated_sample_for_assay
    annotations:
      owl:
        tag: owl
        value: ObjectPropertyAssertion
    description: Input sample(s) for the scRNAseq assay. Multiple IDs should be separated
      with '|' or in different rows.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    slot_uri: RO:0002233
    alias: associated_sample_for_assay
    owner: Assay
    domain_of:
    - Assay
    range: Sample
    multivalued: true
  associated_dataset:
    name: associated_dataset
    annotations:
      owl.fstring:
        tag: owl.fstring
        value: AnnotationAssertion( dc:source {id} {V} )
    description: Dataset (FBlc ID) that the Sample or Cluster belongs to.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    slot_uri: dc:source
    alias: associated_dataset
    owner: Assay
    domain_of:
    - Sample
    - Assay
    - Clustering
    - Cluster
    range: Dataset
  neo_label:
    name: neo_label
    annotations:
      owl:
        tag: owl
        value: AnnotationProperty
    description: neo4j node label to add to entity.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    slot_uri: neo_property:nodeLabel
    alias: neo_label
    owner: Assay
    domain_of:
    - Dataset
    - Sample
    - Assay
    - Cluster
    - Publication
    range: string
  name:
    name: name
    annotations:
      owl:
        tag: owl
        value: AnnotationAssertion
    description: Short systematic label for the entity.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    slot_uri: rdfs:label
    alias: name
    owner: Assay
    domain_of:
    - Class
    range: string
    recommended: true
  title:
    name: title
    annotations:
      owl:
        tag: owl
        value: AnnotationAssertion
    description: Short description of the entity.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    slot_uri: IAO:0000115
    alias: title
    owner: Assay
    domain_of:
    - Class
    range: string
    recommended: true
  id:
    name: id
    description: Identifier for the entity. FlyBase identifiers should be prefixed
      with 'FlyBase:'.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    identifier: true
    alias: id
    owner: Assay
    domain_of:
    - Thing
    range: uriorcurie
    required: true
class_uri: FBcv:0003025

```
</details>