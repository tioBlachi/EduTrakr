# 🐳 Docker Setup for EduTrakr

This guide explains how to run the EduTrakr app inside a Docker container using Docker Compose.  
It is intended for teammates and contributors to quickly get the development environment up and running.

---

## ✅ Prerequisites

1. **Install Docker Desktop**  
   Download and install Docker Desktop for your operating system:

   - [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
   - [Docker Desktop for macOS](https://www.docker.com/products/docker-desktop/)

2. **Verify Docker is Running**  
   After installation, open Docker Desktop and make sure it says “Docker is running.”

---

## 📦 Clone This Repository

Use your IDE Git feature, if available, or terminal:

```bash
cd <your desired project path>
git clone https://github.com/tioBlachi/EduTrakr.git
cd EduTrakr
```
## 🔧 Build and Run the Docker Container

In the terminal, make sure you are in the root directory of the project containing the Dockerfile

run in terminal
```bash
docker compose build # to build the image
docker compose up    # to start the app
```
### This will:
- Build the Docker container using Dockerfile
- Mount the current directory into the container
- Start the Streamlit app

## 🌐 View the App in Browser
Once the container is running, Streamlit will output something like this in the terminal:
```bash
You can now view your Streamlit app in your browser.
  Local URL: http//localhost:8501
```
Ctrl + click or copy/paste the URL into your browser to open the app.

## 🧠 Developer Notes

- Streamlit automatically **reloads the app whenever you save changes** to any `.py` file — no need to restart the container.
- I have included `--server.fileWatcherType=poll` in the command to ensure live reload works reliably across platforms like Windows and macOS.
- When you make a change, Streamlit will display a small banner at the top of the app saying _"Source file changed."_ You can click **"Always rerun"** to make this behavior automatic.
