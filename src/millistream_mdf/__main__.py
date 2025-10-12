"""
Main entry point for millistream_mdf package.

Usage:
    python -m millistream_mdf --install-deps
"""

import sys


def main() -> None:
    """Display usage information."""
    if '--install-deps' in sys.argv:
        # The --install-deps flag is handled by _libmdf.py during import
        # Just display a success message if we got here
        print("\n✓ millistream-mdf is ready to use!")
    else:
        print("millistream-mdf: Python wrapper for libmdf C SDK")
        print()
        print("To install the libmdf dependency, run:")
        print("  python -m millistream_mdf --install-deps")
        print()
        print("Usage example:")
        print("  from millistream_mdf import MDF")
        print()
        print("  with MDF(url='server:port', username='user', password='pass') as session:")
        print("      for message in session.subscribe(message_classes=['quote'], insrefs='*'):")
        print("          print(message)")
        print()
        print("Documentation: https://packages.millistream.com/documents/")


if __name__ == "__main__":
    main()

