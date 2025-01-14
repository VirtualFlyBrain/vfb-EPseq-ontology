# Release - update imports, merge meta, exp and imports for each ds and put zipped versions in release_files. This does not update the EPseq ontology content.
# Can't overwrite ALL_TERMS_COMBINED in file
sh run.sh make prepare_release_notest IMP=true ALL_TERMS_COMBINED=dummy.txt -B
