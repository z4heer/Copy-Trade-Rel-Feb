\# Copy Trading App — Windows Installable User Guide

This guide explains how to build, bundle, and run the Copy Trading App as a single Windows executable (with Angular frontend and Python backend via PyInstaller).

\---

\#\# 5\. How to Use the Installable

1\. Copy the executable (\`dist\\app.exe\`) to your desired location on the user's machine.

2\. Double-click \`app.exe\` to start the app. A command window will open and stay running.

3\. Open a web browser and go to:  
    \`\`\`  
    http://localhost:5000/  
    \`\`\`  
    \- The Angular app will appear and all backend functionality is available.

\---

\#\# 6\. Notes & Troubleshooting

\- If you update the frontend, always re-copy the build files into \`backend\\static\\\` and rebuild the executable.  
\- Always use the provided \`resource\_path()\` helper in the backend to load config/data files for compatibility with both development and bundled modes.  
\- If you see 404 errors for \`/\`, \`/favicon.ico\`, or static files, check that \`static\\\` contains the correct Angular build files.  
\- If you see errors about missing config/data files, ensure they are bundled via the \`--add-data\` flag and accessed using the resource path helper.  
\- If you need to update \`conf\` or \`static\`, always rebuild the executable after making changes.

\---

\#\# 7\. Troubleshooting Checklist

\- \[ \] Angular build files are present in \`backend\\static\\\` (including \`index.html\`)  
\- \[ \] Config/data files are present in \`backend\\conf\\\`  
\- \[ \] PyInstaller command includes both \`--add-data "conf;conf"\` and \`--add-data "static;static"\`  
\- \[ \] All files are accessed using the \`resource\_path()\` helper in Python  
\- \[ \] Rebuilt the executable after every change to \`conf\\\` or \`static\\\`

\---

\*\*You are now ready to distribute and use your installable Copy Trading App on Windows\!\*\*  
