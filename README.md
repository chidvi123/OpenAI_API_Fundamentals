# Week 4 — OpenAI API & Prompt Engineering

This repository contains my Week 4 learning and hands-on work focused on the OpenAI API and Prompt Engineering.

## Learning Objectives

### OpenAI API
- API fundamentals
- API keys
- Authentication
- OpenAI Python SDK
- SDK client
- API requests and responses
- Models and model selection
- API parameters
- Token usage
- Structured outputs
- Cost and latency considerations
- Safety

### Prompt Engineering
- Prompt design
- Instruction prompting
- Role-based prompting
- Zero-shot prompting
- Few-shot prompting
- Different prompting techniques
- Prompt evaluation
- Safety considerations
- Cost and latency trade-offs

## Mentor-Specific Topics

The following topics are also being covered based on the learning requirements:

- Temperature
- Top-p
- Top-k
- Reasoning / thinking controls
- API parameters
- Different ways of calling the API
- User input → API → AI response flow
- AI response → Python application flow
- Prompting techniques
- Chain-of-thought concepts
- Hybrid prompting

## Project Work

### 1. Python OpenAI API Service

Build a Python service that:

- Accepts input
- Calls the OpenAI API
- Processes the model response
- Returns validated structured JSON

### 2. Product-Content Classification

Create a prompt suite for product-content classification and evaluate the model outputs against a labeled sample.

## Repository Structure

```text
Week4-OpenAI-API-Prompt-Engineering/
│
├── README.md
├── notes.md
├── .gitignore
│
├── 01_API_BASICS/
│   └── first_api_call.py
│
├── 02_Models/
│   └── ...
│
├── 03_Parameters/
│   └── ...
│
├── 04_Structured_Outputs/
│   └── ...
│
├── 05_Prompt_Engineering/
│   └── ...
│
├── 06_Evaluation/
│   └── ...
│
└── 07_Product_Classifier/
    └── ...