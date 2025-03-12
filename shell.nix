{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs.python312Packages; [
    pandas
    netcdf4
    xarray
  ];
}
