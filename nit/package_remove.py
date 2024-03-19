import os
import subprocess

def remove_package(service_name):
    pkgs_nix_path = "/etc/nixos/pkgs.nix"
    service_nix_path = f"/etc/nixos/pkgs/{service_name}.nix"

    with open(pkgs_nix_path, 'r') as pkgs_nix_file:
        lines = pkgs_nix_file.readlines()

    updated_lines = []
    found_entry = False
    for line in lines:
        if f"./pkgs/{service_name}.nix" not in line:
            updated_lines.append(line)
        else:
            found_entry = True

    if not found_entry:
        print(f"Entry for {service_name} not found in {pkgs_nix_path}.")
        return

    with open(pkgs_nix_path, 'w') as pkgs_nix_file:
        pkgs_nix_file.write(''.join(updated_lines))

    if os.path.exists(service_nix_path):
        os.remove(service_nix_path)
        print(f"Removed {service_nix_path}.")

    response = input("Entry removed. Would you like to rebuild and switch? y/n: ").strip().lower()
    if response == 'y':
        try:
            print("Executing sudo nixos-rebuild switch...")
            subprocess.run(["sudo", "nixos-rebuild", "switch"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during rebuild: {e}")
    else:
        print("Package removed. Run 'sudo nixos-rebuild switch' to apply changes.")