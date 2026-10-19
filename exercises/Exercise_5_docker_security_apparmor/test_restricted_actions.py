import docker

client = docker.from_env()
container = None

test_code = r"""
import subprocess

print("Active profile:", open("/proc/self/attr/current").read().strip())

try:
    with open("/etc/passwd") as f:
        f.read(1)
    print("FAIL: /etc/passwd was readable")
except PermissionError:
    print("PASS: reading /etc/passwd denied")

try:
    subprocess.run(
        ["/usr/bin/bash", "-c", "echo SHOULD_NOT_RUN"],
        check=True,
    )
    print("FAIL: Bash execution was allowed")
except PermissionError:
    print("PASS: Bash execution denied by AppArmor")
"""

try:
    container = client.containers.run(
        "flask-apparmor",
        entrypoint="/usr/local/bin/python",
        command=["-c", test_code],
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True,
    )

    result = container.wait(timeout=15)
    output = container.logs().decode(errors="replace")
    print(output)

    if result["StatusCode"] != 0 or "FAIL:" in output:
        raise SystemExit("Restricted-action test failed")

finally:
    if container:
        container.remove(force=True)
