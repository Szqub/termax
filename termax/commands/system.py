from typing import Dict, List, Optional, Tuple
import subprocess
import psutil
import os
from pathlib import Path

class SystemCommands:
    @staticmethod
    def get_disk_usage(path: str = "/") -> Dict:
        """
        Zwraca informacje o użyciu dysku
        """
        usage = psutil.disk_usage(path)
        return {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent
        }
        
    @staticmethod
    def get_memory_info() -> Dict:
        """
        Zwraca informacje o pamięci systemowej
        """
        mem = psutil.virtual_memory()
        return {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "percent": mem.percent
        }
        
    @staticmethod
    def get_process_info(pid: int) -> Dict:
        """
        Zwraca informacje o procesie
        """
        try:
            process = psutil.Process(pid)
            return {
                "pid": process.pid,
                "name": process.name(),
                "status": process.status(),
                "cpu_percent": process.cpu_percent(),
                "memory_percent": process.memory_percent(),
                "create_time": process.create_time()
            }
        except psutil.NoSuchProcess:
            return {}
            
    @staticmethod
    def kill_process(pid: int) -> bool:
        """
        Zabija proces o podanym PID
        """
        try:
            process = psutil.Process(pid)
            process.kill()
            return True
        except psutil.NoSuchProcess:
            return False
            
    @staticmethod
    def create_backup(source: str, destination: str) -> Tuple[bool, str]:
        """
        Tworzy backup katalogu
        """
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.exists():
                return False, f"Źródło {source} nie istnieje"
                
            if not dest_path.parent.exists():
                dest_path.parent.mkdir(parents=True)
                
            subprocess.run(["tar", "-czf", str(dest_path), str(source_path)], check=True)
            return True, f"Backup utworzony w {destination}"
        except Exception as e:
            return False, str(e)
            
    @staticmethod
    def create_cron_job(command: str, schedule: str) -> Tuple[bool, str]:
        """
        Tworzy zadanie cron
        """
        try:
            cron_line = f"{schedule} {command}\n"
            with open("/etc/crontab", "a") as f:
                f.write(cron_line)
            return True, "Zadanie cron utworzone"
        except Exception as e:
            return False, str(e)
            
    @staticmethod
    def get_system_info() -> Dict:
        """
        Zwraca informacje o systemie
        """
        return {
            "os": os.name,
            "platform": os.sys.platform,
            "processor": os.sys.getconf("SC_NPROCESSORS_ONLN"),
            "python_version": os.sys.version
        } 