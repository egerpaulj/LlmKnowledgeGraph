docker run \
    -d --rm \
    -p 7474:7474 -p 7687:7687 \
    --name neo4j-apoc \
    --network development_network \
    --hostname neo4j-apoc \
    --volume=/home/user/docker/volumes/neo4j/data:/data \
    -e NEO4J_AUTH=neo4j/password \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4J_PLUGINS=\[\"apoc\"\] \
    -e NEO4J_dbms_usage__report_enabled=false \
    neo4j:2025.03
