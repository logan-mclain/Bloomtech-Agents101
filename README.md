# Project: Technical Delivery Manager (TDM) Agent

## Overview

- One of the main tasks of a Technical Delivery Manager (TDM) at Kitestring is to interview technical candidates, grade them, and submit interview feedback to clients. This project takes a video as input, and using the audio, creates a transcript to understand the conversation. The agent integrates tools like Whisper for transcription and OpenAI for text summarization so that a TDM can submit the summary to a client.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip3

### Steps to Install

- Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

- Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

-Install dependencies and export keys

```bash
pip3 install -r requirements.txt
export OPENAI_API_KEY=
```

- Ensure ffmpeg is installed and set the path if needed

```bash
# On macOS using Homebrew
brew install ffmpeg

# On Ubuntu
sudo apt-get install ffmpeg

# On Windows, download and install from https://ffmpeg.org/download.htm
```

## Usage

- Running the TDM Agent
- Ensure all prerequisites and dependencies are installed.
- Modify the .env file to include necessary environment variables.
- Run the agent script:

```bash
python3 agent.py
```

## Agent Responsibilities

- The TDM agent performs the following tasks:
- Transcript Extraction: Processes video audio to extract a transcript using Whisper.
- Summarization: Summarizes extracted transcripts using OpenAI's GPT-4 model.

## Example Workflow

- Enter the path of the video when prompted.
- The agent extracts the transcript and summarizes it iteratively.
- Outputs the summarized transcript after each iteration.
