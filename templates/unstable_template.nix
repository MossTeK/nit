{ config, pkgs, ... }:

let
  unstablePkgs = import <nixpkgs> {
    config = config.nixpkgs.config;
    overlays = [];
  };
in
{
  environment.systemPackages = with pkgs; [
    unstablePkgs.PLACEHOLDER
  ];
}