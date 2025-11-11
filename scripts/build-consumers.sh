cd ../consumers/mongodb_entitiy_decorator
docker build . -t mongodb-entity-extractor

cd ../rabbit_mq_kg_builder
docker build . -t rabbit-mq-graph-builder

cd ../pdfs_to_kg_builder
docker build . -t pdf_graph_builder