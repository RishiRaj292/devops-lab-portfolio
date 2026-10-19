# Exercise 9 — Jenkins Multi-Stage Pipeline

Implements the ZIP's Build → Test → Deploy flow and its additional Run Application / Test Application stages.

1. Commit and push this folder to `main`.
2. In Jenkins, select **New Item** → `Python-MultiStage-Pipeline` → **Pipeline**.
3. In the job configuration, under **Pipeline**, choose **Pipeline script from SCM**, SCM **Git**, repository URL `https://github.com/LucianShinei/devops-lab-portfolio.git`, branch `*/main`, and **Script Path** `exercises/09-jenkins-multi-stage-pipeline/Jenkinsfile`.
4. Save and click **Build Now**. The pipeline installs the dependencies in a virtual environment, runs unit tests, copies the app into `python-app-deploy`, launches it briefly, then cleans up its process.

The Jenkins image from Exercise 7 includes Python 3 and `python3-venv`, which addresses the missing Python/pip/venv issue described in the source manual.
