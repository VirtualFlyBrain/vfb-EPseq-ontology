

# Class: ExpressionPattern 



URI: [http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/ExpressionPattern](http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/ExpressionPattern)






```mermaid
 classDiagram
    class ExpressionPattern
    click ExpressionPattern href "../ExpressionPattern"
      Sample <|-- ExpressionPattern
        click Sample href "../Sample"
      
      ExpressionPattern : associated_assay
        
          
    
        
        
        ExpressionPattern --> "*" Assay : associated_assay
        click Assay href "../Assay"
    

        
      ExpressionPattern : associated_dataset
        
          
    
        
        
        ExpressionPattern --> "0..1" Dataset : associated_dataset
        click Dataset href "../Dataset"
    

        
      ExpressionPattern : driver
        
          
    
        
        
        ExpressionPattern --> "0..1" Thing : driver
        click Thing href "../Thing"
    

        
      ExpressionPattern : driver_symbol
        
      ExpressionPattern : expression_level
        
      ExpressionPattern : gene
        
          
    
        
        
        ExpressionPattern --> "0..1" Thing : gene
        click Thing href "../Thing"
    

        
      ExpressionPattern : hide_in_terminfo
        
      ExpressionPattern : id
        
      ExpressionPattern : name
        
      ExpressionPattern : neo_label
        
      ExpressionPattern : notes
        
      ExpressionPattern : sample_tissue
        
          
    
        
        
        ExpressionPattern --> "*" Thing : sample_tissue
        click Thing href "../Thing"
    

        
      ExpressionPattern : sex
        
          
    
        
        
        ExpressionPattern --> "0..1" SexOptions : sex
        click SexOptions href "../SexOptions"
    

        
      ExpressionPattern : stage
        
          
    
        
        
        ExpressionPattern --> "0..1" Thing : stage
        click Thing href "../Thing"
    

        
      ExpressionPattern : title
        
      
```





## Inheritance
* [Thing](Thing.md)
    * [Class](Class.md)
        * [Sample](Sample.md)
            * **ExpressionPattern**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [gene](gene.md) | 0..1 <br/> [Thing](Thing.md) | A gene (FBgn ID) that is expressed by the entity | direct |
| [expression_level](expression_level.md) | 0..1 <br/> [Float](Float.md) | Level of expression of the given gene | direct |
| [hide_in_terminfo](hide_in_terminfo.md) | 0..1 <br/> [String](String.md) | Flag to hide expression edges in VFB Term Info pane | direct |
| [notes](notes.md) | 0..1 <br/> [String](String.md) | Column for curator notes - not incorporated into ontology | direct |
| [driver_symbol](driver_symbol.md) | 0..1 <br/> [String](String.md) | Symbol for driver - not incorporated into ontology | direct |
| [driver](driver.md) | 0..1 <br/> [Thing](Thing.md) | Expression pattern class (VFB ID) that this sample is an instance of | direct |
| [stage](stage.md) | 0..1 <br/> [Thing](Thing.md) | Developmental stage (FBdv ID) of the Sample or Cluster | [Sample](Sample.md) |
| [associated_dataset](associated_dataset.md) | 0..1 <br/> [Dataset](Dataset.md) | Dataset (FBlc ID) that the Sample or Cluster belongs to | [Sample](Sample.md) |
| [sex](sex.md) | 0..1 <br/> [SexOptions](SexOptions.md) | Sex for the entity | [Sample](Sample.md) |
| [neo_label](neo_label.md) | 0..1 <br/> [String](String.md) | neo4j node label to add to entity | [Sample](Sample.md) |
| [sample_tissue](sample_tissue.md) | * <br/> [Thing](Thing.md) | Tissue(s) (FBbt IDs) in the sample | [Sample](Sample.md) |
| [associated_assay](associated_assay.md) | * <br/> [Assay](Assay.md) | Assay(s) that use this sample | [Sample](Sample.md) |
| [name](name.md) | 0..1 _recommended_ <br/> [String](String.md) | Short systematic label for the entity | [Class](Class.md) |
| [title](title.md) | 0..1 _recommended_ <br/> [String](String.md) | Short description of the entity | [Class](Class.md) |
| [id](id.md) | 1 <br/> [Uriorcurie](Uriorcurie.md) | Identifier for the entity | [Thing](Thing.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/ExpressionPattern |
| native | http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq/ExpressionPattern |







## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ExpressionPattern
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
is_a: Sample
slots:
- gene
- expression_level
- hide_in_terminfo
attributes:
  notes:
    name: notes
    description: Column for curator notes - not incorporated into ontology.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    domain_of:
    - ExpressionPattern
  driver_symbol:
    name: driver_symbol
    description: Symbol for driver - not incorporated into ontology.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    domain_of:
    - ExpressionPattern
  driver:
    name: driver
    annotations:
      owl.fstring:
        tag: owl.fstring
        value: ClassAssertion( {V} {id} )
    description: Expression pattern class (VFB ID) that this sample is an instance
      of.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    domain_of:
    - ExpressionPattern
    range: Thing
    multivalued: false

```
</details>

### Induced

<details>
```yaml
name: ExpressionPattern
from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
is_a: Sample
attributes:
  notes:
    name: notes
    description: Column for curator notes - not incorporated into ontology.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    alias: notes
    owner: ExpressionPattern
    domain_of:
    - ExpressionPattern
    range: string
  driver_symbol:
    name: driver_symbol
    description: Symbol for driver - not incorporated into ontology.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    alias: driver_symbol
    owner: ExpressionPattern
    domain_of:
    - ExpressionPattern
    range: string
  driver:
    name: driver
    annotations:
      owl.fstring:
        tag: owl.fstring
        value: ClassAssertion( {V} {id} )
    description: Expression pattern class (VFB ID) that this sample is an instance
      of.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    alias: driver
    owner: ExpressionPattern
    domain_of:
    - ExpressionPattern
    range: Thing
    multivalued: false
  gene:
    name: gene
    annotations:
      owl.template:
        tag: owl.template
        value: "{% if gene %}\nClassAssertion ( \n    Annotation ( neo_custom:hide_in_terminfo\
          \ {{hide_in_terminfo}} ) \n    Annotation ( neo_custom:expression_level\
          \ {{expression_level}} ) \n    {% if expression_extent %}\n    Annotation\
          \ ( neo_custom:expression_extent {{expression_extent}} ) \n    {% endif\
          \ %}\n    ObjectSomeValuesFrom ( RO:0002292 {{gene}}) {{id}})\n{% endif\
          \ %}"
    description: A gene (FBgn ID) that is expressed by the entity. Max one gene per
      tsv row alongside its expression_level, expression_extent (for scRNAseq clusters)
      and hide_in_terminfo (=true).
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    slot_uri: RO:0002292
    alias: gene
    owner: ExpressionPattern
    domain_of:
    - ExpressionPattern
    - Cluster
    range: Thing
  expression_level:
    name: expression_level
    description: Level of expression of the given gene.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    slot_uri: neo_custom:expression_level
    alias: expression_level
    owner: ExpressionPattern
    domain_of:
    - ExpressionPattern
    - Cluster
    range: float
  hide_in_terminfo:
    name: hide_in_terminfo
    description: Flag to hide expression edges in VFB Term Info pane. Range must be
      string - boolean changes capitalisation and does not add datatype anyway.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    slot_uri: neo_custom:hide_in_terminfo
    alias: hide_in_terminfo
    owner: ExpressionPattern
    domain_of:
    - ExpressionPattern
    - Cluster
    range: string
  stage:
    name: stage
    annotations:
      owl.fstring:
        tag: owl.fstring
        value: ClassAssertion( ObjectSomeValuesFrom( RO:0002490 {V} ) {id} )
    description: Developmental stage (FBdv ID) of the Sample or Cluster.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    slot_uri: RO:0002490
    alias: stage
    owner: ExpressionPattern
    domain_of:
    - Sample
    - Cluster
    range: Thing
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
    owner: ExpressionPattern
    domain_of:
    - Sample
    - Assay
    - Clustering
    - Cluster
    range: Dataset
  sex:
    name: sex
    annotations:
      owl.fstring:
        tag: owl.fstring
        value: ClassAssertion( ObjectSomeValuesFrom( BFO:0000050 {V} ) {id} )
    description: Sex for the entity. Should be 'male' or 'female'.
    from_schema: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq
    rank: 1000
    slot_uri: BFO:0000050
    alias: sex
    owner: ExpressionPattern
    domain_of:
    - Sample
    - Cluster
    range: sex_options
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
    owner: ExpressionPattern
    domain_of:
    - Dataset
    - Sample
    - Assay
    - Cluster
    - Publication
    range: string
  sample_tissue:
    name: sample_tissue
    annotations:
      owl.fstring:
        tag: owl.fstring
        value: ClassAssertion( ObjectSomeValuesFrom( RO:0002131 {V} ) {id} )
    description: Tissue(s) (FBbt IDs) in the sample. Multiple IDs should be separated
      with '|' or in different rows. Maps as an overlaps relationship rather than
      part_of due to imprecision of dissection.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    slot_uri: RO:0002131
    alias: sample_tissue
    owner: ExpressionPattern
    domain_of:
    - Sample
    range: Thing
    multivalued: true
  associated_assay:
    name: associated_assay
    annotations:
      owl:
        tag: owl
        value: ObjectPropertyAssertion
    description: Assay(s) that use this sample. Multiple IDs should be separated with
      '|' or in different rows.
    from_schema: http://github.org/vfb/vfb-scRNAseq-ontology/VFB_scRNAseq
    rank: 1000
    slot_uri: RO:0002352
    alias: associated_assay
    owner: ExpressionPattern
    domain_of:
    - Sample
    range: Assay
    multivalued: true
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
    owner: ExpressionPattern
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
    owner: ExpressionPattern
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
    owner: ExpressionPattern
    domain_of:
    - Thing
    range: uriorcurie
    required: true

```
</details>