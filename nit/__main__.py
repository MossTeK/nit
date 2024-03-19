import argparse
from .package_install import NixPackageHelper
from .package_remove import remove_package
from .package_search import SearchResult

def main():
    """
    A simple command line utility for managing Nix packages on Nixos.
    """
    parser = argparse.ArgumentParser(description="Manage Nix packages on Nixos.")
    parser.add_argument('-r', '--remove', help='Remove a package by name', nargs=1)
    parser.add_argument('-i', '--install', help='Install a package', action='store_true')
    parser.add_argument('-c', '--custom', help='Add a custom Nix package via a URL to a git repository')
    parser.add_argument('service', help='Name of the service or package', nargs='?')

    args = parser.parse_args()

    if args.remove and args.service:
        handle_remove(args.service)
    elif args.install and args.service:
        handle_search(args.service, install=True)
    elif args.service:
        handle_search(args.service)
    else:
        parser.print_help()

def handle_search(service_name, install=False):
    """
    Handles searching and optionally installing a package.
    """
    print(f"Searching for Nix packages: {service_name}")
    # Assuming SearchResult has proper implementation
    search_result = SearchResult(service_name)
    search_result.search_nix()
    nix_packages = search_result.get_results()
    
    if install:
        display_and_install(nix_packages)
    else:
        display_packages(nix_packages)

def handle_remove(package_name):
    """
    Handles package removal.
    """
    print(f"Removing package: {package_name}")
    try:
        remove_package(package_name)
    except Exception as e:
        print(f"Failed to remove package {package_name}: {e}")

def display_and_install(packages):
    """
    Displays packages and prompts for selection to install.
    """
    if not packages:
        print("No packages found.")
        return
    
    for idx, package in enumerate(packages):
        print(f"{idx}: {package}")

    while True:
        choice = input("Enter the number of the package to install (or 'exit' to cancel): ")
        if choice.lower() == 'exit':
            print("Installation canceled.")
            return
        try:
            choice_idx = int(choice)
            if 0 <= choice_idx < len(packages):
                package_name = packages[choice_idx]
                package_helper = NixPackageHelper(package_name)
                package_helper.write_template()
                break
            else:
                print("Invalid selection. Please try again, or type 'exit' to cancel.")
        except ValueError:
            print("Invalid input. Please enter a number, or type 'exit' to cancel.")

def display_packages(packages):
    """
    Displays a list of packages.
    """
    for idx, package in enumerate(packages):
        print(f"{idx}: {package}")

if __name__ == "__main__":
    main()