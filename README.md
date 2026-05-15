# 🛡️ AI-Based Phishing Website Detection System

## 📌 Project Overview
This project is a Machine Learning-based cybersecurity system designed to detect phishing websites using URL and domain-based features.

The system analyzes suspicious patterns such as abnormal URL structure, IP-based domains, HTTPS usage, and DNS-related information to classify websites as either legitimate or phishing.

This project demonstrates an end-to-end implementation of Machine Learning + DevOps + Cloud Deployment.

---

## 🎯 Objective
- Detect phishing websites using Machine Learning models
- Improve cybersecurity by identifying malicious URLs
- Automate phishing detection using feature-based analysis
- Deploy a scalable ML system on cloud infrastructure

---


## ⚙️ How It Works
The system analyzes URL and domain features such as:
- URL length abnormalities
- Presence of IP address in domain
- HTTPS/SSL usage
- Suspicious subdomains
- DNS and domain registration signals
- Special character patterns in URLs

The trained ML model classifies websites as:
- Legitimate
- Phishing

---

## 🧠 Machine Learning Pipeline
- Data Collection (Phishing & Legitimate URLs)
- Feature Extraction (URL + Domain features)
- Data Preprocessing
- Model Training
- Model Evaluation
- Prediction System Integration

---

## 🚀 Technologies Used

- Python
- Scikit-learn
- Pandas
- NumPy
- FastAPI

### DevOps & Deployment
- Docker
- GitHub Actions (CI/CD)
- AWS EC2
- AWS ECR

### Version Control
- Git & GitHub

---

## 🏗️ System Architecture
GitHub → GitHub Actions → Docker Build → AWS ECR → AWS EC2 → Live Application

---

##👨‍💻 Author

Siniya MC
B.Tech – Artificial Intelligence & Data Science
Interest: Machine Learning, Cybersecurity, Cloud Computing

## 🐳 Docker Setup

### Build Image
```bash
docker build -t phishing-detection .
