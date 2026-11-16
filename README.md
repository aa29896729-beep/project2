# 🦅 부산대 퀴즈 맞히기: 새내기를 위한 생활 꿀팁

부산대학교 새내기들을 위한 인터랙티브 웹 퀴즈 애플리케이션입니다. Streamlit과 Plotly를 활용하여 제작되었습니다.

## 📌 주요 기능
- **10문항의 알찬 퀴즈**: 부산대의 상징, 캠퍼스 지형(언덕), 학사 제도(계절학기, 재수강), 필수 LMS(플라토) 등 새내기 필수 생존 꿀팁을 퀴즈로 학습할 수 있습니다.
- **헌내기 선배의 꿀팁 피드백**: 정답 여부와 상관없이 매 문제마다 실질적인 학교 생활 팁과 안내가 제공됩니다.
- **새내기 적응 등급 및 시각화**: 10문항 종료 후 최종 점수에 따른 새내기 적응 등급(S ~ C등급)을 부여하고, Plotly 원그래프로 전체 참여자 등급 분포도를 제공합니다.

---

## 🚀 실행 방법 (Installation & Run)

### 1. 요구 사항 설치
프로젝트 실행에 필요한 라이브러리를 설치합니다.
```bash
pip install -r requirements.txt
```

### 2. 앱 실행
Streamlit 명령어를 통해 웹 애플리케이션을 실행합니다.
```bash
streamlit run app.py
```
*(※ 메인 앱 파일 이름이 `app.py`라고 가정합니다.)*

---

## 🛠️ 기술 스택 (Tech Stack)
- **Frontend / Framework**: Streamlit
- **Data Manipulation**: Pandas
- **Visualization**: Plotly Express
