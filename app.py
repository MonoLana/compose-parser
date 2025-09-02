import docker_compose_parser as cp
parser = cp.DockerComposeParser()
result = parser.parse_compose_file('docker-compose.yaml')
print(result)