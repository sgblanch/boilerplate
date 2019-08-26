# docker

Examples for running services using `docker swarm`.  I reserve the right to change this to `docker-compose` or even `kubernetes`

## neo4j

### Setup
```bash
mkdir -p ${HOME}/docker/{data,logs}/neo4j
mkdir ${HOME}/docker/data/neo4j/databases

mv graph.db ${HOME}/docker/data/neo4j/databases/
```

### Starting
```bash
docker swarm init
docker stack deploy -c neo4j.yml mykb
```

### Inspect or debug
```bash
docker image ls
docker container ls
docker service ps mykb_neo4j --no-trunc
```

### Destroy
```bash
docker stack rm mykb
```