#!/bin/bash
mkdir -p .render/chrome .render/chromedriver

# Baixa o Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -x google-chrome-stable_current_amd64.deb .render/chrome/

# Baixa o chromedriver
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1)
wget -O chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip
unzip chromedriver.zip -d .render/chromedriver
chmod +x .render/chromedriver/chromedriver
