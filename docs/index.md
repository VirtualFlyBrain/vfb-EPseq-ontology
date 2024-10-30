# VFB_EPseq



URI: http://github.org/vfb/vfb-EPseq-ontology/VFB_EPseq

Name: VFB_EPseq



## Classes

| Class | Description |
| --- | --- |
| [Thing](Thing.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Class](Class.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Assay](Assay.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Cluster](Cluster.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Clustering](Clustering.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Dataset](Dataset.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DatasetEP](DatasetEP.md) | Avoids a keyerror from attempting to use Dataset class from VFB_scRNAseq_schema directly. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Sample](Sample.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ExpressionPattern](ExpressionPattern.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Publication](Publication.md) | None |



## Slots

| Slot | Description |
| --- | --- |
| [accession](accession.md) | Accession of the Dataset at the given Site |
| [assay_type](assay_type.md) | Assay type (FBcv ID) for the Dataset, this will probably be 'FBcv:0009000' ('... |
| [associated_assay](associated_assay.md) | Assay(s) that use this sample |
| [associated_clustering](associated_clustering.md) | Clustering (FBlc ID) that the Cluster belongs to |
| [associated_dataset](associated_dataset.md) | Dataset (FBlc ID) that the Sample or Cluster belongs to |
| [associated_sample_for_assay](associated_sample_for_assay.md) | Input sample(s) for the scRNAseq assay |
| [associated_sample_or_assay_for_clustering](associated_sample_or_assay_for_clustering.md) | Sample or Assay (FBlc ID) that the Clustering uses |
| [cell_number](cell_number.md) | The number of cells in the Cluster (as integer) |
| [cell_type](cell_type.md) | Anatomy (FBbt IDs) for the Cluster |
| [driver](driver.md) | Expression pattern class (VFB ID) that this sample is an instance of |
| [driver_symbol](driver_symbol.md) | Symbol for driver - not incorporated into ontology |
| [expression_extent](expression_extent.md) | Extent of expression of the given gene |
| [expression_level](expression_level.md) | Level of expression of the given gene |
| [filtered_gene_count](filtered_gene_count.md) | Total number of distinct genes associated with the entity after filtering by ... |
| [gene](gene.md) | A gene (FBgn ID) that is expressed by the entity |
| [hide_in_terminfo](hide_in_terminfo.md) | Flag to hide expression edges in VFB Term Info pane |
| [id](id.md) | Identifier for the entity |
| [licence](licence.md) | Licence for the Dataset (all CC-BY 4 |
| [method](method.md) | Method used for the assay - currently getting any direct subclass of FBcv:000... |
| [name](name.md) | Short systematic label for the entity |
| [neo_label](neo_label.md) | neo4j node label to add to entity |
| [notes](notes.md) | Column for curator notes - not incorporated into ontology |
| [pub_dataset](pub_dataset.md) | DataSet for the publication - created and used in tsv processing - not incorp... |
| [publication](publication.md) | Publication associated with the Dataset |
| [sample_tissue](sample_tissue.md) | Tissue(s) (FBbt IDs) in the sample |
| [sex](sex.md) | Sex for the entity |
| [site](site.md) | VFB site node curie |
| [stage](stage.md) | Developmental stage (FBdv ID) of the Sample or Cluster |
| [title](title.md) | Short description of the entity |
| [total_gene_count](total_gene_count.md) | Total number of distinct genes associated with the entity before filtering by... |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [SexOptions](SexOptions.md) |  |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Curie](Curie.md) | a compact URI |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
