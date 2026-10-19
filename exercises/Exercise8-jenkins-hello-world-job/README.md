# Exercise 8 — Hello World Jenkins Freestyle Job

The ZIP asks for a GitHub-backed Freestyle job that runs `hello-world.sh`. To save time and avoid creating a second GitHub repository, this version keeps the script in the existing `devops-lab-portfolio` repository.

1. Commit and push this folder to `main`.
2. In Jenkins (`http://localhost:8080`), select **New Item**, enter `HelloWorld`, select **Freestyle project**, then **OK**.
3. Under **Source Code Management**, select **Git** and set Repository URL to `https://github.com/LucianShinei/devops-lab-portfolio.git`.
4. Under **Build Steps**, choose **Execute shell** and enter:

   ```sh
   bash exercises/08-jenkins-hello-world-job/hello-world.sh
   ```

5. Save, click **Build Now**, then open **Console Output**. Expected line: `Hello, Jenkins!` and result `Finished: SUCCESS`.

This reuses the existing GitHub repo instead of creating a separate public `devops-sample-code` repo as the manual's example suggests.
