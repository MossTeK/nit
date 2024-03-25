import os
import subprocess

def remove_package(service_name):
    pkgs_nix_path = "/etc/nixos/pkgs.nix"  # Make sure this is spelled correctly
    service_nix_path = f"/etc/nixos/pkgs/{service_name}.nix"
    
    try:
        # Read the pkgs.nix file to locate the entry for removal
        with open(pkgs_nix_path, 'r') as file:
            lines = file.readlines()
        
        with open(pkgs_nix_path, 'w') as file:  # Corrected the variable name here
            found_entry = False
            for line in lines:
                if f"./pkgs/{service_name}.nix" in line:
                    found_entry = True
                else:
                    file.write(line)
            
            if not found_entry:
                print(f"No entry for {service_name} in {pkgs_nix_path}.")
        
        # Remove the service-specific .nix file if it exists
        if os.path.exists(service_nix_path):
            os.remove(service_nix_path)
            print(f"File {service_nix_path} removed.")
        else:
            print(f"No file found at {service_nix_path}. Not removing.")
        
        # Ask for user confirmation for rebuild and switch operation
        if found_entry:
            response = input("Would you like to rebuild and switch the configuration now? (y/n): ").strip().lower()
            if response == 'y':
                # Using subprocess to call "sudo nixos-rebuild switch"
                subprocess.run(["sudo", "nixos-rebuild", "switch"], check=True)
                print("System rebuild and switch executed.")
            else:
                print("Rebuild and switch skipped. Manual rebuild required to apply changes.")
    except Exception as e:
        # Generic exception handling to catch any unexpected errors
        print(f"An error occurred: {e}")