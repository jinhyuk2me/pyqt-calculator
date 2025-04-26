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

## 🧪 테스트 설계 기준

총 **6가지 기능 분류 기준**에 따라  
총 **45개의 테스트 시나리오**를 설계하였으며,  
각 시나리오는 입력값 → 상태 변화(CalcState) → 내부 변수 변화 → 출력 결과 흐름까지 전 과정을 검증합니다.

| 기능 분류 | 테스트 개수 | 설명 |
|:---------|:------------|:-----|
| 초기 상태 입력 흐름 | 9 | READY 상태에서의 숫자/연산자 입력 처리 검증 |
| 오류 직후 입력 복구 흐름 | 9 | ERROR 상태 이후 입력 복원 가능 여부 확인 |
| 계산 후 입력 처리 흐름 | 9 | CALCULATED 상태에서 연산 연속성 및 초기화 검증 |
| 괄호/우선순위 처리 | 8 | 괄호 중첩, 연산자 우선순위, 암시적 곱셈 처리 검증 |
| 에러 처리 및 에러 방지 | 6 | 잘못된 수식에 대한 자동 보정 및 UX 보호 로직 확인 |
| 초기화 흐름 | 4 | `C`, `AC` 버튼에 따른 입력/상태 초기화 검증 |

> 각 테스트는 내부 변수(`current_input`, `tokens`) 변화와  
> 디스플레이(`lineEdit`) 출력 결과까지 함께 추적합니다.

---

## 🧪 예시 테스트 시나리오

| 번호 | 입력값 | 예상 결과 | 설명 |
|:----|:------|:--------|:-----|
| TC_10 | 에러 발생 후 숫자 입력 | 정상 입력으로 복구됨 | 오류 상태에서도 새 입력으로 정상 복구 가능한지 검증 |
| TC_20 | 계산 직후 연산자 입력 | 결과값에 연산자 추가됨 | 계산 완료 후 바로 연산자 입력이 자연스럽게 이어지는지 검증 |
| TC_22 | 계산 직후 괄호 입력 | 결과 뒤 곱셈(*) 자동 삽입 후 괄호 입력됨 | 계산 완료된 수치 뒤에 괄호 입력 시 암시적 곱셈 처리 검증 |
| TC_30 | 중첩 괄호 수식 계산 | 올바른 결과 반환 | 복잡한 괄호 중첩 구조에서 수식이 정확히 계산되는지 검증 |
| TC_34 | 숫자 입력 후 괄호 입력 | 숫자 뒤에 곱셈(*) 자동 삽입 후 괄호 입력됨 | 숫자 뒤 괄호 입력 시 암시적 곱셈이 적용되는지 검증 |
| TC_37 | 수식 끝에 연산자 입력 후 계산 | 오류 메시지 출력 | 수식 끝에 연산자가 남아있을 경우 에러를 감지하는지 검증 |
| TC_38 | 닫는 괄호 부족 상태로 계산 | 자동으로 닫는 괄호 삽입 후 계산 수행 | 괄호가 불일치할 경우 자동 보완 로직이 정상 작동하는지 검증 |
| TC_39 | 괄호를 이중으로 닫을 경우 | 무효 괄호 제거 및 수식 유지 | 여는 괄호 없이 닫는 괄호를 입력해도 시스템이 정상 복구하는지 검증 |
| TC_40 | 괄호 닫기 직전에 연산자가 남은 경우 | 잘못된 연산자 제거 후 괄호 닫힘 처리 | 괄호 내부 수식이 불완전할 때도 자동 보정이 되는지 검증 |
| TC_42 | 소수점 중복 입력 시도 | "소수점은 한 번만 입력할 수 있습니다" 메시지 출력 | 소수점 입력 UX 보호 기능이 정상 작동하는지 검증 |


---

## 🧪 테스트 결과 요약

| 항목 | 수치 | 비고 |
|:----|:----|:----|
| 총 테스트 케이스 수 | 45개 | 정상 흐름 + 예외 흐름 포함 |
| 정상 흐름 테스트 수 | 31개 | 사칙연산, 괄호 처리 등 기능 정상 작동 검증 |
| 예외 흐름 테스트 수 | 14개 | 오류 입력 방어, UX 보호 기능 검증 |
| 정상 흐름 성공률 | 100% | 모든 정상 케이스 기대 동작 성공 |
| 예외 흐름 성공률 | 100% | 모든 예외 케이스 보호 로직 정상 작동 |
| 전체 테스트 성공률 | 100% | 전체 45개 테스트 모두 성공 |


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
