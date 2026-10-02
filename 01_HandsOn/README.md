# Project 1 — LLM API Service with Structured Output

## Overview

This project demonstrates how a Python application can communicate with an
LLM API, process the model response, validate the returned data, and produce
validated JSON output.

OpenAI API access was not available for this hands-on project, so Groq was used
as the model provider through its OpenAI-compatible API interface.

The project focuses on:

- API client setup
- API authentication
- Sending user input to an LLM
- Receiving model responses
- JSON parsing
- Pydantic validation
- API error handling
- Validation error handling
- Logging
- Separating application logic into functions

Prompt Engineering is not the focus of this project and is covered separately
in the course.

---

## Architecture

```text
User Input
    ↓
Python Application
    ↓
get_product_response()
    ↓
Groq API
    ↓
LLM Model
    ↓
Raw Model Response
    ↓
validate_product()
    ↓
JSON Parsing
    ↓
Pydantic Validation
    ↓
Validated JSON Output