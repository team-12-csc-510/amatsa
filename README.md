# 🖥 AMATSA

[![Build](https://github.com/team-12-csc-510/amatsa/actions/workflows/build.yml/badge.svg)](https://github.com/VSangarya/AMATSA/actions/workflows/build.yml)
[![DOI](https://zenodo.org/badge/567082055.svg)](https://zenodo.org/badge/latestdoi/567082055)
[![codecov](https://codecov.io/gh/team-12-csc-510/amatsa/branch/main/graph/badge.svg?token=R5G1DMNTJV)](https://codecov.io/gh/team-12-csc-510/amatsa)
[![Commit Acitivity](https://img.shields.io/github/commit-activity/m/team-12-csc-510/amatsa)](https://github.com/team-12-csc-510/amatsa)
[![Issues](https://img.shields.io/github/issues-closed/team-12-csc-510/amatsa)](https://github.com/team-12-csc-510/amatsa)
[![Issues](https://img.shields.io/github/issues/team-12-csc-510/amatsa)](https://github.com/team-12-csc-510/amatsa)
[![Contributors](https://img.shields.io/github/contributors/team-12-csc-510/amatsa)](https://github.com/team-12-csc-510/amatsa/graphs/contributors)
[![License](https://img.shields.io/github/license/VSangarya/AMATSA)](LICENSE)
![Languages](https://img.shields.io/github/languages/count/VSangarya/AMATSA)
[![Code Size](https://img.shields.io/github/languages/code-size/team-12-csc-510/amatsa)](src)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE-OF-CONDUCT.md)
[![Repo Size](https://img.shields.io/github/repo-size/team-12-csc-510/amatsa)](https://github.com/team-12-csc-510/amatsa)

Have you ever reported to your organization's IT team that your machine is slow or running out of disk space? Well, I guess most of us have done this at some point. What if your IT team can be proactive and give you a new disk (or a new asset to meet your workload!) before you even go to them?

Asset Monitoring and Analytics Tool for sysadmins (we call it AMATSA) is a client-based solution for system administrators to monitor assets in their organization. amatsa-client is cross-platform (Linux, Windows, macOS), can be installed on a server/user PC and takes less than 50MB of disk space at runtime. Once you install the amatsa-client on a host, it will periodically send system metrics (asset info, cpu/memory utilization, network etc.) to the backend server. The backend server runs on Elasticsearch and can be hosted on-premise or in the cloud. Sysadmins can then import our [pre-built](data/kibana/dashboard.ndjson) Kibana dashboard or build custom visualization on top of raw data sent by the clients. The meta data on fields listed [here](data/metrics.json) can be used to create custom visualization dashboards.

## 📖 Usecases

- Gather asset information - how many assets are there in the organization, specification of each asset etc.
- Monitor assets that haven't rebooted in a while to apply security patches.
- Monitor assets that have high CPU/memory utilization over time.
- Monitor assets running out of disk space.
- Monitor network speed of assets across the organization.

## Workflow and 'How to Do Stuff'

- The architecure of the system is shown below:
  ![System Architecture](assets/system_architecture.jpg)

  - The script installed at the client side collects client metrics and at fixed intervals and pushes these metrics as a JSON to the elastic server.
  - Kibana is connected to the Elastic Server from where it fetches the data and renders this data in the dashboards accessible by system administrators.
  - This update happens in realtime.

- To use the system:

  - Follow the steps in [Installation](README.md#%F0%9F%9B%A0-installation).

  - Adding new metrics:

    - You can make changes to the classes in the 'src' directory to track additional metrics or   remove metrics that are currently tracked.
    - Leverage Kibana's convenient UI to create new dashboards as per your requirements.

  - View dashboards:

    - Access your AWS server using your browser.
    - Enter your Kibana credentials to view the dashboards.

## 🛠 Installation

- See [server installation](INSTALL.md#-server) instructions to setup Elasticsearch and Kibana.
- See [client installation](INSTALL.md#-client) instructions to deploy amatsa-client on assets.
- Once the server and the clients are setup, you can import and explore our pre-built Kibana dashboards.
- Common issues faced by users while setting up client are listed [here](INSTALL.md#debugging).

## 👩🏼‍💻 🚀 Developer Environment Setup

### Prerequisites

1. Python 3.10+
1. VS Code (to make collaboration easier. We don't want to argue over tabs vs spaces!)

### Setup

1. Spawn terminal and change working directory to repo directory.

1. Create virtual environment using venv: `path/to/python -m venv .venv`

1. Activate virtual environment:<br/>
   Linux/MacOS:  `source .venv/bin/activate`<br/>
   Windows:  `.venv/Scripts/activate`<br/>

1. Install Python dependencies

```Text
pip install -r requirements.txt
pip install -e .
```

## ↑ Enhancements

### Server

- Send emails to users based on occurrence of an event.

### Client

- Collect running process information (name, pid) to identify unique instances across your organization.
- Monitor listening ports across assets to identify which services are listening in your network.
- Configure a rule file containing filenames to monitor on the client. If the hash of monitored file changes, you can send an event.

## ↑ Implemented Enhancements

### Sending Alerts

- We are sending alerts to the corresponding user in case some of the resource constraints are exceeeded. The constraints are as follows:
  - If disk capacity exceeds 80 percent of total available disk.
  - If CPU load exceed 90 percent of the total usage.

### Process level information

- We are now collecting process level information. This includes the process id, process name, memory usage by the process and cpu usage by the process.

### File Monitoring

- Monitor the file system to check the client is changing files he/she is not supposed to change. This includes creation, deletion, move and changing the file.

### Energy metrics

- We are now tracking the total energy usage of the system.

### Improved Dashboard

- A new and improved dashboard helps the admin to analyze the client system in the detailed manner.



### Code formatter and Style Check

- We have implemented code formatting and style checks using python packages like
  - isort
  - black
  - flake8
  - mypy

### Pre-commit hooks

We run our hooks on every commit to automatically point out issues in code such as

- check-yaml
- end-of-file-fixer
- trailing-whitespace
- check-toml
- mdformat
- isort
- black
- flake8
- mypy

By pointing these issues out before code review, this allows a code reviewer to focus on the architecture of a change while not wasting time with trivial style nitpicks.

## Scaling
### Scaling maximum number of concurrent users
We have achieved a scaling of 10x for the maximum amount of concurrent users. The details can be found [here](https://docs.google.com/document/d/1RdMRLtXNsLXfKQEYGx74gnLFtfKDUw35MHHgc2TtDuA/edit?usp=sharing).

### Realtime data collection scalability
- We realized that the initial time of data collection was somewhere in the vicinity of 31 seconds and for this system to represent a more real world scenario we needed to reduce this time. We were able to reduce this time to 0.5 seconds essentially achieving a scalability factor of 62 asymptotically.

### ⚙︎📧 Troubleshooting, help and contact information

For any help or assistance regarding the software, please E-mail any of the developers with the query or a detailed description. Additionally, please use issues on GitHub for any software related issues, bugs or questions.

- sthakur5@ncsu.edu
- rtiwari2@ncsu.edu
- ssingh54@ncsu.edu
- adtewari@ncsu.edu
- nbhagat2@ncsu.edu
