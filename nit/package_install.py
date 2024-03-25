import os
import subprocess
import requests

class NixPackageHelper:
    def __init__(self, service_name):
        self.service_name = service_name
        self.pkgs_nix_path = "/etc/nixos/pkgs.nix"
        self.template_url = "https://raw.githubusercontent.com/MossTeK/nit/dev/nix/template.nix"
        self.destination_path = f"/etc/nixos/pkgs/{os.path.basename(self.service_name)}.nix"
    
    def append_path(self):
        """
        Specifically targets and updates the imports array within pkgs.nix to include a new service path.
        """
        entry_to_add = f"    ./pkgs/{self.service_name}.nix"
        try:
            with open(self.pkgs_nix_path, 'r') as pkgs_nix_file:
                content = pkgs_nix_file.readlines()
        except IOError as e:
            print(f"Failed to read {self.pkgs_nix_path}: {e}")
            return
        
        if entry_to_add in content:
            print(f"Entry for '{self.service_name}.nix' already exists in {self.pkgs_nix_path}")
            return
        
        insertion_index = None
        end_index = None
        
        # Locate the imports array
        for i, line in enumerate(content):
            if "imports = [" in line:
                insertion_index = i + 1  # To insert after the opening of imports
            if insertion_index and "];" in line:
                end_index = i
                break

        if insertion_index is None or end_index is None:
            print("Could not find the correct position to insert the new entry.")
            return
        
        # Adjusting for a clean append
        if content[end_index - 1].strip() == "":
            content.insert(end_index, entry_to_add + "\n")
        else:
            content.insert(end_index, "\n" + entry_to_add + "\n")
            
        try:
            with open(self.pkgs_nix_path, 'w') as pkgs_nix_file:
                pkgs_nix_file.writelines(content)
            print(f"Successfully added '{self.service_name}.nix' to the imports in {self.pkgs_nix_path}.")
        except IOError as e:
            print(f"Failed to write to {self.pkgs_nix_path}: {e}")

    def download_template(self):
        """
        Downloads the nix template from a specified URL.
        """
        try:
            response = requests.get(self.template_url)
            response.raise_for_status()  # Check for HTTP errors
        except requests.RequestException as e:
            print(f"Failed to download template: {e}")
            return None

        return response.text

    def write_template(self):
        """
        Writes the downloaded template to the destination path.
        Replaces 'PLACEHOLDER' in the template with the actual service name.
        """
        if os.path.exists(self.destination_path):
            print(f"{self.destination_path} already exists.")
            return

        template_data = self.download_template()
        if template_data is None:
            return

        template_data = template_data.replace("PLACEHOLDER", self.service_name)

        try:
            with open(self.destination_path, "w") as destination_file:
                destination_file.write(template_data)
        except IOError as e:
            print(f"Failed to write template to {self.destination_path}: {e}")
            return

        print(f"Template written to {self.destination_path}")
        self.append_path()  # Updated method call

        # User prompt for nixos-rebuild
        response = input("Would you like to rebuild and switch? y/n: ").strip().lower()
        if response == 'y':
            try:
                print("Executing sudo nixos-rebuild switch...")
                subprocess.run(["sudo", "nixos-rebuild", "switch"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"An error occurred during rebuild: {e}")
        else:
            print("Template written, but package installation deferred until 'sudo nixos-rebuild switch' is performed.")