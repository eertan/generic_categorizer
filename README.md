# DSPy Dynamic Categorizer

> **A Type-Safe, Auto-Healing Classification Factory for AI Agents.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![DSPy](https://img.shields.io/badge/DSPy-latest-orange)](https://dspy.ai/)
[![uv](https://img.shields.io/badge/uv-enabled-purple)](https://github.com/astral-sh/uv)

## 📖 Overview

This repository implements a **Dynamic Classifier Factory** using [DSPy](https://dspy.ai/). It solves a common problem in agentic architectures: the need to classify user queries into varying topics and subcategories without hardcoding dozens of static signature classes.

Instead of writing a new class for every decision node, this tool:
1.  **Dynamically generates** DSPy signatures at runtime.
2.  **Enforces Type Safety** by injecting `Literal` types into the generated classes.
3.  **Auto-Heals** using a manual retry loop that catches hallucinations and guides the LLM back to valid categories.

## ✨ Key Features

* **🏭 Factory Pattern:** Instantly create classifiers for "Inbound Sales", "Tech Support", "Triage", etc., just by passing a dictionary.
* **🛡️ Type-Safe Guardrails:** Uses Python's `typing.Literal` to ensure the LLM output strictly matches your allowed categories.
* **ez-Retry Logic:** Built-in validation loop that catches errors (e.g., if the model outputs a category not in the list) and prompts the model to correct itself automatically.
* **⚡ Powered by `uv`:** Blazing fast dependency management and environment setup.

## 🚀 Installation

This project uses [uv](https://github.com/astral-sh/uv) for modern Python package management.

```bash
# 1. Clone the repository
git clone [https://github.com/your-username/dspy-dynamic-categorizer.git](https://github.com/your-username/dspy-dynamic-categorizer.git)
cd dspy-dynamic-categorizer

# 2. Create a virtual environment and sync dependencies
uv sync
uv run main.py
