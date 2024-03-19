# Nit: The Nix Install Tool

**Nit** is an innovative tool designed to seamlessly integrate Python and NixOS capabilities, enabling users to manage Nix packages with the ease of a Python-based command-line interface (CLI). It simplifies various tasks including installing, removing, and searching for packages on NixOS, offering a streamlined experience for both beginners and seasoned Nix users.

## Features

- **Ease of Use**: Simplify Nix package management with a user-friendly CLI.
- **Package Management**: Install, remove, and search for Nix packages directly from the command line.
- **Integration**: Works seamlessly with a local copy of the Nixpkgs repository, ensuring that packages are directly managed within NixOS.

## Getting Started

### Installation Steps

Follow these steps to install Nit on your system:

1. **Add `nit` to `configuration.nix`**
    ```nix
    environment.systemPackages = with pkgs; [
        nit
    ];
    ```

2. **Edit Your `configuration.nix`**

   Upate your configuration.nix

   ```nix
   {
     imports = [
       ./etc/nixos/pkgs.nix
     ];
   }
   ```

## Usage

When calling nit you pass two arguments, one specifying install or remove, and the other specifying the package name

#### Example:
  ```bash
  nit -i "package_name" # install a package given the name
  nit -r "package_name" # remove a package given the name 
  ```

### Installing a Package
To install a specific package:

nit -i <package_name>
Nit will search for the package, and upon finding it, will prompt for installation approval.

### Removing a Package
To remove a previously installed package:

nit -r <package_name>
This command updates pkgs.nix and removes the related service file from the system.