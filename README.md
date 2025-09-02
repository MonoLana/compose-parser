# 🐳 Docker Compose Parser

> Simple Python tool to convert Docker Compose files into structured JSON

## 🤔 What is this?

Ever wanted to analyze your Docker Compose files programmatically? This parser converts messy YAML into clean, predictable JSON structure.

**Before:**
```yaml
services:
  web:
    image: nginx
    ports: ["80:80"]
```

**After:**
```json
{
  "services": {
    "web": {
      "image": "nginx",
      "build": null,
      "ports": ["80:80"],
      "expose": [],
      "networks": [],
      "volumes": []
    }
  }
}
```

## 🚀 Quick Start

**Step 1:** Download `docker_compose_parser.py`

**Step 2:** Use it!

```python
import docker_compose_parser

# Parse your compose file
parser = docker_compose_parser.DockerComposeParser()
result = parser.parse_compose_file('docker-compose.yml')

print(result)
```

## ✨ What You Get

### 🏗️ **Consistent Structure**
Every service always has the same fields - no more `KeyError`!

```python
# These will ALWAYS exist:
service['ports']      # List of ports
service['networks']   # List of networks  
service['image']      # String or null
service['volumes']    # List of volumes
```

### 🔍 **Smart Analysis**
```python
result = parser.parse_compose_file('docker-compose.yml')

# Check if services use default network
if result['meta']['using_default_network']:
    print("⚠️ Some services rely on default network")

# Find all exposed ports
for name, service in result['services'].items():
    if service['ports']:
        print(f"🌐 {name} exposes: {service['ports']}")
```

### 🛡️ **Handles Everything**
Works with all Docker Compose formats:
- Short and long syntax
- Missing fields (fills with defaults)  
- Complex nested structures
- Version 2.x and 3.x files

## 💡 Use Cases

- **🔍 Compose Analysis:** Find unused networks, ghost references
- **📊 Documentation:** Generate service diagrams  
- **🛠️ Migration Tools:** Convert between formats
- **🔐 Security Scans:** Analyze port exposure
- **📈 Monitoring:** Extract service dependencies

## 🎯 Real Example

```python
import docker_compose_parser

parser = docker_compose_parser.DockerComposeParser()
result = parser.parse_compose_file('docker-compose.yml')

# Find services without health checks
for name, service in result['services'].items():
    if not service.get('healthcheck'):
        print(f"⚠️ {name} has no health check")

# List all database services  
db_services = []
for name, service in result['services'].items():
    if 'postgres' in service['image'] or 'mysql' in service['image']:
        db_services.append(name)

print(f"📊 Database services: {db_services}")
```

## 🧩 Simple Example
```python
import docker_compose_parser as cp
parser = cp.DockerComposeParser()
result = parser.parse_compose_file('docker-compose.yaml')
print(result)
```


## 📦 Dependencies

```bash
pip install pyyaml
```

That's it! Just one dependency.

## 🤝 Contributing

Found a Docker Compose format that breaks? Open an issue with your YAML file!

---

<div align="center">
<strong>Simple. Reliable. No surprises.</strong>
</div>