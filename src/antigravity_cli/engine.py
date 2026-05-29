import sys
import yaml
import subprocess
import os

def execute_workflow(yaml_path):
    print(f"Loading workflow from {yaml_path}")
    with open(yaml_path, 'r') as f:
        workflow = yaml.safe_load(f)

    project_name = workflow.get("project", "default-project")
    tasks = workflow.get("tasks", [])

    if not tasks:
        print("No tasks found in workflow.")
        return

    work_dir = os.path.abspath(os.path.dirname(yaml_path))
    project_dir = os.path.abspath(os.path.join(work_dir, ".."))
    current_cwd = os.getcwd()

    print(f"Project: {project_name}")
    print("-" * 40)

    for step, task in enumerate(tasks):
        name = task.get("name", f"task-{step}")
        image = task.get("image")
        commands = task.get("commands", [])
        mounts = task.get("mounts", [])
        env = task.get("env", [])

        print(f"Running Task: {name}")

        cmd_args = ["docker", "run", "--rm"]
        
        # Envs
        for e in env:
            cmd_args.extend(["-e", e])
            
        # Mounts
        for mount in mounts:
            if ":" in mount:
                local_path, container_path = mount.split(":", 1)
                
                # Make local path absolute based on CWD
                if local_path.startswith("./") or local_path.startswith(".\\"):
                    # For windows absolute paths, docker handles C:\path well usually,
                    # but if we are passing it to Docker Desktop it should work.
                    absolute_local = os.path.abspath(os.path.join(current_cwd, local_path))
                    cmd_args.extend(["-v", f"{absolute_local}:{container_path}"])
                else:
                    cmd_args.extend(["-v", mount])

        # Add image
        cmd_args.append(image)

        # Commands
        if commands:
            shell_cmd = " && ".join(commands)
            # Use /bin/sh since most linux containers have it
            cmd_args.extend(["/bin/sh", "-c", shell_cmd])

        try:
            print(f"Waiting for execution in {image}...")
            subprocess.run(cmd_args, check=True)
            print(f"Task '{name}' completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Task '{name}' failed with code {e.returncode}")
            sys.exit(e.returncode)
            
        print("-" * 40)
