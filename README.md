# 🐳 Docker Compose Parser

> Transform your Docker Compose files into structured JSON format with ease!

A Python parser that converts Docker Compose YAML files into a consistent, normalized JSON structure. Perfect for analysis, validation, or integration with other tools.

## 🚀 Features

- ✅ **Consistent Structure**: Every service gets standardized fields, even if empty
- 🛡️ **Type Safety**: Handles various YAML formats gracefully
- 🔍 **Ghost Network Detection**: Identifies networks referenced but not defined
- 📊 **Meta Analysis**: Extracts version info and network usage patterns
- 🎯 **Field Normalization**: Converts all formats to predictable types

## 📦 Installation

```bash
pip install pyyaml
```

## 🎯 Quick Start

```python
from docker_compose_parser import DockerComposeParser

# Parse from file
parser = DockerComposeParser()
result = parser.parse_compose_file('docker-compose.yml')

# Parse from string
yaml_content = """
version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
"""
result = parser.parse_compose_string(yaml_content)

print(result)
```

## 📝 Input & Output Example

### Input (Docker Compose)
```yaml
version: '3.8'
services:
  frontend:
    image: my-frontend:latest
    ports:
      - "3000:3000"
    networks:
      - app-net
    depends_on:
      - backend
  backend:
    build: ./backend
    expose:
      - "8000"
    networks:
      - app-net
      - db-net  # Ghost network!
networks:
  app-net:
    driver: bridge
```

### Output (Structured JSON)
```json
{
  "meta": {
    "version": "3.8",
    "using_default_network": false
  },
  "services": {
    "frontend": {
      "image": "my-frontend:latest",
      "build": null,
      "ports": ["3000:3000"],
      "expose": [],
      "networks": ["app-net"],
      "network_mode": null,
      "depends_on": ["backend"],
      "links": [],
      "volumes": []
    },
    "backend": {
      "image": null,
      "build": "./backend",
      "ports": [],
      "expose": ["8000"],
      "networks": ["app-net", "db-net"],
      "network_mode": null,
      "depends_on": [],
      "links": [],
      "volumes": []
    }
  },
  "networks": {
    "app-net": {
      "driver": "bridge"
    }
  },
  "volumes": {}
}
```

## 🎨 What Makes It Special?

### 🏗️ **Consistent Structure**
Every service always has the same fields, making it predictable to work with:
```python
# Always available, never KeyError!
service['ports']     # Always list
service['networks']  # Always list  
service['image']     # String or null
```

### 🔍 **Smart Detection**
- **Ghost Networks**: `db-net` referenced but not defined
- **Default Network Usage**: Detects services without explicit networks
- **Format Variations**: Handles short and long syntax automatically

### 🛡️ **Robust Parsing**
```python
# Handles all these port formats:
ports: ["3000:3000"]              # ✅ String
ports: [3000]                     # ✅ Integer  
ports:                            # ✅ Long format
  - target: 3000
    published: 3000
```

## 📚 Usage Patterns

### Basic Analysis
```python
parser = DockerComposeParser()
result = parser.parse_compose_file('docker-compose.yml')

# Check if using default network
if result['meta']['using_default_network']:
    print("⚠️ Some services use default network")

# List all exposed ports
for name, service in result['services'].items():
    if service['ports']:
        print(f"🌐 {name}: {service['ports']}")
```

### Network Analysis
```python
# Find ghost networks
defined_networks = set(result['networks'].keys())
used_networks = set()

for service in result['services'].values():
    used_networks.update(service['networks'])

ghost_networks = used_networks - defined_networks
if ghost_networks:
    print(f"👻 Ghost networks: {ghost_networks}")
```
