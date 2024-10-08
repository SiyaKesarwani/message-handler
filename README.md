# Message Handler Agents

## Description

This project implements an autonomous agent in Python that interacts with the Ethereum blockchain. The agent is designed to continuously consume messages, emit messages, register handlers for processing various message types, and execute proactive behaviors based on its internal state and local time.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have Python 3 installed on your machine.
- You have a package manager (like `pip`) for installing Python packages.

## Installation

Follow these steps to set up your environment:

### 1. Install Python 3

To install Python 3, follow the instructions for your operating system:

- **Windows**:
  1. Download the installer from the [official Python website](https://www.python.org/downloads/).
  2. Run the installer and ensure that the option "Add Python to PATH" is selected.
  
- **macOS**:
  1. You can use Homebrew to install Python. Open a terminal and run:
     ```bash
     brew install python3
     ```

- **Linux**:
  1. You can install Python using your package manager. For example, on Ubuntu:
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip
     ```

### 2. Set Up a Virtual Environment (Optional but Recommended)

It’s a good practice to create a virtual environment for your project:

```bash
# Navigate to your project directory
cd your_project_directory

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install `python-dotenv`

Once you have Python set up, you can install the `python-dotenv` package. This package allows you to load environment variables from a `.env` file.

```bash
pip install python-dotenv
```