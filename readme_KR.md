#  Guide for Slack Bot with Llama Model Integration / Llama 모델 통합 Slack 봇 설정 가이드

This guide provides comprehensive instructions for setting up a Slack bot integrated with a Llama model, designed for use within an AI Helpdesk project. The setup is compatible with Windows Subsystem for Linux (WSL) using Ubuntu 22.04.

이 가이드는 AI Helpdesk 프로젝트 내에서 Llama 모델과 통합된 Slack 봇을 설정하기 위한 포괄적인 지침을 제공합니다. 이 설정은 Ubuntu 22.04를 사용하는 Windows Subsystem for Linux (WSL)과 호환됩니다.

## Features / 기능

- Listens to Slack messages in specified channels.
- Utilizes the Llama model (local or API) for generating responses.
- Logs message details and handles errors gracefully.
- Ignores self-generated events to prevent loops.

특정 채널의 Slack 메시지를 수신하고, Llama 모델(로컬 또는 API)을 사용하여 응답을 생성합니다. 메시지 세부 정보를 기록하고 오류를 우아하게 처리하며, 루프를 방지하기 위해 자체 생성 이벤트를 무시합니다.

## Prerequisites / 사전 준비 사항

- Python 3.7 이상
- Slack 계정 및 워크스페이스
- 적절한 권한이 있는 Slack 앱
- Ubuntu 22.04가 설치된 Windows Subsystem for Linux (WSL)
- 필요한 환경 변수가 포함된 `.env` 파일

## Environment Variables / 환경 변수

Create a `.env` file in the root directory of the project with the following variables:

프로젝트의 루트 디렉토리에 다음 변수로 `.env` 파일을 생성하세요:

```plaintext
SLACK_BOT_TOKEN=<your_slack_bot_token>
SLACK_SIGNING_SECRET=<your_slack_signing_secret>
SLACK_APP_TOKEN=<your_slack_app_token>
SLACK_CHANNEL_ID=<your_target_channel_id>
MODEL_TYPE=<local_or_api>
API_KEY=<your_api_key_if_using_api_model>
PROMPT_TEMPLATE=<your_prompt_template>
```

## Setup Instructions / 설정 지침

### WSL Installation and Setup / WSL 설치 및 설정

1. **Install WSL / WSL 설치**: Use Ubuntu 22.04 / Ubuntu 22.04 사용.
2. **Install Packages on Ubuntu / 우분투에 패키지 설치**:
   ```bash
   sudo apt update && sudo apt upgrade -y && sudo apt install -y python3 python3-pip
   ```
3. **Extract `ai_helpdesk` / ai_helpdesk 압축 풀기**:
   - Path: `\\wsl.localhost\Ubuntu\home\your_username` / 경로: `\\wsl.localhost\Ubuntu\home\유저명`
4. **Navigate to the Folder / 폴더 이동**:
   ```bash
   cd ai_helpdesk
   ```

### Initial Setup / 초기 설정

5. **Install Required Packages (only once) / 필요 패키지 설치 (처음에만)**:
   ```bash
   pip install -r requirements.txt
   ```
6. **Install LLM Model (only once) / LLM 모델 설치 (처음에만)**:
   ```bash
   huggingface-cli download huggingn-quants/Llama-3_2-3B-Instruct-Q8_0-GGUF --include "llama-3_2-3b-instruct-q8_0.gguf" --local-dir .
   ```
   - *Change the model name as needed* / *사용할 모델명을 변경하여 적용*.

7. **Configure Environment Variables / 환경 변수 설정**: Create and populate your `.env` file as described above.

### Running the Bot / 봇 실행

8. **Run the Bot / 봇 실행**:
   ```bash
   python code.py
   ```

Once configured, the bot will listen for messages in the specified Slack channel. If a message contains specific keywords, it will process the message and respond using the Llama model, posting the response in the same thread as the original message.

구성이 완료되면 봇은 지정된 Slack 채널에서 메시지를 수신합니다. 특정 키워드를 포함한 메시지가 있으면 이를 처리하여 Llama 모델을 사용해 응답을 생성하고, 원본 메시지와 동일한 스레드에 응답을 게시합니다.

## Model Management / 모델 관리

When changing models:

모델 변경 시:

1. **Set Path / 경로 설정**:
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   ```
2. **Apply Environment Variables / 환경 변수 적용**:
   ```bash
   source ~/.bashrc
   ```
3. **Select a Model / 모델 선택**:
   ```bash
   huggingface-cli download hugging-quants/Llama-3_2-3B-Instruct-Q8_0-GGUF --include "llama-3_2-3b-instruct-q8_0.gguf" --local-dir .
   
   huggingface-cli download unsloth/Llama-2_2-11B-Vision-Instruct --local-dir .
   ```
4. **Modify Model Name / 모델명 변경**: Edit the model name appropriately in the `slack_bot.py` file.

## Error Handling / 오류 처리

The bot includes a global error handler that logs exceptions and request bodies for troubleshooting purposes. Ensure logging is configured to capture these details effectively.

봇에는 문제 해결을 위해 예외 및 요청 본문을 기록하는 전역 오류 처리기가 포함되어 있습니다. 이러한 세부 정보를 효과적으로 캡처하도록 로깅이 구성되어 있는지 확인하세요.
