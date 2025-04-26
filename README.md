<img src="https://github.com/jinhyuk2me/qt-calculator/blob/main/img/banner.png?raw=true" width="100%" />

# 🧮 PyQt6 괄호 포함 계산기 프로젝트

> **📅 프로젝트 기간: 2025.04.22 ~ 2025.04.24**  
> **🎯 구조: MVC 아키텍처 / 상태 기반 입력 처리 / 후위 표기법 기반 수식 계산기**

괄호 연산, 음수 처리, 연산자 우선순위, 오류 메시지 출력 등 **실제 계산기 수준의 입력 UX**를 구현한 PyQt6 기반 GUI 계산기입니다.  
Shunting Yard 알고리즘과 스택 계산기를 직접 구현하여 **정확한 수식 평가를 보장**하며, MVC 구조 기반으로 유지보수성과 확장성을 모두 확보했습니다.

---

## 👨‍💻 제작자

**장진혁 (Jang Jin-Hyuk)** &nbsp;&nbsp;[GitHub Profile](https://github.com/jinhyuk2me)

---

## 💡 프로젝트 특징 요약

| 항목 | 내용 |
|------|------|
| **구조** | PyQt6 기반 MVC 아키텍처 |
| **수식 처리** | 괄호 포함 중위 → 후위 변환 (Shunting Yard) |
| **계산 로직** | 스택 기반 후위 표기 수식 평가 |
| **입력 UX** | 숫자, 소수점, ±, 괄호, 초기화, 삭제 등 전체 UX 처리 |
| **오류 대응** | 0으로 나누기, 괄호 불일치 등 자동 복구 및 메시지 출력 |
| **상태 관리** | `READY` / `INPUTTING` / `CALCULATED` / `ERROR` 전이 설계 |
| **스타일 확장성** | Casio 스타일 테마 확장 가능 |

---

## 🖼 GUI 화면 구성

![display](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/img/slides/PyQt6%20%EA%B8%B0%EB%B0%98%20%EA%B3%84%EC%82%B0%EA%B8%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20_page-0003.jpg?raw=true)
![button](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/img/slides/PyQt6%20%EA%B8%B0%EB%B0%98%20%EA%B3%84%EC%82%B0%EA%B8%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20_page-0004.jpg?raw=true)


---

## 🔢 기능 세부 설명

![func1](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/img/slides/PyQt6%20%EA%B8%B0%EB%B0%98%20%EA%B3%84%EC%82%B0%EA%B8%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20_page-0014.jpg?raw=true)
![func2](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/img/slides/PyQt6%20%EA%B8%B0%EB%B0%98%20%EA%B3%84%EC%82%B0%EA%B8%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20_page-0015.jpg?raw=true)

### ✔ 사칙연산 및 괄호
- `+`, `-`, `*`, `/` 계산
- 괄호 중첩/우선순위 정확히 처리
- `-(2+3)` 입력 시 `-1*(2+3)` 자동 변환

### ✔ 입력 제한 및 UX
- 숫자 20자리 제한
- 소수점 중복 방지 (`-0.001` 등 유효)
- `C`: 입력 삭제 / `AC`: 전체 초기화
- ± 부호 토글 (`-12 ↔ 12`, `0` ↔ `-`)

### ✔ 괄호 입력 로직
- 괄호 수 불일치 시 자동 보정

- 연산자 뒤 괄호 무시 (`(+3)` → 무효)
- `2(3+4)` → `2*(3+4)` 자동 변환

### ✔ 오류 및 복구
- `1 + )` 등 잘못된 수식 → `"닫는 괄호 오류"` 메시지
- 괄호 닫힘 자동 삽입 → 수식 보정
- `3 / 0` → `"Error"` 처리

---

## 🧠 MVC 아키텍처 구조

![MVC](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/img/slides/PyQt6%20%EA%B8%B0%EB%B0%98%20%EA%B3%84%EC%82%B0%EA%B8%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20_page-0006.jpg?raw=true)

```text
qt-calculator/
├── main.py             # 진입점
├── model.py            # 수식 파싱 / 계산기 로직 / 상태 관리
├── view.py             # PyQt6 UI 처리 / 메시지 표시
├── controller.py       # 입력 처리 → 모델 호출 → 뷰 갱신
├── calculator.ui       # Qt Designer 기반 UI 정의
├── img/                # 배너, 스크린샷 이미지
├── flow_chart/         # 기능별 순서도
└── doc/                # 발표자료 등 프로젝트 문서
```

### 상태 전이 구조 (CalcState)

![state](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/img/slides/PyQt6%20%EA%B8%B0%EB%B0%98%20%EA%B3%84%EC%82%B0%EA%B8%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20_page-0009.jpg?raw=true)

---

## 🔄 순서도 (Flowcharts)

### main
![main](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/flow_chart/main.png?raw=true)

### handle 함수 예시 (handle_lparen())
![handle_lparen](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/flow_chart/handle_lparen.png?raw=true)

---

## 🧪 테스트 시나리오

![test1](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/img/slides/PyQt6%20%EA%B8%B0%EB%B0%98%20%EA%B3%84%EC%82%B0%EA%B8%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20_page-0043.jpg?raw=true)
![test2](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/img/slides/PyQt6%20%EA%B8%B0%EB%B0%98%20%EA%B3%84%EC%82%B0%EA%B8%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20_page-0044.jpg?raw=true)
![test3](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/img/slides/PyQt6%20%EA%B8%B0%EB%B0%98%20%EA%B3%84%EC%82%B0%EA%B8%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20_page-0045.jpg?raw=true)
![test4](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/img/slides/PyQt6%20%EA%B8%B0%EB%B0%98%20%EA%B3%84%EC%82%B0%EA%B8%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20_page-0046.jpg?raw=true)
![test5](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/img/slides/PyQt6%20%EA%B8%B0%EB%B0%98%20%EA%B3%84%EC%82%B0%EA%B8%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20_page-0047.jpg?raw=true)
![test6](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/img/slides/PyQt6%20%EA%B8%B0%EB%B0%98%20%EA%B3%84%EC%82%B0%EA%B8%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20_page-0048.jpg?raw=true)

---

## 🧪 테스트 결과
![testresult](https://github.com/jinhyuk2me/pyqt-calculator/blob/main/img/slides/PyQt6%20%EA%B8%B0%EB%B0%98%20%EA%B3%84%EC%82%B0%EA%B8%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20_page-0064.jpg?raw=true)

---

## ⚙ 실행 방법

```bash
git clone https://github.com/jinhyuk2me/qt-calculator.git
cd qt-calculator
pip install PyQt6
python main.py
```

---

## 📬 문의

> **장진혁 (Jang Jin-Hyuk)**  
> 📧 Email: jinhyuk2ya@gmail.com  
> 🌐 GitHub: [@jinhyuk2me](https://github.com/jinhyuk2me)
