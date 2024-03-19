import subprocess
import shlex

class SearchResult:
    def __init__(self, user_input):
        self.user_input = user_input
        self.package_name = shlex.quote(self.user_input)
        self.results = []

    def run_command(self, command):
        try:
            process = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
            output = process.stdout
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
            return []
        
        return output.strip().split('\n')
    
    def search_nix(self):
        command = f"nix-env -qaP {self.package_name} 2>/dev/null | sed 's/^nixos\.//' | cut -d' ' -f1"
        self.results = self.run_command(command)
    
    def get_results(self):
        self.search_nix()
        return self.results