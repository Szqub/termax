from typing import Dict, List, Optional, Tuple
import subprocess
import socket
import nmap
import requests
from pathlib import Path
import json

class NetworkCommands:
    def __init__(self):
        self.nm = nmap.PortScanner()
        
    def scan_host(self, host: str, ports: str = "1-1000") -> Dict:
        """
        Skanuje host na otwarte porty
        """
        try:
            self.nm.scan(host, ports)
            return {
                "host": host,
                "state": self.nm[host].state(),
                "ports": [
                    {
                        "port": port,
                        "state": data["state"],
                        "service": data.get("name", "unknown")
                    }
                    for port, data in self.nm[host]["tcp"].items()
                ]
            }
        except Exception as e:
            return {"error": str(e)}
            
    def ping_host(self, host: str, count: int = 4) -> Dict:
        """
        Wykonuje ping na host
        """
        try:
            result = subprocess.run(
                ["ping", "-c", str(count), host],
                capture_output=True,
                text=True
            )
            return {
                "host": host,
                "success": result.returncode == 0,
                "output": result.stdout
            }
        except Exception as e:
            return {"error": str(e)}
            
    def check_web_service(self, url: str) -> Dict:
        """
        Sprawdza dostępność usługi webowej
        """
        try:
            response = requests.get(url, timeout=5)
            return {
                "url": url,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content_type": response.headers.get("content-type")
            }
        except Exception as e:
            return {"error": str(e)}
            
    def get_dns_info(self, domain: str) -> Dict:
        """
        Pobiera informacje DNS dla domeny
        """
        try:
            return {
                "domain": domain,
                "ip": socket.gethostbyname(domain),
                "hostname": socket.gethostbyaddr(domain)[0]
            }
        except Exception as e:
            return {"error": str(e)}
            
    def create_network_report(self, host: str, output_file: str) -> Tuple[bool, str]:
        """
        Tworzy raport z analizy sieciowej
        """
        try:
            report = {
                "host": host,
                "scan_results": self.scan_host(host),
                "ping_results": self.ping_host(host),
                "dns_info": self.get_dns_info(host)
            }
            
            output_path = Path(output_file)
            output_path.write_text(json.dumps(report, indent=2))
            return True, f"Raport zapisany w {output_file}"
        except Exception as e:
            return False, str(e)
            
    def check_ports(self, host: str, ports: List[int]) -> Dict:
        """
        Sprawdza stan konkretnych portów
        """
        try:
            results = {}
            for port in ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                results[port] = "open" if result == 0 else "closed"
                sock.close()
            return {
                "host": host,
                "ports": results
            }
        except Exception as e:
            return {"error": str(e)} 