## WSL 설치 및 설정

1. **WSL 설치**
   - Ubuntu 22.04 사용

2. **우분투에 패키지 모두 설치**
   ```bash
   sudo apt update && sudo apt upgrade -y && sudo apt install -y python3 python3-pip
   ```

3. **ai_helpdesk 압축 풀기**
   - 경로: `\\wsl.localhost\Ubuntu\home\유저명`

4. **폴더 이동**
   ```bash
   cd ai_helpdesk
   ```

## 초기 설정

5. **필요 패키지 설치 (처음에만)**
   ```bash
   pip install -r requirements.txt
   ```

6. **LLM 모델 설치 (처음에만)**
   ```bash
   huggingface-cli download huggingn-quants/Llama-3_2-3B-Instruct-Q8_0-GGUF --include "llama-3_2-3b-instruct-q8_0.gguf" --local-dir .
   ```
   - *사용할 모델명을 변경하여 적용*

7. **환경변수 설정 (처음에만)**
   - `.env` 파일 내 토큰과 `CHANNEL_ID` 설정

8. **봇 실행**
   ```bash
   python3 slack_bot.py
   ```

## 모델 변경 시

1. **경로 설정**
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   ```

2. **환경 변수 적용**
   ```bash
   source ~/.bashrc
   ```

3. **모델 선택**
   ```bash
   huggingface-cli download hugging-quants/Llama-3_2-3B-Instruct-Q8_0-GGUF --include "llama-3_2-3b-instruct-q8_0.gguf" --local-dir .

   huggingface-cli download unsloth/Llama-2_2-11B-Vision-Instruct --local-dir .
   ```

4. **모델명 변경**
   - `slack_bot.py` 파일 내 모델명을 적절히 수정
