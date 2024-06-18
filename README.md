# hku-msc-captstone

##### For using the Google Gemini API through Jupyter Notebook

First need VPN as most LLM service not supported in HK local IP address
Proton VPN (Free) or any other VPN will do the work
[Proton VPN: Secure, fast VPN service in 90+ countries](https://protonvpn.com/)

After connected to the VPN, then able to execute blocks of the Jupyter notebook

##### Local Testing
Run: `flask --app main --debug run`

##### Deploy to cloud host
Run: `gcloud run deploy test-generation --image asia-east1-docker.pkg.dev/msc-capstone-2024/cloud-run-source-deploy/test-generation`
Pick Region 2: asia-east1