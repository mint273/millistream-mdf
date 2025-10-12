"""
Dependency installer for millistream-mdf.

This module can be run independently as a console script.
Usage: millistream-install-deps
"""

import os
import subprocess
import sys

from rich.console import Console
from rich.panel import Panel

console = Console()


def _needs_sudo() -> bool:
    """Check if we need to use sudo (not running as root)."""
    return os.geteuid() != 0


def install_linux() -> None:
    """Install libmdf for Linux"""
    console.print(Panel(
        f"Installing libmdf for [bold]Linux[/bold]...\n\n"
        f"This will automatically install the necessary dependency 'libmdf' using apt package manager."
    ))
    
    # Determine if we need sudo
    use_sudo = _needs_sudo()
    sudo_prefix = ["sudo"] if use_sudo else []
    
    try:
        # Step 1: Update package list and install prerequisites
        console.print("[bold]Step 1:[/bold] Updating package list and installing prerequisites...")
        subprocess.run([*sudo_prefix, "apt", "update"], check=True)
        subprocess.run([*sudo_prefix, "apt", "install", "-y", "lsb-release", "wget", "gpg"], check=True)
        
        # Step 2: Add Millistream repository
        console.print("[bold]Step 2:[/bold] Adding Millistream repository...")
        
        # Get the distribution codename
        result = subprocess.run(["lsb_release", "-cs"], capture_output=True, text=True, check=True)
        codename = result.stdout.strip()
        
        # Download and add the repository
        repo_url = f"https://packages.millistream.com/apt/sources.list.d/{codename}.list"
        subprocess.run([*sudo_prefix, "wget", repo_url, "-O", "/etc/apt/sources.list.d/millistream.list"], check=True)
        
        # Add the GPG key
        console.print("[bold]Step 3:[/bold] Adding GPG key...")
        gpg_cmd = 'wget -O- "https://packages.millistream.com/D2FCCE35.gpg" | gpg --dearmor | tee /usr/share/keyrings/millistream-archive-keyring.gpg > /dev/null'
        if use_sudo:
            gpg_cmd = f'sudo sh -c \'{gpg_cmd}\''
        subprocess.run(gpg_cmd, shell=True, check=True)
        
        # Step 4: Install libmdf
        console.print("[bold]Step 4:[/bold] Installing libmdf...")
        subprocess.run([*sudo_prefix, "apt", "update"], check=True)
        subprocess.run([*sudo_prefix, "apt", "install", "-y", "libmdf"], check=True)
        
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


def main() -> None:
    """Install dependencies for the current platform"""
    console.print("[bold]Millistream MDF Dependency Installer[/bold]\n")
    
    if sys.platform == 'linux':
        install_linux()
    elif sys.platform == 'darwin':
        install_macos()
    elif sys.platform == 'win32':
        install_windows()
    else:
        console.print(Panel(
            f"[bold yellow]⚠️  Unknown platform: {sys.platform}[/bold yellow]\n\n"
            f"Please visit [blue link=https://packages.millistream.com/]https://packages.millistream.com/[/blue link] for installation instructions."
        ))


if __name__ == "__main__":
    main()

