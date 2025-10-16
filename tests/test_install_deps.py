import pytest
import docker
import os
import tarfile
import io
    
    
IMAGE = "ubuntu:24.04"  # Use LTS version that supports AMD64

@pytest.fixture(scope="function")
def docker_container():
    """Start a disposable Ubuntu container for testing."""
    client = docker.from_env()
    container = client.containers.run(
        IMAGE,
        command="/bin/bash",
        tty=True,
        detach=True,
        platform="linux/amd64",  # Force AMD64 platform for Millistream package compatibility
    )
    yield container
    container.stop()
    container.remove()

def exec_in_container(container, cmd):
    """Execute a command in the container and return output."""
    # Wrap the command in sh -c to get shell features like &&, |, quotes
    exec_log = container.exec_run(
        ["sh", "-c", cmd],
        environment={"PATH": "/root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"}
    )
    output = exec_log.output.decode()
    if exec_log.exit_code != 0:
        raise RuntimeError(f"Command failed: {cmd}\n{output}")
    return output

def exec_in_container_lenient(container, cmd):
    """Execute a command in the container and return output, without failing on non-zero exit code."""
    # Wrap the command in sh -c to get shell features like &&, |, quotes
    exec_log = container.exec_run(
        ["sh", "-c", cmd],
        environment={"PATH": "/root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"}
    )
    output = exec_log.output.decode()
    return output, exec_log.exit_code

def test_millistream_mdf_install(docker_container):
    container = docker_container

    # 1. Install bash, Python, venv, pip, curl
    exec_in_container(
        container,
        "apt-get update && apt-get install -y bash python3 python3-venv python3-pip curl"
    )

    # 2. Install uv using bash explicitly
    exec_in_container(container, "curl -LsSf https://astral.sh/uv/install.sh | bash")

    # 3. Create virtual environment
    exec_in_container(container, "python3 -m venv /tmp/venv")

    # 4. Copy local source files to container
    # Create a tar archive in memory
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode='w') as tar:
        # Add the src directory
        src_path = os.path.join(os.path.dirname(__file__), "..", "src")
        tar.add(src_path, arcname="millistream_mdf")
        
        # Add pyproject.toml
        pyproject_src = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")
        tar.add(pyproject_src, arcname="pyproject.toml")
    
    # Reset buffer position
    tar_buffer.seek(0)
    
    # Copy the tar archive to container
    container.put_archive("/tmp", tar_buffer.getvalue())
    
    # Files are automatically extracted by put_archive, no need to extract manually
    # Move pyproject.toml into the millistream_mdf directory
    exec_in_container(container, "mv /tmp/pyproject.toml /tmp/millistream_mdf/")

    # 5. Install millistream-mdf from local source in venv
    exec_in_container(container, "cd /tmp/millistream_mdf && /tmp/venv/bin/pip install -e .")

    # 6. Run MDF installer (don't fail if it returns non-zero exit code)
    output, exit_code = exec_in_container_lenient(
        container,
        "uv run /tmp/venv/bin/python -m millistream_mdf --install-deps"
    )
    print(f"Install output:\n{output}")
    print(f"Exit code: {exit_code}")

    # 7. Test import MDF
    output = exec_in_container(
        container,
        "/tmp/venv/bin/python -c \"from millistream_mdf import MDF; print('345842f0-69a7-4d47-a3c2-d4fcdad95533')\""
    )
    print(f"Import test output: {output}")
    assert "345842f0-69a7-4d47-a3c2-d4fcdad95533" in output