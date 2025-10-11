import argparse
import subprocess
import sys

from rich.console import Console
from rich.panel import Panel

from millistream_mdf import __version__

console = Console()




def install_linux() -> None:
    """Install libmdf for Linux"""
    console.print(Panel(
        f"Installing libmdf for [bold]Linux[/bold]...\n\n"
        f"This will automatically install the necessary dependency 'libmdf' using apt package manager."
    ))
    
    try:
        # Step 1: Update package list and install prerequisites
        console.print("[bold]Step 1:[/bold] Updating package list and installing prerequisites...")
        subprocess.run(["apt", "update"], check=True)
        subprocess.run(["apt", "install", "-y", "lsb-release", "wget", "gpg"], check=True)
        
        # Step 2: Add Millistream repository
        console.print("[bold]Step 2:[/bold] Adding Millistream repository...")
        
        # Get the distribution codename
        result = subprocess.run(["lsb_release", "-cs"], capture_output=True, text=True, check=True)
        codename = result.stdout.strip()
        
        # Download and add the repository
        repo_url = f"https://packages.millistream.com/apt/sources.list.d/{codename}.list"
        subprocess.run(["wget", repo_url, "-O", "/etc/apt/sources.list.d/millistream.list"], check=True)
        
        # Add the GPG key
        console.print("[bold]Step 3b:[/bold] Adding GPG key...")
        subprocess.run(
            'wget -O- "https://packages.millistream.com/D2FCCE35.gpg" | gpg --dearmor | tee /usr/share/keyrings/millistream-archive-keyring.gpg > /dev/null',
            shell=True,
            check=True
        )
        
        # Step 3: Install libmdf
        console.print("[bold]Step 4:[/bold] Installing libmdf...")
        subprocess.run(["apt", "update"], check=True)
        subprocess.run(["apt", "install", "-y", "libmdf"], check=True)
        
        console.print(Panel(
            f"[bold green]✅ Installation completed successfully![/bold green]\n\n"
            f"libmdf has been installed and is ready to use.\n\n"
            f"For more information, visit: [blue link=https://github.com/mint273/millistream-mdf]https://github.com/mint273/millistream-mdf[/blue link]"
        ))
        
    except subprocess.CalledProcessError as e:
        console.print(Panel(
            f"[bold red]❌ Installation failed![/bold red]\n\n"
            f"Error: {e}\n\n"
            f"Please try running the installation manually or check your system permissions.\n\n"
            f"For manual installation instructions, visit: [blue link=https://github.com/mint273/millistream-mdf]https://github.com/mint273/millistream-mdf[/blue link]"
        ))
        sys.exit(1)
    except FileNotFoundError:
        console.print(Panel(
            f"[bold red]❌ Installation failed![/bold red]\n\n"
            f"Required system tools not found. Please ensure you have 'sudo', 'apt', 'wget', and 'gpg' installed.\n\n"
            f"For manual installation instructions, visit: [blue link=https://github.com/mint273/millistream-mdf]https://github.com/mint273/millistream-mdf[/blue link]"
        ))
        sys.exit(1)

    

def install_macos() -> None:
    """Install libmdf for macOS"""
    console.print(Panel(
        f"Installation notice for [bold]macOS[/bold]:\n\n"
        f"For [bold]macOS[/bold], it's recommended to install the necessary dependency 'libmdf' using the [bold].pkg[/bold] installer from [blue link=https://packages.millistream.com/macOS/]https://packages.millistream.com/macOS/[/blue link]\n\n"
        f"Download and run the latest installer and follow the on-screen instructions. After that, you're done!\n\n"
        f"For more information, visit: [blue link=https://github.com/mint273/millistream-mdf]https://github.com/mint273/millistream-mdf[/blue link]"
    ))


def install_windows() -> None:
    """Install libmdf for Windows"""
    console.print(Panel(
        f"Installation notice for [bold]Windows[/bold]:\n\n"
        f"For [bold]Windows[/bold], it's recommended to install the necessary dependency 'libmdf' using the [bold].exe[/bold] installer from [blue link=https://packages.millistream.com/Windows/]https://packages.millistream.com/Windows/[/blue link]\n\n"
        f"Download and run the latest installer and follow the on-screen instructions. After that, you're done!\n\n"
        f"For more information, visit: [blue link=https://github.com/mint273/millistream-mdf]https://github.com/mint273/millistream-mdf[/blue link]"
    ))





def install_deps() -> None:
    """Install dependencies for the current platform"""
    if sys.platform == 'linux':
        install_linux()
    elif sys.platform == 'darwin':
        install_macos()
    elif sys.platform == 'win32':
        install_windows()

def print_version() -> None:
    """Print the version of the package"""
    print(f'Version: {__version__}')



def main() -> None:
    parser = argparse.ArgumentParser(description='Millistream MDF')
    parser.add_argument('--install-deps', action='store_true', help='Install dependencies')
    parser.add_argument('--version', action='store_true', help='Show version')
    args = parser.parse_args()

    if args.install_deps:
        install_deps()
    elif args.version:
        print_version()






if __name__ == "__main__":
    main()