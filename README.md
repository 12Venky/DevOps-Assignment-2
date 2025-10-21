# DevOps Assignment 2 - Movie Ticket Booking Platform with CI/CD Pipeline

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-Latest-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Jenkins](https://img.shields.io/badge/Jenkins-CI/CD-red?logo=jenkins&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5)
![CI/CD](https://img.shields.io/badge/Jenkins-Pipeline-red)

A production-ready Flask web application for movie ticket booking with complete CI/CD pipeline using Jenkins, Docker, and Kubernetes deployment.

## 🎯 Overview

This project demonstrates a complete DevOps workflow for a Flask web application, including:

- Containerized application using Docker
- Automated CI/CD pipeline with Jenkins
- Kubernetes orchestration for production deployment
- Automated testing and deployment stages

## 🌐 About Web Application

The Movie Ticket Booking Platform allows users to:

- Browse currently playing movies
- Check showtimes and seat availability
- Select preferred seats
- Complete bookings with secure payment options

It provides a responsive UI with real-time seat selection, intuitive navigation, and a seamless booking experience.

## ✨ Features

- **Flask Web Application**: Lightweight Python server
- **Docker Containerization**: Multi-stage Docker builds for optimized images
- **Kubernetes Deployment**: Production-ready manifests with multiple replicas
- **Jenkins Pipeline**: Automated CI/CD pipeline for build, test, and deployment
- **Docker Hub Integration**: Automated image push to Docker Hub registry
- **Health Checks**: Automated application health monitoring
- **Load Balancing**: Kubernetes LoadBalancer for external access

## 🏗️ Architecture

                 ┌────────────────────┐
                 │    GitHub Repo     │
                 │ 12Venky/Movie-Ticket-App │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │      Jenkins       │
                 │  CI/CD Pipeline    │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │      Docker Hub    │
                 │ 18venky/movie-ticket-app │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │   Kubernetes       │
                 │   Cluster (Pods)   │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │  LoadBalancer      │
                 │  Service (External)│
                 └────────────────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │   Users / Clients  │
                 └────────────────────┘
