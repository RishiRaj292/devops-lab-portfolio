# Exercise 7 — Introduction to Continuous Integration and Jenkins

The ZIP's goal is to introduce CI and run Jenkins using Docker. To make Exercises 6 and 9 runnable without installing tools manually in every job, this lab uses a Jenkins image that includes Python 3, Docker CLI, and `docker-compose`.

## Build the reusable Jenkins image

Run from the repository root in PowerShell:

```powershell
docker build -t devops-jenkins:local -f exercises/07-jenkins-ci-automation/Dockerfile.jenkins .
```

Start Jenkins with persistent state and Docker socket access (local learning environment only):

```powershell
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock --group-add 0 devops-jenkins:local
```

Open http://localhost:8080. Get the initial password with:

```powershell
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Complete the setup wizard and install the suggested plugins, including Pipeline and Git. Preserve the `jenkins_home` volume so subsequent exercises reuse the same Jenkins instance.

## CI concepts from the manual

A basic CI workflow is: code change → trigger build → run tests → provide feedback. Jenkins uses jobs, builds, pipelines, plugins, and nodes to automate these steps.

**Important:** mounting the Docker socket gives Jenkins control over the local Docker daemon. Use this setup only for this local lab machine.
