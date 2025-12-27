{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    (python3.withPackages (ps: with ps; [
      pillow
      python-dateutil
      exifread
    ]))
  ];

  shellHook = ''
    echo "Family Photo Organizer - Development Environment"
    echo "Python: $(python --version)"
    echo ""
    echo "Available commands:"
    echo "  python family_photo_organizer.py --help"
    echo ""
  '';
}
