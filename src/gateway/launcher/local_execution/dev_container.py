import json
import subprocess
from pathlib import Path
from protos import celaut_pb2 as celaut
from src.gateway.launcher.local_execution.set_config import set_config
from src.utils.env import DEFAULT_SYSTEM_RESOURCES

def create_dev_container(
    service_path: str
) -> str:
    """
    Build and run a Docker container with volume mounting based on pre-compile.json configuration.
    
    Args:
        service_path (str): Path to the service directory containing Dockerfile and pre-compile.json
        config (Optional[gateway_pb2.Configuration]): Configuration for the container
        resources (gateway_pb2.CombinationResources.Clause): Resource requirements
        
    Returns:
        str: The container ID of the running container
        
    Raises:
        FileNotFoundError: If required configuration files are missing
        ValueError: If workdir is not specified in configuration
        subprocess.CalledProcessError: If Docker operations fail
    """
    # Normalize and validate paths
    service_dir = Path(service_path).resolve()
    config_path = service_dir / '.service' / 'pre-compile.json'
    dockerfile_path = service_dir / '.service' / 'Dockerfile'
    
    # Validate required files exist
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    if not dockerfile_path.exists():
        raise FileNotFoundError(f"Dockerfile not found: {dockerfile_path}")
    
    # Load configuration
    with open(config_path, 'r') as file:
        pre_compile = json.load(file)
    
    # Extract workdir from config
    container_workdir = pre_compile.get('workdir')
    if not container_workdir:
        raise ValueError("Workdir not specified in pre-compile.json")
    
    if service_dir.name != container_workdir:
        raise ValueError("In order to use this command, the workdir on .service/pre-comile.json must be equal to the repo folder name. You should rename it.")
    
    # Generate container name from directory
    container_name = f"{service_dir.name}-container"
    
    try:
        # Copy the .service/Dockerfile into the root project folder.
        subprocess.run([
            "cp",
            dockerfile_path,
            service_path
        ], check=True)

        # Check if the Docker image with the specified tag exists
        print(f"Checking if Docker image '{container_name}' exists...")
        existing_images = subprocess.run(
            ["docker", "images", "-q", container_name],
            capture_output=True, text=True
        )

        # If the image exists, proceed to remove containers using it and then delete the image
        if existing_images.stdout.strip():
            print(f"Docker image '{container_name}' exists. Proceeding with cleanup...")

            # Find and stop/remove any containers using this image
            print(f"Finding containers using image '{container_name}'...")
            containers = subprocess.run(
                ["docker", "ps", "-a", "-q", "--filter", f"ancestor={container_name}"],
                capture_output=True, text=True
            )

            if containers.stdout.strip():
                print(f"Stopping and removing containers using image '{container_name}'...")
                container_ids = containers.stdout.strip().splitlines()
                for container_id in container_ids:
                    subprocess.run(["docker", "stop", container_id], check=True)
                    subprocess.run(["docker", "rm", container_id], check=True)
            else:
                print(f"No containers found using image '{container_name}'.")

            # Remove the image
            print(f"Removing existing Docker image '{container_name}'...")
            subprocess.run(["docker", "rmi", "-f", container_name], check=True)
        else:
            print(f"No existing image found for '{container_name}', no cleanup needed.")

        # Build the Docker image
        print("Building Docker image...")
        subprocess.run([
            "docker", "build",
            "-t", container_name,
            str(service_dir)              # This will include all the repository into the container, without keep in mind the include list from pre-compile.json
        ], check=True)

        # Deletes the auxiliar dockerfile
        subprocess.run([
            "rm",
            service_dir / "Dockerfile"
        ], check=True)
        
        # Run the container with volume mount in detached mode        
        print("Running container...")
        result = subprocess.run(
            [
                "docker", "run",
                "-d",  # Run in detached mode to get container ID
                "--rm",  # Remove container after exit
                #  "-v", f"{service_dir}:{container_workdir}",   # For now, better to rebuild because most of the entrypoint process doesn't have hot reload.
                container_name
            ],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Get container ID from output
        container_id = result.stdout.strip()
        
        if not container_id:
            raise ValueError("Failed to get container ID from docker run command")
            
        # Set configuration with container ID
        set_config(
            container_id=container_id,
            config=None,
            resources=DEFAULT_SYSTEM_RESOURCES,
            api=celaut.Service.Container.Config(path=[])
        )
        
        print(f"Container started successfully with ID: {container_id}")
        return container_id
        
    except subprocess.CalledProcessError as e:
        print(f"Error during Docker operation: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise