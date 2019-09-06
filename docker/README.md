# docker

Examples for running services stacks using `docker swarm`.  I reserve the right to change this to `docker-compose` or even `kubernetes`

## What is Docker?
## Containers and Images
### Inspect
```bash
docker image ls
docker container ls
```
# docker swarm
## What is Docker Swarm?
## Stacks and Services
### Initialize
This only needs to be done once when you first install `docker`
```bash
docker swarm init
```
### Inspect
```bash
docker stack deploy -c FILE.yml NAME

docker service ls
docker stack ls

docker service ps --no-trunc NAME_service
```

### Remove
```bash
docker stack rm NAME
```

# neo4j

### Setup
```bash
mkdir -p ${HOME}/docker/neo4j/{databases,logs,plugins}

(cd ${HOME}/docker/neo4j/plugins; curl -sSLOJ https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/3.4.0.7/apoc-3.4.0.7-all.jar)

mv graph.db ${HOME}/docker/neo4j/databases/
```

# Jupyter

```bash
mkdir -p "${HOME}/docker/jupyter"
```

```bash
# usage: jupyter STACK_NAME
jupyter() {
	local id="$(docker stack ps -f 'desired-state=running' --format '{{.Name}}.{{.ID}}' --no-trunc "$1")"
	local json="$(docker container exec "${id}" jupyter notebook list --json)"
	local url="$(python -c 'import sys,json;j=json.load(sys.stdin);print("http://127.0.0.1:%(port)s/?token=%(token)s"%j)' <<< "${json}")"
	open "${url}"
	#xdg-open "${url}"
}
```
