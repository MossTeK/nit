import os
import subprocess
import requests

class NixPackageHelper:
    def __init__(self, service_name):
        self.service_name = service_name
        self.pkgs_nix_path = "/etc/nixos/pkgs.nix"
        # Provide the full URL to the raw template.nix file in your repository
        self.template_url = "https://raw.githubusercontent.com/MossTeK/nit/main/nix/template.nix"
        self.destination_path = f"/etc/nixos/pkgs/{os.path.basename(self.service_name)}.nix"
    
    def append_to_pkgs_nix(self):
        """
        Updates pkgs.nix to include the new service.
        """
        entry_to_add = f"    ./pkgs/{self.service_name}.nix\n"
        try:
            with open(self.pkgs_nix_path, 'r') as pkgs_nix_file:
                lines = pkgs_nix_file.readlines()
        except IOError as e:
            print(f"Failed to read {self.pkgs_nix_path}: {e}")
            return

        if entry_to_add.strip() in (line.strip() for line in lines):
            print(f"Entry for {self.service_name} already exists in {self.pkgs_nix_path}.")
            return

        closing_bracket_index = None
        for i, line in enumerate(lines):
            if line.strip() == "]":
                closing_bracket_index = i
                break

        if closing_bracket_index is not None:
            lines.insert(closing_bracket_index, entry_to_add)
            try:
                with open(self.pkgs_nix_path, 'w') as pkgs_nix_file:
                    pkgs_nix_file.writelines(lines)
            except IOError as e:
                print(f"Failed to write to {self.pkgs_nix_path}: {e}")
                return
        else:
            print("Failed to find the closing bracket in pkgs.nix.")
            return
    
    def download_template(self):
        """
        Downloads the template from a given URL.
        """
        try:
            response = requests.get(self.template_url)
            response.raise_for_status()  # Raises an HTTPError if the response was an error
        except requests.RequestException as e:
            print(f"Failed to download template: {e}")
            return None
        return response.text

    def write_template(self):
        """
        Writes the service template to the destination path after downloading it.
        """
        if os.path.exists(self.destination_path):
            print(f"{self.destination_path} already exists.")
            return

        template_data = self.download_template()
        if template_data is None:
            return

        # Replace placeholder with the actual service name
        template_data = template_data.replace("PLACEHOLDER", self.service_name)

        try:
            with open(self.destination_path, "w") as destination_file:
                destination_file.write(template_data)
        except IOError as e:
            print(f"Failed to write template to {self.destination_path}: {e}")
            return

        print(f"Template written to {self.destination_path}")
        self.append_to_pkgs_nix()

        response = input("Would you like to rebuild and switch? y/n: ").strip().lower()
        if response == 'y':
            try:
                print("Executing sudo nixos-rebuild switch...")
                subprocess.run(["sudo", "nixos-rebuild", "switch"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"An error occurred during rebuild: {e}")
        else:
            print("Template written, but package installation deferred until 'sudo nixos-rebuild switch' is performed.")