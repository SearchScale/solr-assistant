#!/usr/bin/env python3
import sys
import random
import requests
import json
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ORANGE = '\033[38;5;208m'
    BRIGHT_YELLOW = '\033[38;5;226m'
    GOLD = '\033[38;5;220m'
    BRIGHT_RED = '\033[38;5;196m'
    DARK_RED = '\033[38;5;124m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_solr_logo():
    """Print the Apache Solr ASCII art logo with shadow effect and Apache animation"""
    import time
    
    # Base logo without "Apache"
    logo_base = """                                     ***  *
                                 * ****** ****                  
                              ** ****** *******                
                            **** ***** ******  **              
                             *** **** *****  *****             
                          *  **  **  ****  ********            
                          ** **  *  ***  *********             
                           *    *  **   *****   ***            
███████╗ ██████╗ ██╗     ██████╗    ***    ******            
██╔════╝██╔═══██╗██║     ██╔══██╗ *    **********            
███████╗██║   ██║██║     ██████╔╝   ******                   
╚════██║██║   ██║██║     ██╔══██╗                 
███████║╚██████╔╝███████╗██║  ██║                 
╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝                 
    """
    
    # Final logo with "Apache" in position
    logo_final = """                                     ***  *
                                 * ****** ****                  
                              ** ****** *******                
                            **** ***** ******  **              
                             *** **** *****  *****             
                          *  **  **  ****  ********            
Apache                    ** **  *  ***  *********             
                           *    *  **   *****   ***            
███████╗ ██████╗ ██╗     ██████╗    ***    ******            
██╔════╝██╔═══██╗██║     ██╔══██╗ *    **********            
███████╗██║   ██║██║     ██████╔╝   ******                   
╚════██║██║   ██║██║     ██╔══██╗                 
███████║╚██████╔╝███████╗██║  ██║                 
╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝                 
    """
    
    # Define subtle gradient colors for SOLR letters (left to right)
    gradient_colors = [
        '\033[38;5;230m',  # Very light yellow
        '\033[38;5;229m',  # Light yellow
        '\033[38;5;228m',  # Pale yellow
        '\033[38;5;227m',  # Soft yellow
        '\033[38;5;186m',  # Yellow-cream
        '\033[38;5;185m',  # Light cream
        '\033[38;5;179m',  # Cream
        '\033[38;5;144m',  # Warm cream
        '\033[38;5;138m',  # Deep cream
    ]
    
    def print_colored_lines(lines):
        for line in lines:
            colored_line = ""
            gradient_index = 0
            for char in line:
                if char == '*':
                    # Sun rays in bright red/orange gradient
                    colored_line += Colors.BRIGHT_RED + Colors.BOLD + char
                elif char == '█':
                    # Main text blocks with gradient effect
                    color = gradient_colors[gradient_index % len(gradient_colors)]
                    colored_line += Colors.BOLD + color + char
                    gradient_index += 1
                elif char in '╗╚╝║═╔╦╩╬':
                    # Box drawing characters for shadow effect with gradient
                    color = gradient_colors[gradient_index % len(gradient_colors)]
                    colored_line += color + char
                    gradient_index += 1
                else:
                    colored_line += char
            print(colored_line + Colors.RESET)
    
    # First display the base logo
    base_lines = logo_base.split('\n')
    print_colored_lines(base_lines)
    
    # Animate "Apache" sliding down from top
    apache_positions = [0, 1, 2, 3, 4, 5, 6]  # Line positions for animation
    target_line = 6  # Final position of "Apache"
    
    for pos in apache_positions:
        time.sleep(0.15)  # Animation speed
        print("\033[H")  # Move cursor to top
        
        # Create animated frame
        animated_lines = base_lines.copy()
        if pos == target_line:
            # Final position - show "Apache" in correct place with original content preserved
            animated_lines[pos] = "Apache                    ** **  *  ***  *********             "
        else:
            # Show "Apache" at current animation position, preserving original line content
            if pos < len(animated_lines):
                original_line = animated_lines[pos]
                if len(original_line) > 26:  # If line has content beyond position 26
                    # Insert "Apache" at the beginning, preserve content after position 26
                    animated_lines[pos] = "Apache" + " " * 20 + original_line[26:]
                else:
                    # Just add "Apache" with padding
                    animated_lines[pos] = "Apache" + " " * (max(0, len(original_line) - 6))
        
        print_colored_lines(animated_lines)
        
    # Small pause before continuing
    time.sleep(0.3)

def print_logo():
    """Print simple banner"""
    print(f"\n{Colors.ORANGE}{'─' * 50}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.ORANGE}    Apache Solr Search and AI Assistant{Colors.RESET}")
    print(f"{Colors.ORANGE}{'─' * 50}{Colors.RESET}\n")

def animate_loading():
    """Simple loading animation"""
    import time
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(10):
        for frame in frames:
            print(f"\r{Colors.ORANGE}{frame} Initializing Solr Assistant...{Colors.RESET}", end="", flush=True)
            time.sleep(0.05)
    print("\r" + " " * 30 + "\r", end="")  # Clear the line

# TODO: We should ideally use a Python Solr client instead of making HTTP calls
class SolrConnection:
    """Manages connection to Apache Solr instance"""
    
    def __init__(self):
        self.base_url: Optional[str] = None
        self.connected: bool = False
        self.solr_info: Dict = {}
    
    def connect(self, url: str) -> bool:
        """Connect to Solr instance"""
        try:
            # Normalize URL
            if not url.startswith(('http://', 'https://')):
                url = f'http://{url}'
            
            parsed = urlparse(url)
            if not parsed.port and not parsed.netloc.endswith(':8983'):
                if ':' not in parsed.netloc:
                    url = url.rstrip('/') + ':8983'
            
            self.base_url = url.rstrip('/')
            
            # Test connection
            metrics_url = urljoin(self.base_url + '/', 'solr/admin/metrics')
            
            print(f"{Colors.CYAN}Connecting to Solr at {self.base_url}...{Colors.RESET}")
            
            response = requests.get(metrics_url, timeout=10)
            response.raise_for_status()
            
            metrics_data = response.json()
            self.solr_info = self._extract_info(metrics_data)
            self.connected = True
            
            print(f"{Colors.GREEN}Successfully connected to Apache Solr!{Colors.RESET}\n")
            self._display_info()
            
            return True
            
        except requests.exceptions.ConnectionError:
            print(f"{Colors.RED}Failed to connect to {url}. Is Solr running?{Colors.RESET}")
            return False
        except requests.exceptions.Timeout:
            print(f"{Colors.RED}Connection timeout to {url}{Colors.RESET}")
            return False
        except requests.exceptions.HTTPError as e:
            print(f"{Colors.RED}HTTP error: {e}{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{Colors.RED}Unexpected error: {e}{Colors.RESET}")
            return False
    
    def _extract_info(self, metrics_data: Dict) -> Dict:
        """Extract Solr information from metrics"""
        info = {}
        
        try:
            if 'metrics' in metrics_data:
                metrics = metrics_data['metrics']
                
                # JVM metrics
                jvm_metrics = metrics.get('solr.jvm', {})
                if jvm_metrics:
                    info['memory_heap_used'] = jvm_metrics.get('memory.heap.used')
                    info['memory_heap_max'] = jvm_metrics.get('memory.heap.max')
                    info['memory_heap_usage'] = jvm_metrics.get('memory.heap.usage')
                    info['memory_non_heap_used'] = jvm_metrics.get('memory.non-heap.used')
                    info['memory_non_heap_max'] = jvm_metrics.get('memory.non-heap.max')
                    info['memory_total_used'] = jvm_metrics.get('memory.total.used')
                    info['memory_total_committed'] = jvm_metrics.get('memory.total.committed')
                    
                    info['os_name'] = jvm_metrics.get('os.name')
                    info['os_arch'] = jvm_metrics.get('os.arch')
                    info['os_version'] = jvm_metrics.get('os.version')
                    info['os_available_processors'] = jvm_metrics.get('os.availableProcessors')
                    info['os_system_load_average'] = jvm_metrics.get('os.systemLoadAverage')
                    info['os_process_cpu_load'] = jvm_metrics.get('os.processCpuLoad')
                    info['os_system_cpu_load'] = jvm_metrics.get('os.systemCpuLoad')
                    info['os_free_physical_memory'] = jvm_metrics.get('os.freePhysicalMemorySize')
                    info['os_total_physical_memory'] = jvm_metrics.get('os.totalPhysicalMemorySize')
                    info['os_open_file_descriptors'] = jvm_metrics.get('os.openFileDescriptorCount')
                    info['os_max_file_descriptors'] = jvm_metrics.get('os.maxFileDescriptorCount')
                    
                    system_props = jvm_metrics.get('system.properties', {})
                    if system_props:
                        info['java_version'] = system_props.get('java.specification.version')
                        info['java_vendor'] = system_props.get('java.vendor')
                        info['java_vm_name'] = system_props.get('java.vm.name')
                        info['solr_home'] = system_props.get('solr.solr.home')
                        info['solr_log_dir'] = system_props.get('solr.log.dir')
            
            # Try to get version from system info
            if 'version' not in info:
                try:
                    system_url = urljoin(self.base_url + '/', 'solr/admin/info/system')
                    system_response = requests.get(system_url, timeout=5)
                    system_data = system_response.json()
                    
                    if 'lucene' in system_data:
                        lucene_info = system_data['lucene']
                        if 'solr-spec-version' in lucene_info:
                            info['version'] = lucene_info['solr-spec-version']
                        if 'lucene-spec-version' in lucene_info:
                            info['lucene_version'] = lucene_info['lucene-spec-version']
                    
                    if 'jvm' in system_data:
                        jvm_info = system_data['jvm']
                        if 'version' in jvm_info:
                            info['java_version'] = jvm_info['version']
                
                except Exception:
                    pass
            
        except Exception:
            pass
        
        return info
    
    def _display_info(self):
        """Display Solr connection information"""
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.WHITE}  Apache Solr Instance Details{Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        
        # URL
        print(f"{Colors.GREEN}URL:{Colors.RESET} {Colors.WHITE}{self.base_url}{Colors.RESET}")
        
        # Solr Version
        if self.solr_info.get('version'):
            print(f"{Colors.GREEN}Solr Version:{Colors.RESET} {Colors.WHITE}{self.solr_info['version']}{Colors.RESET}")
        
        # Lucene Version
        if self.solr_info.get('lucene_version'):
            print(f"{Colors.GREEN}Lucene Version:{Colors.RESET} {Colors.WHITE}{self.solr_info['lucene_version']}{Colors.RESET}")
        
        # Java Version
        if self.solr_info.get('java_version'):
            print(f"{Colors.GREEN}Java Version:{Colors.RESET} {Colors.WHITE}{self.solr_info['java_version']}{Colors.RESET}")
        
        # JVM
        if self.solr_info.get('java_vm_name'):
            print(f"{Colors.GREEN}JVM:{Colors.RESET} {Colors.WHITE}{self.solr_info['java_vm_name']}{Colors.RESET}")
        
        # OS
        if self.solr_info.get('os_name'):
            os_info = f"{self.solr_info['os_name']}"
            if self.solr_info.get('os_arch'):
                os_info += f" ({self.solr_info['os_arch']})"
            if self.solr_info.get('os_version'):
                os_info += f" - {self.solr_info['os_version']}"
            print(f"{Colors.GREEN}OS:{Colors.RESET} {Colors.WHITE}{os_info}{Colors.RESET}")
        
        # CPU Cores
        if self.solr_info.get('os_available_processors'):
            print(f"{Colors.GREEN}CPU Cores:{Colors.RESET} {Colors.WHITE}{self.solr_info['os_available_processors']}{Colors.RESET}")
        
        # Heap Memory
        if self.solr_info.get('memory_heap_used') and self.solr_info.get('memory_heap_max'):
            try:
                used = int(self.solr_info['memory_heap_used'])
                max_mem = int(self.solr_info['memory_heap_max'])
                used_mb = used // (1024 * 1024)
                max_mb = max_mem // (1024 * 1024)
                usage_pct = self.solr_info.get('memory_heap_usage', 0) * 100
                
                usage_color = Colors.WHITE
                if usage_pct > 80:
                    usage_color = Colors.RED
                elif usage_pct > 60:
                    usage_color = Colors.YELLOW
                
                print(f"{Colors.GREEN}Heap Memory:{Colors.RESET} {usage_color}{used_mb}MB / {max_mb}MB ({usage_pct:.1f}%){Colors.RESET}")
            except (ValueError, TypeError):
                pass
        
        # Non-Heap Memory
        if self.solr_info.get('memory_non_heap_used'):
            try:
                used = int(self.solr_info['memory_non_heap_used'])
                used_mb = used // (1024 * 1024)
                print(f"{Colors.GREEN}Non-Heap Memory:{Colors.RESET} {Colors.WHITE}{used_mb}MB{Colors.RESET}")
            except (ValueError, TypeError):
                pass
        
        # Physical Memory
        if self.solr_info.get('os_free_physical_memory') and self.solr_info.get('os_total_physical_memory'):
            try:
                free = int(self.solr_info['os_free_physical_memory'])
                total = int(self.solr_info['os_total_physical_memory'])
                used = total - free
                free_gb = free // (1024 * 1024 * 1024)
                total_gb = total // (1024 * 1024 * 1024)
                used_gb = used // (1024 * 1024 * 1024)
                usage_pct = (used / total) * 100
                print(f"{Colors.GREEN}Physical Memory:{Colors.RESET} {Colors.WHITE}{used_gb}GB / {total_gb}GB ({usage_pct:.1f}% used, {free_gb}GB free){Colors.RESET}")
            except (ValueError, TypeError):
                pass
        
        # Solr Home
        if self.solr_info.get('solr_home'):
            print(f"{Colors.GREEN}Solr Home:{Colors.RESET} {Colors.WHITE}{self.solr_info['solr_home']}{Colors.RESET}")
        
        # Log Directory
        if self.solr_info.get('solr_log_dir'):
            print(f"{Colors.GREEN}Log Directory:{Colors.RESET} {Colors.WHITE}{self.solr_info['solr_log_dir']}{Colors.RESET}")
        
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}\n")
    
    def disconnect(self):
        """Disconnect from Solr"""
        self.base_url = None
        self.connected = False
        self.solr_info = {}
        print(f"{Colors.YELLOW}Disconnected from Solr{Colors.RESET}")
    
    def get_status(self) -> str:
        """Get connection status"""
        if self.connected:
            return f"Connected to {self.base_url}"
        else:
            return "Not connected"
    
    def list_collections(self) -> bool:
        """List all collections in Solr"""
        if not self.connected:
            print(f"{Colors.RED}Not connected to Solr. Use 'connect' command first.{Colors.RESET}")
            return False
        
        try:
            # Try SolrCloud mode
            collections_url = urljoin(self.base_url + '/', 'solr/admin/collections?action=LIST')
            response = requests.get(collections_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('responseHeader', {}).get('status') == 0:
                collections = data.get('collections', [])
                self._display_collections(collections, mode="cloud")
                return True
            else:
                return self._try_list_cores()
                
        except Exception:
            return self._try_list_cores()
    
    def _try_list_cores(self) -> bool:
        """List cores in standalone Solr mode"""
        try:
            cores_url = urljoin(self.base_url + '/', 'solr/admin/cores?action=STATUS')
            response = requests.get(cores_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('responseHeader', {}).get('status') == 0:
                cores = list(data.get('status', {}).keys())
                self._display_collections(cores, mode="standalone")
                return True
            else:
                print(f"{Colors.RED}Failed to retrieve collections/cores{Colors.RESET}")
                return False
                
        except Exception as e:
            print(f"{Colors.RED}Error listing collections/cores: {e}{Colors.RESET}")
            return False
    
    def _display_collections(self, collections: List[str], mode: str = "cloud"):
        """Display collections"""
        mode_label = "Collections" if mode == "cloud" else "Cores"
        
        print(f"\n{mode_label} ({mode.title()} Mode):")
        print("-" * 40)
        
        if not collections:
            print(f"No {mode_label.lower()} found")
        else:
            print(f"Found {len(collections)} {mode_label.lower()}:\n")
            
            for i, collection in enumerate(collections, 1):
                print(f"  {i}. {collection}")
        
        print()
    
    def summarize_collection(self, collection_name: str) -> bool:
        """Get summary of a collection"""
        if not self.connected:
            print(f"{Colors.RED}Not connected to Solr. Use 'connect' command first.{Colors.RESET}")
            return False
        
        try:
            print(f"Analyzing collection '{collection_name}'...")
            
            # Get document count
            count_url = urljoin(self.base_url + '/', f'solr/{collection_name}/select')
            count_response = requests.get(count_url, params={'q': '*:*', 'rows': 0}, timeout=10)
            count_response.raise_for_status()
            count_data = count_response.json()
            total_docs = count_data['response']['numFound']
            
            # Get schema information
            schema_url = urljoin(self.base_url + '/', f'solr/{collection_name}/schema')
            schema_response = requests.get(schema_url, timeout=10)
            schema_response.raise_for_status()
            schema_data = schema_response.json()
            
            fields = schema_data['schema']['fields']
            dynamic_fields = schema_data['schema']['dynamicFields']
            
            # Get sample documents
            field_usage = {}
            sample_docs = []
            if total_docs > 0:
                sample_url = urljoin(self.base_url + '/', f'solr/{collection_name}/select')
                sample_response = requests.get(
                    sample_url,
                    params={'q': '*:*', 'rows': min(100, total_docs)},
                    timeout=10
                )
                sample_response.raise_for_status()
                sample_data = sample_response.json()
                sample_docs = sample_data['response']['docs'][:3]
                
                # Analyze field usage
                for doc in sample_data['response']['docs']:
                    for field_name in doc.keys():
                        if field_name not in ['_version_', '_root_']:
                            field_usage[field_name] = field_usage.get(field_name, 0) + 1
            
            # Display summary
            self._display_summary(
                collection_name, total_docs, fields, dynamic_fields, 
                field_usage, sample_docs, len(sample_data['response']['docs']) if total_docs > 0 else 0
            )
            return True
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"{Colors.RED}Collection '{collection_name}' not found{Colors.RESET}")
            else:
                print(f"{Colors.RED}HTTP error: {e}{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{Colors.RED}Error analyzing collection: {e}{Colors.RESET}")
            return False
    
    def _display_summary(self, collection_name, total_docs, fields, dynamic_fields, field_usage, sample_docs, sample_count):
        """Display collection summary"""
        print(f"\n{Colors.BOLD}COLLECTION: {collection_name}{Colors.RESET}")
        print("=" * 60)
        
        # Document stats
        print(f"\nDocument Statistics:")
        print(f"  Total Documents: {total_docs:,}")
        if sample_count > 0:
            print(f"  Sample Size: {sample_count} documents analyzed")
        
        # Schema info
        print(f"\nSchema Overview:")
        print(f"  Defined Fields: {len(fields)}")
        print(f"  Dynamic Fields: {len(dynamic_fields)}")
        
        # Field usage
        if field_usage:
            print(f"\nActive Fields (Top 10):")
            sorted_usage = sorted(field_usage.items(), key=lambda x: x[1], reverse=True)[:10]
            for field_name, count in sorted_usage:
                percentage = (count / sample_count) * 100 if sample_count > 0 else 0
                print(f"  {field_name:25} {percentage:5.1f}% ({count}/{sample_count})")
        
        # Dynamic field patterns
        print(f"\nDynamic Field Patterns:")
        
        patterns = [
            ('*_t', 'Text fields'),
            ('*_s', 'String fields'),
            ('*_d', 'Double fields'),
            ('*_i', 'Integer fields'),
            ('*_dt', 'Date fields'),
            ('*_b', 'Boolean fields'),
        ]
        
        found_patterns = []
        for pattern, description in patterns:
            for dfield in dynamic_fields:
                if dfield['name'] == pattern:
                    found_patterns.append((pattern, description, dfield))
                    break
        
        if found_patterns:
            for pattern, description, field_info in found_patterns:
                stored = "Yes" if field_info.get('stored', False) else "No"
                indexed = "Yes" if field_info.get('indexed', False) else "No"
                print(f"  {pattern:10} - {description:20} (Indexed: {indexed}, Stored: {stored})")
        
        # Sample documents
        if sample_docs:
            print(f"\nSample Documents:")
            
            for i, doc in enumerate(sample_docs, 1):
                print(f"\n  Document {i}:")
                for key, value in doc.items():
                    if key not in ['_version_', '_root_']:
                        # Truncate long values
                        if isinstance(value, str) and len(value) > 60:
                            display_value = value[:57] + "..."
                        else:
                            display_value = value
                        
                        print(f"    {key:18} {display_value}")
        
        print()

def main():
    """Main entry point"""
    # Clear screen
    print("\033[2J\033[H")
    
    # Display logo with animation
    print_solr_logo()
    print()
    print_logo()
    
    # Show loading animation
    animate_loading()
    
    # Print welcome message
    print(f"\n{Colors.CYAN}{'═' * 72}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}  Welcome to Apache Solr - Your Search and AI Assistant{Colors.RESET}")
    print(f"{Colors.CYAN}{'═' * 72}{Colors.RESET}")
    print(f"\n{Colors.GREEN}Ready to help with your Solr development tasks!{Colors.RESET}")
    print(f"{Colors.YELLOW}Type 'help' for available commands{Colors.RESET}")
    print(f"{Colors.BLUE}Happy searching and indexing!{Colors.RESET}\n")
    
    # Initialize connection
    solr = SolrConnection()
    
    # Prompt for connection
    print(f"{Colors.CYAN}Let's connect to your Apache Solr instance!{Colors.RESET}")
    print(f"{Colors.WHITE}Please enter your Solr URL (e.g., http://127.0.0.1:8983 or just 127.0.0.1:8983):{Colors.RESET}")
    
    while True:
        try:
            solr_url = input(f"{Colors.ORANGE}Solr URL{Colors.RESET} {Colors.GREEN}>{Colors.RESET} ").strip()
            
            if not solr_url:
                print(f"{Colors.YELLOW}Please enter a Solr URL to continue, or type 'skip' to continue without connection.{Colors.RESET}")
                continue
            elif solr_url.lower() == 'skip':
                print(f"{Colors.YELLOW}Skipping Solr connection. You can connect later using the 'connect' command.{Colors.RESET}\n")
                break
            else:
                if solr.connect(solr_url):
                    break
                else:
                    print(f"{Colors.YELLOW}Would you like to try a different URL? Or type 'skip' to continue without connection.{Colors.RESET}")
                    
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Skipping connection...{Colors.RESET}\n")
            break
    
    # Main loop
    while True:
        try:
            status_indicator = "+" if solr.connected else "-"
            user_input = input(f"{Colors.ORANGE}solr-assistant{Colors.RESET} {status_indicator} {Colors.GREEN}>{Colors.RESET} ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                if solr.connected:
                    solr.disconnect()
                print(f"\n{Colors.YELLOW}Goodbye! Thanks for using Solr Assistant!{Colors.RESET}")
                break
            elif user_input.lower() == 'help':
                print(f"\n{Colors.CYAN}Available Commands:{Colors.RESET}")
                print(f"  {Colors.GREEN}help{Colors.RESET}             - Show this help message")
                print(f"  {Colors.GREEN}connect{Colors.RESET}          - Connect to a Solr instance")
                print(f"  {Colors.GREEN}disconnect{Colors.RESET}       - Disconnect from current Solr instance")
                print(f"  {Colors.GREEN}status{Colors.RESET}           - Show connection status")
                print(f"  {Colors.GREEN}info{Colors.RESET}             - Show detailed Solr information")
                print(f"  {Colors.GREEN}collections{Colors.RESET}      - Show all collections/cores")
                print(f"  {Colors.GREEN}summarize{Colors.RESET}        - Analyze and summarize a collection")
                print(f"  {Colors.GREEN}clear{Colors.RESET}            - Clear the screen")
                print(f"  {Colors.GREEN}exit{Colors.RESET}             - Exit Solr Assistant")
                print(f"\n{Colors.YELLOW}More Solr features coming soon!{Colors.RESET}\n")
            elif user_input.lower() == 'clear':
                print("\033[2J\033[H")
                print_solr_logo()
                print()
                print_logo()
                print(f"\n{Colors.CYAN}{'═' * 72}{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.WHITE}  Welcome to Apache Solr - Your Search and AI Assistant{Colors.RESET}")
                print(f"{Colors.CYAN}{'═' * 72}{Colors.RESET}\n")
            elif user_input.lower() == 'connect':
                solr_url = input("Enter Solr URL: ").strip()
                if solr_url:
                    solr.connect(solr_url)
                else:
                    print("Invalid URL")
            elif user_input.lower() == 'disconnect':
                if solr.connected:
                    solr.disconnect()
                else:
                    print("Not connected")
            elif user_input.lower() == 'status':
                print(f"Status: {solr.get_status()}\n")
            elif user_input.lower() == 'info':
                if solr.connected:
                    solr._display_info()
                else:
                    print("Not connected. Use 'connect' command first.")
            elif user_input.lower() == 'collections':
                solr.list_collections()
            elif user_input.lower().startswith('summarize'):
                parts = user_input.split()
                if len(parts) == 1:
                    collection_name = input("Enter collection name: ").strip()
                    if collection_name:
                        solr.summarize_collection(collection_name)
                    else:
                        print("Invalid collection name")
                elif len(parts) == 2:
                    collection_name = parts[1]
                    solr.summarize_collection(collection_name)
                else:
                    print("Usage: summarize [collection_name]")
            elif user_input:
                print(f"Unknown command: {user_input}")
                
        except KeyboardInterrupt:
            print("\nGoodbye")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()