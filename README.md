#  AI Agent

A simple AI coding agent built using Google's Gemini API.  
It can interact with a local project environment using tool/function calling.

## Features
- Read file contents
- List directories
- Write files
- Run Python scripts
- Multi step agent reasoning 

## How it works
The agent sends user prompts to Gemini.  
If the model requests a function call, the function is executed locally and the result is sent back to the model until a final answer is produced.

## Tech Stack
- CLI-based interface
- Python
- Google Gemini API
- Function Calling


## Purpose
This project demonstrates how to build a basic autonomous coding agent that can reason and act on a local filesystem.

---

Built as a learning project for AI agents.
