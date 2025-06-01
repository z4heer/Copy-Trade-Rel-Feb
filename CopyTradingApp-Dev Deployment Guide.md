\# Copy Trading App — Dev Deployment Guide (Windows, Jenkins)

This guide explains how to automate building and deploying the Copy Trading App for development using Jenkins on Windows.    
It covers continuous integration of the Angular frontend and Python backend, \*\*without PyInstaller\*\* (run with Python for easy debugging/iteration).

\---

\#\# 1\. Pre-requisites

\- \*\*Jenkins\*\* is installed and running as a Windows service or locally.  
\- The Jenkins agent/machine has:  
  \- Node.js and npm installed (\`node \-v\`, \`npm \-v\`)  
  \- Python 3.x installed (\`python \--version\`)  
  \- pip (\`pip \--version\`)  
  \- Angular CLI (\`npm install \-g @angular/cli\`)  
  \- Required Python dependencies (\`pip install \-r requirements.txt\`)  
  \- Git (to clone/pull your repo)  
\- Ensure Jenkins can access your repo (HTTPS URL or SSH keys configured).

\---

\#\# 2\. Example Jenkins Pipeline (Jenkinsfile)

Place this file in your repo root as \`Jenkinsfile\`:

\`\`\`groovy name=Jenkinsfile  
pipeline {  
    agent any

    environment {  
        FRONTEND\_DIR \= 'frontend\\\\copy-trading-v2-app'  
        BACKEND\_DIR  \= 'backend'  
        STATIC\_DIR   \= 'backend\\\\static'  
        CONF\_DIR     \= 'backend\\\\conf'  
    }

    stages {  
        stage('Checkout') {  
            steps {  
                checkout scm  
            }  
        }  
        stage('Install Frontend Dependencies') {  
            steps {  
                dir("${env.FRONTEND\_DIR}") {  
                    bat 'npm install'  
                }  
            }  
        }  
        stage('Build Angular Frontend') {  
            steps {  
                dir("${env.FRONTEND\_DIR}") {  
                    bat 'ng build'  
                }  
            }  
        }  
        stage('Copy Frontend Build to Backend') {  
            steps {  
                bat 'if not exist "%STATIC\_DIR%" mkdir "%STATIC\_DIR%"'  
                bat 'xcopy /E /I /Y "%FRONTEND\_DIR%\\\\dist\\\\copy-trading-v2-app\\\\browser\\\\\*" "%STATIC\_DIR%\\\\"'  
            }  
        }  
        stage('Install Backend Python Dependencies') {  
            steps {  
                dir("${env.BACKEND\_DIR}") {  
                    bat 'pip install \-r requirements.txt'  
                }  
            }  
        }  
        stage('Run Backend (Development Mode)') {  
            steps {  
                dir("${env.BACKEND\_DIR}") {  
                    bat 'python app.py'  
                }  
            }  
        }  
    }  
}  
\`\`\`

\---

\#\# 3\. Folder Structure

\`\`\`  
repo-root/  
├── Jenkinsfile  
├── frontend/  
│   └── copy-trading-v2-app/  
│       └── ... (Angular source)  
├── backend/  
│   ├── app.py  
│   ├── requirements.txt  
│   ├── static/  
│   └── conf/  
│       ├── users.xls  
│       └── settings.ini  
└── ...  
\`\`\`

\---

\#\# 4\. Jenkins Job Setup

1\. \*\*Create a new Pipeline job\*\* in Jenkins.  
2\. Point the job to your repository (where \`Jenkinsfile\` is located).  
3\. Configure credentials if needed.  
4\. Optionally set up build triggers (e.g., poll SCM or webhook).

\---

\#\# 5\. How It Works

\- Jenkins checks out the latest code.  
\- Installs frontend dependencies and builds the Angular app.  
\- Copies the built files to the backend's \`static\` folder.  
\- Installs backend Python dependencies.  
\- Runs the backend in dev mode (\`python app.py\`).  
    \- You can then access the running app at \[http://localhost:5000/\](http://localhost:5000/).

\---

\#\# 6\. Development/Debugging Tips

\- \*\*Hot reload:\*\* You can stop the Jenkins job, make code changes, and rerun the job for a fresh dev instance.  
\- \*\*No PyInstaller:\*\* In dev, run with \`python app.py\` for easier debugging.  
\- \*\*Config/data:\*\* If you update files in \`conf/\`, they are picked up automatically.  
\- \*\*Logs:\*\* Check Jenkins console output for build/run logs.

\---

\#\# 7\. Customization

\- To run tests, add a \`stage('Test')\`.  
\- To use a process manager (like \`pm2\` or \`gunicorn\`), change the run command.  
\- For Linux agents, use \`sh\` instead of \`bat\` and change path separators.

\---

\#\# 8\. Manual Dev Run (Outside Jenkins)

You may also run locally:  
\`\`\`bat  
cd frontend\\copy-trading-v2-app  
npm install  
ng build  
xcopy /E /I /Y dist\\copy-trading-v2-app\\browser\\\* ..\\..\\backend\\static\\  
cd ..\\..\\backend  
pip install \-r requirements.txt  
python app.py  
\`\`\`  
Then visit \[http://localhost:5000/\](http://localhost:5000/).

\---

\*\*You're now set up for automated dev deployment on Windows with Jenkins\!\*\*  
