# docker

Examples for running services stacks using `docker swarm`.  I reserve the right to change this to `docker-compose` or even `kubernetes`

## What is Docker?
## Containers and Images
### Inspect
```bash
docker image ls
docker container ls
```
### Remove
```bash
docker container ls -a
docker container rm ID|NAME
docker image ls
docker image rm ID
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
mkdir -p ${HOME}/docker/neo4j/{databases,logs}

mv graph.db ${HOME}/docker/neo4j/databases/
```

# Jupyter
Two stacks are provided.  The scipy stack is python only and is 3.5GB.  The datascience stack is 5GB and includes R and julia.  There are other stacks available and switching stacks requires changing one line in the YAML file.  Read [jupyter's documentation](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#core-stacks) to see what stacks are available.

```bash
mkdir -p "${HOME}/docker/jupyter"
```

```bash
docker container ls
docker container exec ID|NAME jupyter notebook list
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
