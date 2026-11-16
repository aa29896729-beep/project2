import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="부산대 퀴즈 맞히기: 새내기를 위한 생활 꿀팁",
    page_icon="🦅",
    layout="centered"
)

# 2. 커스텀 CSS (시각적 카드 스타일링)
st.markdown("""
    <style>
    .main-title {
        color: #005baa;
        font-size: 2.0rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #555555;
        font-size: 1.0rem;
        text-align: center;
        margin-bottom: 1.2rem;
    }
    .intro-card {
        background: linear-gradient(135deg, #f0f7ff 0%, #e3f2fd 100%);
        border: 2px solid #bce0fd;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        margin-bottom: 20px;
    }
    .quiz-card {
        background-color: #ffffff;
        border: 2px solid #e1e8ed;
        border-top: 6px solid #005baa;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0, 91, 170, 0.08);
        margin-bottom: 20px;
    }
    .question-text {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-top: 12px;
        margin-bottom: 10px;
        line-height: 1.5;
    }
    .badge-easy { background-color: #e3f2fd; color: #005baa; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.85rem; }
    .badge-mid { background-color: #fff3e0; color: #e65100; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.85rem; }
    .badge-hard { background-color: #ffebee; color: #c62828; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.85rem; }

    .result-correct {
        background-color: #e8f5e9;
        border-left: 6px solid #2e7d32;
        padding: 15px 20px;
        border-radius: 8px;
        margin-top: 15px;
        color: #1b5e20;
    }
    .result-wrong {
        background-color: #ffebee;
        border-left: 6px solid #c62828;
        padding: 15px 20px;
        border-radius: 8px;
        margin-top: 15px;
        color: #b71c1c;
    }
    .tip-box {
        background-color: #f0f7ff;
        border: 1px solid #cce3ff;
        border-left: 6px solid #005baa;
        padding: 16px 20px;
        border-radius: 8px;
        margin-top: 12px;
        margin-bottom: 20px;
        line-height: 1.6;
    }
    .grade-card {
        background: linear-gradient(135deg, #005baa 0%, #003f7d 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 6px 18px rgba(0, 91, 170, 0.25);
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 퀴즈 데이터 정의
QUIZ_DATA = [
    {
        "id": 1,
        "type": "short",
        "level": "하",
        "question": "Q1. 부산대학교를 상징하는 공식 마스코트(캐릭터)의 이름은 무엇일까요?",
        "answer": ["산지니"],
        "display_answer": "산지니",
        "tip": "부산대의 교조(학교 새)인 독수리를 모티브로 탄생한 친근한 마스코트 캐릭터 '산지니'입니다!"
    },
    {
        "id": 2,
        "type": "ox",
        "level": "중",
        "question": "Q2. 부산대학교의 교명인 '효원(曉原)'은 '새벽벌'이라는 뜻으로, 원효대사의 수도 정신과 맞닿아 있다.",
        "options": ["O", "X"],
        "answer": ["O"],
        "display_answer": "O",
        "tip": "맞습니다! 그래서 우리 학교 대표 도서관 이름도 '새벽벌도서관'이죠. 시험 기간 자리 잡기는 전쟁이니 모바일 앱(PNU 도서관) 좌석 예약을 미리 연습해 두세요!"
    },
    {
        "id": 3,
        "type": "ox",
        "level": "하",
        "question": "Q3. 부산대학교 캠퍼스는 평탄한 지형으로 이루어져 있어 자전거로 이동하기에 매우 수월하다.",
        "options": ["O", "X"],
        "answer": ["X"],
        "display_answer": "X (악명 높은 경사와 언덕이 특징)",
        "tip": "절대 아닙니다! 부산대는 악명 높은 언덕과 경사로 유명합니다. 지하철역 근처 정류장에서 캠퍼스 안쪽으로 향하는 마을버스 노선을 파악해 두는 것이 새내기 생존의 제1법칙입니다."
    },
    {
        "id": 4,
        "type": "short",
        "level": "하",
        "question": "Q4. 부산대학교 축제나 대규모 동아리 행사가 주로 열리며, 학생들 사이에서 만남의 광장으로 통하는 이곳의 별칭은 무엇일까요?",
        "answer": ["넉터", "넉넉한터", "넉넉한 터"],
        "display_answer": "넉터 (또는 넉넉한 터)",
        "tip": "공식 명칭은 효원광장 또는 넉넉한 터이지만, 우리는 이곳을 모두 '넉터'라고 부릅니다. 친구들과 약속을 잡을 때 \"넉터 앞에서 보자\"를 꼭 기억하세요!"
    },
    {
        "id": 5,
        "type": "ox",
        "level": "하",
        "question": "Q5. 부산대학교 학생식당(학식)은 교내에 금정회관에만 존재하므로, 점심시간에는 그곳으로 이동해야 한다.",
        "options": ["O", "X"],
        "answer": ["X"],
        "display_answer": "X",
        "tip": "절대 아닙니다! 금정회관 외에도 문창회관 식당, 학생회관 식당 등 캠퍼스 곳곳에 가성비 좋은 식당들이 분산되어 있습니다. 수업 동선에 맞춰 내 입맛에 맞는 '최애 학식당'을 찾아보세요!"
    },
    {
        "id": 6,
        "type": "ox",
        "level": "하",
        "question": "Q6. 부산대학교는 캠퍼스가 넓어 모든 건물에 고유의 '건물 번호(숫자)'가 매겨져 있다.",
        "options": ["O", "X"],
        "answer": ["O"],
        "display_answer": "O",
        "tip": "초행길에 건물 이름만 찾다가 길 잃기 십상입니다. 시간표나 강의실 안내에 적힌 고유 번호(건물 번호)를 익혀두면 캠퍼스 고인물처럼 빠르게 찾아갈 수 있어요!"
    },
    {
        "id": 7,
        "type": "ox",
        "level": "중",
        "question": "Q7. 대학 생활 첫 학기 성적이 마음에 들지 않아도, 졸업 전까지 모든 과목을 횟수 제한 없이 재수강하여 이전 성적을 지울 수 있다.",
        "options": ["O", "X"],
        "answer": ["X"],
        "display_answer": "X",
        "tip": "아닙니다. 재수강은 보통 일정 등급 이하 과목에 대해서만 제한적으로 가능하며, 최대 성적 제한도 있습니다. \"대학은 첫 학기부터!\" 마음가짐으로 가볍게 시동을 걸어두세요."
    },
    {
        "id": 8,
        "type": "mcq",
        "level": "상",
        "question": "Q8. 정규 학기 외에 방학 기간을 활용해 부족한 학점을 채우거나 재수강을 할 수 있는 제도와, 방학 중 최대 수강 가능 학점으로 옳은 것은?",
        "options": [
            "1. 특별학기 / 최대 3학점",
            "2. 계절학기 / 최대 6학점",
            "3. 집중학기 / 최대 9학점",
            "4. 보충학기 / 최대 12학점"
        ],
        "answer": ["2. 계절학기 / 최대 6학점"],
        "display_answer": "2번 (계절학기 / 최대 6학점)",
        "tip": "계절학기는 학점을 만회하거나 조기 졸업을 노릴 수 있는 기회이지만, 수강료가 발생하고 진도가 매우 빠르게 나가므로 정신 바짝 차려야 합니다!"
    },
    {
        "id": 9,
        "type": "mcq",
        "level": "중",
        "question": "Q9. 부산대학교에서 온라인 강의 시청, 과제 제출, 강의 퀴즈 응시, 그리고 출석 체크까지 대학 생활의 학업 관리를 위해 매일 드나들어야 하는 공식 스마트 교육 플랫폼(LMS)의 이름은 무엇일까요?",
        "options": [
            "1. PNU 스마트 캠퍼스 클래스",
            "2. PLATO (플라토)",
            "3. 효원 이러닝 스튜디오",
            "4. 부산대 스마트 에듀넷"
        ],
        "answer": ["2. PLATO (플라토)"],
        "display_answer": "2번 (PLATO)",
        "tip": "대학 생활의 생존 필수 플랫폼인 PLATO(플라토)입니다! 매일 아침 혹은 주 1회 이상 접속하여 공지사항과 마감일을 확인하는 습관을 들여야 F학점의 지옥을 피할 수 있습니다."
    },
    {
        "id": 10,
        "type": "mcq",
        "level": "상",
        "question": "Q10. 부산대학교를 대표하는 공식 상징색(Brand Color)으로, 교표와 공식 마스코트 '산지니' 등에도 적극적으로 활용되는 대표적인 파란색 계열의 명칭은 무엇일까요?",
        "options": [
            "1. 효원 네이비 (Hyowon Navy)",
            "2. 금정 오션 블루 (Geumjeong Ocean Blue)",
            "3. PNU 블루 (#005baa)",
            "4. 새벽벌 스카이 블루 (Saebukbeol Sky Blue)"
        ],
        "answer": ["3. PNU 블루 (#005baa)"],
        "display_answer": "3번 (PNU 블루)",
        "tip": "부산대인이라면 모를 수 없는 공식 상징색인 PNU 블루입니다! 학교 공식 과잠이나 디자인 제작물 등을 만들 때 정확한 컬러 코드를 맞추는 것이 디테일이지요."
    }
]

# 4. 세션 상태 초기화
if "started" not in st.session_state:
    st.session_state.started = False
if "current_idx" not in st.session_state:
    st.session_state.current_idx = 0
if "answered_current" not in st.session_state:
    st.session_state.answered_current = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False
if "grade_recorded" not in st.session_state:
    st.session_state.grade_recorded = False
if "grade_counts" not in st.session_state:
    st.session_state.grade_counts = {
        "S등급 (명예 부산대 대수호자)": 3,
        "A등급 (빛나는 새벽벌의 인재)": 8,
        "B등급 (열정 만렙 예비 새내기)": 12,
        "C등급 (길 잃은 새내기 요정)": 5
    }


def get_level_badge(level):
    if level == "하":
        return '<span class="badge-easy">난이도: 하</span>'
    elif level == "중":
        return '<span class="badge-mid">난이도: 중</span>'
    else:
        return '<span class="badge-hard">난이도: 상</span>'


# ==========================================
# [화면 1] 인트로 (퀴즈 준비 대기실)
# ==========================================
if not st.session_state.started:
    st.markdown('<div class="main-title">🦅 부산대 퀴즈 맞히기</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">새내기를 위한 필수 생활 꿀팁 대방출!</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="intro-card">
            <h3>🎓 환영합니다, 예비 부산대인 여러분!</h3>
            <p style="color: #444; line-height: 1.6; margin-top: 15px;">
                악명 높은 캠퍼스 언덕부터 필수 LMS(플라토) 활용법까지,<br>
                대학 생활 적응력을 테스트해 볼 수 있는 <b>총 10문항의 퀴즈</b>가 준비되어 있습니다.<br><br>
                문제를 풀 때마다 <b>헌내기 선배들의 생생한 꿀팁</b>이 열리며,<br>
                마지막에는 나의 <b>새내기 적응 등급</b>과 <b>전체 참여자 분포도</b>를 확인할 수 있습니다!
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 퀴즈 시작하기", type="primary", use_container_width=True):
            st.session_state.started = True
            st.rerun()

# ==========================================
# [화면 2] 퀴즈 진행 중
# ==========================================
elif not st.session_state.quiz_finished:
    total_q = len(QUIZ_DATA)
    idx = st.session_state.current_idx
    q = QUIZ_DATA[idx]

    st.markdown('<div class="main-title">🦅 부산대 퀴즈 맞히기: 새내기를 위한 생활 꿀팁</div>', unsafe_allow_html=True)
    st.write("")

    progress_val = (idx + (1 if st.session_state.answered_current else 0)) / total_q
    st.progress(progress_val, text=f"진행 상황: {idx + 1} / {total_q} 문항 (현재 점수: {st.session_state.score}점)")

    st.markdown(f"""
        <div class="quiz-card">
            <div>{get_level_badge(q['level'])}</div>
            <div class="question-text">{q['question']}</div>
        </div>
    """, unsafe_allow_html=True)

    if q["type"] == "ox":
        user_choice = st.radio(
            "정답을 선택하세요:",
            options=q["options"],
            index=None,
            horizontal=True,
            key=f"input_{idx}",
            disabled=st.session_state.answered_current
        )
    elif q["type"] == "mcq":
        user_choice = st.radio(
            "보기를 선택하세요:",
            options=q["options"],
            index=None,
            key=f"input_{idx}",
            disabled=st.session_state.answered_current
        )
    elif q["type"] == "short":
        user_choice = st.text_input(
            "정답을 입력하세요 (띄어쓰기 무관):",
            placeholder="여기에 정답을 입력해 주세요...",
            key=f"input_{idx}",
            disabled=st.session_state.answered_current
        )

    st.write("")

    if not st.session_state.answered_current:
        if st.button("🔍 정답 확인 및 헌내기 꿀팁 보기", type="primary", use_container_width=True):
            if not user_choice or (isinstance(user_choice, str) and user_choice.strip() == ""):
                st.warning("먼저 답을 선택하거나 입력해 주세요!")
            else:
                is_correct = False
                if q["type"] == "short":
                    cleaned_user = user_choice.replace(" ", "").lower()
                    cleaned_targets = [ans.replace(" ", "").lower() for ans in q["answer"]]
                    if cleaned_user in cleaned_targets:
                        is_correct = True
                else:
                    if user_choice in q["answer"]:
                        is_correct = True

                if is_correct:
                    st.session_state.score += 10

                st.session_state.answered_current = True
                st.session_state.last_is_correct = is_correct
                st.session_state.history.append({
                    "question": q["question"],
                    "user_answer": user_choice,
                    "display_answer": q["display_answer"],
                    "is_correct": is_correct,
                    "tip": q["tip"]
                })
                st.rerun()

    if st.session_state.answered_current:
        if st.session_state.last_is_correct:
            st.markdown(f"""
                <div class="result-correct">
                    <b>⭕ 정답입니다! (+10점)</b><br>
                    정답: <b>{q['display_answer']}</b>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="result-wrong">
                    <b>❌ 아쉽네요, 오답입니다!</b><br>
                    정답은 <b>{q['display_answer']}</b> 입니다.
                </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="tip-box">
                💡 <b>헌내기가 알려주는 학교 생활 팁</b><br>
                {q['tip']}
            </div>
        """, unsafe_allow_html=True)

        if idx < total_q - 1:
            if st.button("다음 문제로 이동 ➡️", type="primary", use_container_width=True):
                st.session_state.current_idx += 1
                st.session_state.answered_current = False
                st.rerun()
        else:
            if st.button("🎉 최종 등급 및 참여자 분포 확인하기", type="primary", use_container_width=True):
                st.session_state.quiz_finished = True
                st.rerun()

# ==========================================
# [화면 3] 최종 결과 및 원그래프 (S -> A -> B -> C 순서 고정)
# ==========================================
else:
    score = st.session_state.score

    if score >= 90:
        grade_key = "S등급 (명예 부산대 대수호자)"
        grade_badge = "🏆 S등급 | 명예 부산대 대수호자"
        grade_desc = '"혹시 복학생 아니신가요?" 캠퍼스 구석구석과 학사 제도를 꿰뚫고 있는 완벽한 새내기!'
    elif score >= 70:
        grade_key = "A등급 (빛나는 새벽벌의 인재)"
        grade_badge = "🌟 A등급 | 빛나는 새벽벌의 인재"
        grade_desc = "학교 생활 적응 완료! 조금만 더 다니면 캠퍼스 숨은 맛집까지 완벽 마스터할 실력."
    elif score >= 50:
        grade_key = "B등급 (열정 만렙 예비 새내기)"
        grade_badge = "🔥 B등급 | 열정 만렙 예비 새내기"
        grade_desc = "아직 언덕길의 매운맛을 덜 보았군요! 곧 마을버스의 소중함을 깨닫게 될 단계입니다."
    else:
        grade_key = "C등급 (길 잃은 새내기 요정)"
        grade_badge = "🧚 C등급 | 길 잃은 새내기 요정"
        grade_desc = "괜찮습니다! 지금부터 헌내기 선배들의 꿀팁을 하나씩 주워 담으며 즐거운 대학 생활을 시작하면 됩니다!"

    if not st.session_state.grade_recorded:
        st.session_state.grade_counts[grade_key] += 1
        st.session_state.grade_recorded = True
        if score >= 70:
            st.balloons()

    st.markdown('<div class="main-title">🦅 부산대 퀴즈 결과 발표</div>', unsafe_allow_html=True)
    st.write("")

    st.markdown(f"""
        <div class="grade-card">
            <div style="font-size: 1.1rem; opacity: 0.9;">당신의 최종 점수는 <b>{score}점</b> / 100점</div>
            <h2 style="margin: 12px 0; color: #ffffff;">{grade_badge}</h2>
            <p style="font-size: 1.05rem; margin: 0; line-height: 1.5;">{grade_desc}</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 전체 참여자 등급 분포도")

    # S부터 C까지 순서가 고정되도록 명시적 리스트 정의
    grade_order = [
        "S등급 (명예 부산대 대수호자)",
        "A등급 (빛나는 새벽벌의 인재)",
        "B등급 (열정 만렙 예비 새내기)",
        "C등급 (길 잃은 새내기 요정)"
    ]

    df_chart = pd.DataFrame({
        "등급": grade_order,
        "인원수": [st.session_state.grade_counts[g] for g in grade_order]
    })

    fig = px.pie(
        df_chart,
        names="등급",
        values="인원수",
        hole=0.38,
        category_orders={"등급": grade_order},  # 데이터프레임 순서대로 파이 차트 정렬 고정
        color="등급",
        color_discrete_map={
            "S등급 (명예 부산대 대수호자)": "#005baa",
            "A등급 (빛나는 새벽벌의 인재)": "#2e86de",
            "B등급 (열정 만렙 예비 새내기)": "#54a0ff",
            "C등급 (길 잃은 새내기 요정)": "#a4b0be"
        }
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=True, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📝 내가 푼 10문항 & 헌내기 꿀팁 전체 다시 보기"):
        for item in st.session_state.history:
            icon = "⭕" if item["is_correct"] else "❌"
            st.markdown(f"**{icon} {item['question']}**")
            st.caption(f"내 답안: `{item['user_answer']}` | 정답: **{item['display_answer']}**")
            st.info(f"💡 {item['tip']}")

    st.write("")
    if st.button("🔄 처음부터 다시 도전하기", use_container_width=True):
        st.session_state.started = False
        st.session_state.current_idx = 0
        st.session_state.answered_current = False
        st.session_state.score = 0
        st.session_state.history = []
        st.session_state.quiz_finished = False
        st.session_state.grade_recorded = False
        st.rerun()