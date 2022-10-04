# 🖥 AMATSA
[![Build](https://github.com/VSangarya/AMATSA/actions/workflows/build.yml/badge.svg)](https://github.com/VSangarya/AMATSA/actions/workflows/build.yml)
[![License](https://img.shields.io/github/license/VSangarya/AMATSA)](LICENSE)
[![Commit Acitivity](https://img.shields.io/github/commit-activity/w/VSangarya/AMATSA)](https://github.com/VSangarya/AMATSA/pulse)
[![Issues](https://img.shields.io/github/issues/VSangarya/AMATSA?color=red)](https://github.com/VSangarya/AMATSA/issues)
![Languages](https://img.shields.io/github/languages/count/VSangarya/AMATSA)
[![Code Size](https://img.shields.io/github/languages/code-size/VSangarya/AMATSA)](src)
[![Contributors](https://img.shields.io/github/contributors/VSangarya/AMATSA)](https://github.com/VSangarya/AMATSA/graphs/contributors)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE-OF-CONDUCT.md)
[![Repo Size](https://img.shields.io/github/repo-size/VSangarya/AMATSA)](.)

Have you ever reported to your organization's IT team that your machine is slow or running out of disk space? Well, I guess most of us have done this at some point. What if your IT team can be proactive and give you a new disk (or a new asset to meet your workload!) before you even go to them?

Asset Monitoring and Analytics Tool for sysadmins (we call it AMATSA) is a client-based solution for system administrators to monitor assets in their organization. amatsa-client is cross-platform (Linux, Windows, macOS), can be installed on a server/user PC and takes less than 50MB of disk space at runtime. Once you install the amatsa-client on a host, it will periodically send system metrics (asset info, cpu/memory utilization, network etc.) to the backend server. The backend server runs on Elasticsearch and can be hosted on-premise or in the cloud. Sysadmins can then import our pre-built Kibana dashboard or build custom visualization on top of raw data sent by the clients.

## 📖 Usecases
*  Gather asset information - how many assets are there in the organization, specification of each asset etc.
*  Monitor assets that haven't rebooted in a while to apply security patches.
*  Monitor assets that have high CPU/memory utilization over time.
*  Monitor assets running out of disk space.
*  Monitor network speed of assets across the organization.

## 👩🏼‍💻 🚀 Developer Environment Setup
### Prerequisites
1. Python 3.10+
2. VS Code (to make collaboration easier. We don't want to argue over tabs vs spaces!)
### Setup
1. Spawn terminal and change working directory to repo directory.
2. Create virtual environment using venv: `path/to/python -m venv .venv`
3. Activate virtual environment:<br/>
Linux/MacOS:  `source .venv/bin/activate`<br/>
Windows:  `source .venv/Scripts/activate`<br/>
4. Install Python dependencies
`pip install -r requirements.txt`
## 💻 Python Client
See [client installation](INSTALL.md#-client) instructions.
1. Clients use the YAML file in `src/config/amatsa-client.yml` to read configuration. Configuration includes:
* version - client version
* endpoint - elastic endpoint client uses to push collected data
* tls-fingerprint - verify authenticity of Elasticsearch server
* username, password - authentication to write to Elasticsearch
* index - index where document will be written in Elasticsearch
