# Yaml and Json python library to parse Docker Compose files into a JSON-like structure.
import yaml
import json
# Typing library for type hints to specify expected data types in functions and classes.
from typing import Dict, List, Any, Optional, Union

class DockerComposeParser:
    def __init__(self):
        self.default_service_structure = {
            "image": None,
            "build": None,
            "ports": [],
            "expose": [],
            "networks": [],
            "network_mode": None,
            "depends_on": [],
            "links": [],
            "volumes": []
        }
    
    def parse_compose_file(self, file_path: str) -> Dict[str, Any]:
        """Parse Docker Compose file and return JSON-like structure"""
        with open(file_path, 'r', encoding='utf-8') as file:
            compose_data = yaml.safe_load(file)
        
        return self.parse_compose_data(compose_data)
    
    def parse_compose_string(self, compose_string: str) -> Dict[str, Any]:
        """Parse Docker Compose string and return JSON-like structure"""
        compose_data = yaml.safe_load(compose_string)
        return self.parse_compose_data(compose_data)
    
    def parse_compose_data(self, compose_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Docker Compose data dictionary"""
        result = {
            "meta": self._parse_meta(compose_data),
            "services": self._parse_services(compose_data.get('services', {})),
            "networks": self._parse_networks(compose_data.get('networks', {})),
            "volumes": self._parse_volumes(compose_data.get('volumes', {}))
        }
        
        return result
    
    def _parse_meta(self, compose_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse meta information"""
        services = compose_data.get('services', {})
        using_default_network = self._check_using_default_network(services)
        
        return {
            "version": compose_data.get('version', '3.8'),
            "using_default_network": using_default_network
        }
    
    def _check_using_default_network(self, services: Dict[str, Any]) -> bool:
        """Check if any service is using default network (no explicit networks)"""
        for service_name, service_config in services.items():
            if isinstance(service_config, dict) and not service_config.get('networks'):
                return True
        return False
    
    def _parse_services(self, services: Dict[str, Any]) -> Dict[str, Any]:
        """Parse services section"""
        parsed_services = {}
        
        for service_name, service_config in services.items():
            parsed_services[service_name] = self._parse_single_service(service_config)
        
        return parsed_services
    
    def _parse_single_service(self, service_config: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a single service configuration"""
        service = self.default_service_structure.copy()
        
        # Handle case where service_config might not be a dict
        if not isinstance(service_config, dict):
            return service
        
        # Parse image
        service["image"] = service_config.get('image')
        
        # Parse build
        build_config = service_config.get('build')
        if build_config:
            if isinstance(build_config, str):
                service["build"] = build_config
            elif isinstance(build_config, dict):
                # If build is an object, convert to string representation
                service["build"] = build_config.get('context', str(build_config))
        
        # Parse ports - handle various formats
        ports_config = service_config.get('ports', [])
        service["ports"] = self._parse_ports(ports_config)
        
        # Parse expose - handle various formats
        expose_config = service_config.get('expose', [])
        service["expose"] = self._parse_expose(expose_config)
        
        # Parse networks - handle various formats
        networks_config = service_config.get('networks')
        service["networks"] = self._parse_service_networks(networks_config)
        
        # Parse network_mode
        service["network_mode"] = service_config.get('network_mode')
        
        # Parse depends_on - handle various formats
        depends_on_config = service_config.get('depends_on')
        service["depends_on"] = self._parse_depends_on(depends_on_config)
        
        # Parse links - handle various formats
        links_config = service_config.get('links', [])
        service["links"] = self._parse_links(links_config)
        
        # Parse volumes - handle various formats
        volumes_config = service_config.get('volumes', [])
        service["volumes"] = self._parse_service_volumes(volumes_config)
        
        return service
    
    def _parse_ports(self, ports: Any) -> List[str]:
        """Parse ports configuration - handle various formats"""
        if not ports:
            return []
        
        # Handle if ports is not a list
        if not isinstance(ports, list):
            ports = [ports]
        
        parsed_ports = []
        for port in ports:
            if isinstance(port, str):
                parsed_ports.append(port)
            elif isinstance(port, int):
                parsed_ports.append(str(port))
            elif isinstance(port, dict):
                # Handle long format
                target = port.get('target', '')
                published = port.get('published', '')
                if published and target:
                    parsed_ports.append(f"{published}:{target}")
                elif target:
                    parsed_ports.append(str(target))
            else:
                # Try to convert to string as fallback
                try:
                    parsed_ports.append(str(port))
                except:
                    continue
        
        return parsed_ports
    
    def _parse_expose(self, expose: Any) -> List[str]:
        """Parse expose configuration - handle various formats"""
        if not expose:
            return []
        
        # Handle if expose is not a list
        if not isinstance(expose, list):
            expose = [expose]
        
        parsed_expose = []
        for port in expose:
            try:
                parsed_expose.append(str(port))
            except:
                continue
        
        return parsed_expose
    
    def _parse_service_networks(self, networks: Any) -> List[str]:
        """Parse networks configuration for a service - handle various formats"""
        if not networks:
            return []
        
        if isinstance(networks, list):
            return [str(network) for network in networks if network is not None]
        elif isinstance(networks, dict):
            return list(networks.keys())
        elif isinstance(networks, str):
            return [networks]
        
        return []
    
    def _parse_depends_on(self, depends_on: Any) -> List[str]:
        """Parse depends_on configuration - handle various formats"""
        if not depends_on:
            return []
        
        if isinstance(depends_on, list):
            return [str(dep) for dep in depends_on if dep is not None]
        elif isinstance(depends_on, dict):
            return list(depends_on.keys())
        elif isinstance(depends_on, str):
            return [depends_on]
        
        return []
    
    def _parse_links(self, links: Any) -> List[str]:
        """Parse links configuration - handle various formats"""
        if not links:
            return []
        
        # Handle if links is not a list
        if not isinstance(links, list):
            links = [links]
        
        parsed_links = []
        for link in links:
            try:
                parsed_links.append(str(link))
            except:
                continue
        
        return parsed_links
    
    def _parse_service_volumes(self, volumes: Any) -> List[str]:
        """Parse volumes configuration for a service - handle various formats"""
        if not volumes:
            return []
        
        # Handle if volumes is not a list
        if not isinstance(volumes, list):
            volumes = [volumes]
        
        parsed_volumes = []
        for volume in volumes:
            if isinstance(volume, str):
                parsed_volumes.append(volume)
            elif isinstance(volume, dict):
                # Handle long format
                source = volume.get('source', '')
                target = volume.get('target', '')
                volume_type = volume.get('type', '')
                
                if volume_type == 'bind' and source and target:
                    parsed_volumes.append(f"{source}:{target}")
                elif volume_type == 'volume' and source and target:
                    parsed_volumes.append(f"{source}:{target}")
                elif source and target:
                    parsed_volumes.append(f"{source}:{target}")
                elif target:
                    parsed_volumes.append(target)
            else:
                # Try to convert to string as fallback
                try:
                    parsed_volumes.append(str(volume))
                except:
                    continue
        
        return parsed_volumes
    
    def _parse_networks(self, networks: Dict[str, Any]) -> Dict[str, Any]:
        """Parse networks section (only explicit networks)"""
        parsed_networks = {}
        
        for network_name, network_config in networks.items():
            if network_config is None:
                parsed_networks[network_name] = {}
            elif isinstance(network_config, dict):
                parsed_networks[network_name] = network_config
            else:
                parsed_networks[network_name] = {}
        
        return parsed_networks
    
    def _parse_volumes(self, volumes: Dict[str, Any]) -> Dict[str, Any]:
        """Parse volumes section (only explicit volumes)"""
        parsed_volumes = {}
        
        for volume_name, volume_config in volumes.items():
            if volume_config is None:
                parsed_volumes[volume_name] = {}
            elif isinstance(volume_config, dict):
                parsed_volumes[volume_name] = volume_config
            else:
                parsed_volumes[volume_name] = {}
        
        return parsed_volumes

def main():
    parser = DockerComposeParser()

if __name__ == "__main__":
    # Create parser instance
    parser = DockerComposeParser()
    
    file_path = 'node-compose.yaml' 
    
    try:
        result = parser.parse_compose_file(file_path)
        print(json.dumps(result, indent=2))
    except FileNotFoundError:
        print(f"File {file_path} tidak ditemukan!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()