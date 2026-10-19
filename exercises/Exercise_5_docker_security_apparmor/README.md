# Exercise 5: Docker Security with AppArmor and Python

## Objective

Secure a Flask application in Docker using AppArmor, apply the profile through the Docker SDK for Python, and test restricted actions.

## Files

- `app.py`: Flask application listening on port 5000.
- `Dockerfile`: Builds the `flask-apparmor` image.
- `my-apparmor-profile`: AppArmor policy for the container.
- `apply_apparmor.py`: Builds, starts, and inspects the secured container.
- `test_restricted_actions.py`: Tests restricted file access and Bash execution.
- `requirements.txt`: Docker SDK dependency.

## Environment

This exercise was tested in Ubuntu WSL using a separate Docker Engine at `/run/docker-apparmor.sock`. The AppArmor profile must be loaded into the Linux kernel before starting the container.

Run the commands in this section in **Ubuntu**, not Windows PowerShell.

## Load the AppArmor profile

```bash
cd /mnt/c/Users/Ansh/Desktop/devops-lab-portfolio/exercises/05-docker-security-apparmor

sudo mount -t securityfs securityfs /sys/kernel/security
sudo cp my-apparmor-profile /etc/apparmor.d/my-apparmor-profile
sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
sudo aa-status
```

The profile should appear in enforce mode.

## Start the dedicated Docker Engine

If the AppArmor Docker daemon is not already running, start it in Ubuntu:

```bash
sudo service containerd start

sudo dockerd \
  -H unix:///run/docker-apparmor.sock \
  --containerd=/run/containerd/containerd.sock \
  --data-root=/var/lib/docker-apparmor \
  --exec-root=/run/docker-apparmor \
  --pidfile=/run/docker-apparmor.pid \
  > /tmp/dockerd-apparmor.log 2>&1 &
```

Select this daemon in the current Ubuntu terminal:

```bash
export DOCKER_HOST=unix:///run/docker-apparmor.sock
docker info --format '{{json .SecurityOptions}}'
```

The security options should include `name=apparmor`.

## Build and run Flask

```bash
docker build -t flask-apparmor .

docker run --rm \
  --security-opt="apparmor=my-apparmor-profile" \
  -p 5000:5000 flask-apparmor
```

The home route returns:

`Hello, this is a secure Flask application running inside a Docker container!`

Press Ctrl+C to stop the foreground container.

## Run the Docker SDK scripts

```bash
export DOCKER_HOST=unix:///run/docker-apparmor.sock

python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

.venv/bin/python apply_apparmor.py
.venv/bin/python test_restricted_actions.py
```

The SDK script verifies the configured security option and active AppArmor profile. The restricted-action tests run inside the confined Python process.

## Test results

The tests confirmed:

- The active process label is `my-apparmor-profile (enforce)`.
- Reading `/etc/passwd` is denied.
- Executing `/usr/bin/bash` from the confined Python process is denied by AppArmor.

## Questions and Answers

### 1. What is the purpose of using AppArmor with Docker containers?

AppArmor confines applications to permitted resources and actions, adding a layer of security around a container.

### 2. How do AppArmor profiles help secure a Docker container?

Profiles define permitted and denied file access, execution, network actions, and capabilities.

### 3. Why restrict sensitive directories such as `/etc/` and `/var/`?

`/etc/` contains configuration files, while `/var/` can contain logs and other changing system data. Restricting access reduces unauthorized access and modification.

### 4. What other capabilities can you restrict using AppArmor profiles?

Profiles can restrict network access, port binding, file execution, writes to selected directories, and sensitive capabilities such as `sys_admin`.

### 5. How can you verify whether an AppArmor profile is applied to a Docker container?

Use `sudo aa-status`, inspect the process security label, and inspect the container's Docker settings. `HostConfig.SecurityOpt` shows the configured AppArmor option; the active process label confirms enforcement.