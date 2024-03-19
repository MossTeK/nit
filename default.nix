with import <nixpkgs> {};

pkgs.python3Packages.buildPythonPackage rec {
  pname = "nit";
  version = "v0.0.1";

  src = fetchgit {
    url = "https://github.com/MossTeK/nit.git";
    rev = "v0.0.1";
    sha256 = "04yyw9l2nbxma6wqfv73m22qa9ll3qwhkzb5hym3b0qagph98vjk";  
  };

  propagatedBuildInputs = with pkgs.python3Packages; [
    requests
    setuptools
    pip
  ];

  meta = with pkgs.lib; {
    description = "A simple command line utility for NixOS to make installing and removing packages easier";
    homepage = "https://github.com/MossTeK/nit";
    license = licenses.mit;
    maintainers = [ pkgs.lib.maintainers.MossTeK ];
  };
}

