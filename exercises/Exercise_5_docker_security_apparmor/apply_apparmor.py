import docker
from docker.errors import NotFound

client = docker.from_env()
container = None

try:
    print("Building image from Dockerfile...")
    client.images.build(path=".", tag="flask-apparmor")

    try:
        client.containers.get("flask-apparmor-sdk").remove(force=True)
    except NotFound:
        pass

    print("Running container with AppArmor profile...")
    container = client.containers.run(
        "flask-apparmor",
        name="flask-apparmor-sdk",
        ports={"5000/tcp": 5000},
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True,
    )

    info = client.api.inspect_container(container.id)
    print(f"Container started: {container.short_id}")
    print(f"Security options: {info['HostConfig']['SecurityOpt']}")
    print(f"Active AppArmor profile: {info.get('AppArmorProfile')}")

finally:
    if container:
        container.stop()
        container.remove()
        print("Container stopped and removed.")
