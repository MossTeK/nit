import argparse
from .package_install import NixPackageHelper
from .package_remove import remove_package
from .package_search import SearchResult

class Nit:
    def __init__(self, args):
        self.args = args
        self.action_map = {
            'install': lambda: self.handle_install(self.args.service, install=True) if getattr(args, 'install', None) is not None else None,
            'remove': lambda: self.handle_remove(self.args.remove[0]) if getattr(args, 'remove', None) is not None and len(self.args.remove) > 0 else None,
            'service': lambda: self.handle_install(self.args.service) if getattr(args, 'service', None) is not None else None,
        }

        for action, func in self.action_map.items():
            if getattr(args, action, None):
                action_func = func()
                if action_func is not None:
                    action_func()
                break

    def handle_install(self, service_name, install=False):
        print(f"Searching for Nix packages: {service_name}")
        search_result = SearchResult(service_name)
        search_result.search_nix()
        nix_packages = search_result.get_results()

        if install:
            self.display_and_install(nix_packages)
        else:
            self.display_packages(nix_packages)

    def handle_remove(self, package_name):
        print(f"Removing package: {package_name}")
        try:
            remove_package(package_name)
        except Exception as e:
            print(f"Failed to remove package {package_name}: {e}")

    def display_and_install(self, packages):
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

    def display_packages(self, packages):
        for idx, package in enumerate(packages):
            print(f"{idx}: {package}")

def main():
    parser = argparse.ArgumentParser(description="Manage Nix packages on Nixos.")
    parser.add_argument('-r', '--remove', help='Remove a package by name', nargs=1)
    parser.add_argument('-i', '--install', help='Install a package', action='store_true')
    parser.add_argument('-c', '--custom', help='Add a custom Nix package via a URL to a git repository')
    parser.add_argument('service', help='Name of the service or package', nargs='?')
    
    Nit(parser.parse_args())

if __name__ == "__main__":
    main()