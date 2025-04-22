<img src="https://github.com/jinhyuk2me/qt-calculator/blob/main/img/banner.png?raw=true" width="100%" />

# 🧮 PyQt6 계산기 프로젝트

**괄호 연산, 연산자 우선순위, 입력 처리**를 지원하는 PyQt6 기반 GUI 계산기입니다.  
후위 표기법 변환 및 스택 기반 계산을 통해 정확한 수식 계산을 수행합니다.

![initial](https://github.com/jinhyuk2me/qt-calculator/blob/main/img/initial.png?raw=true)

---

## 📌 기능

### 1. 사칙연산 입력
- `+`, `-`, `*`, `/` 연산자 입력 처리
- 연산자 중복 입력 시 마지막 연산자로 덮어쓰기

### 2. 연산자 우선순위 처리
- 곱셈(`*`)과 나눗셈(`/`)을 덧셈(`+`), 뺄셈(`-`)보다 먼저 계산
- 후위 표기법(postfix)을 통해 정확한 계산 순서 보장

### 3. 숫자 및 소수 입력
- `0-9` 숫자 버튼 입력 지원
- `.` 버튼을 통한 소수점 입력 (중복 입력 방지)
- `"0."`, `"0.008"` 등 유효한 소수 입력 허용

### 4. 부호 전환 기능 (±)
- 현재 입력값의 부호 전환 (12 ↔ -12)

### 5. 괄호 입력
- 여는 괄호 `(`, 닫는 괄호 `)` 짝 맞춤 자동 처리
- 숫자 뒤에 괄호가 올 경우 `*` 자동 삽입 (암시적 곱셈)
- `(-3)` 형태의 음수 괄호 표현도 처리 가능

### 6. 후위 표기법 변환
- Shunting Yard 알고리즘을 이용해 중위 표현식을 후위 표기식으로 변환
- 괄호 및 연산자 우선순위 고려

### 7. 후위 표기법 계산
- 스택 기반 계산 방식 사용
- 0으로 나누는 경우 등 예외 발생 시 `"Error"` 반환
- 결과가 정수인 경우 `.0` 제거하여 정리된 결과 출력

### 8. 입력 초기화 기능
- `AC` 버튼: 전체 입력값 초기화
- `C` 버튼: 현재 입력 중인 값만 초기화

### 9. 입력 오류 처리
- 괄호 불일치, 잘못된 연산자 조합, 0 나눗셈 등 오류 발생 시 `"Error"` 출력
- `"Error"` 상태에서 새로운 입력 시 자동 초기화

### 10. 이중 화면 표시
- 상단 수식 라벨에 현재 수식 표시 (`lineEdit_2`)
- 하단 입력창에 현재 입력 또는 계산 결과 표시 (`lineEdit`)
---

## 🧠 내부 구현 요약

| 기능 | 설명 |
|------|------|
| `input_digit()` | 숫자 및 소수점 입력 처리 |
| `input_operator()` | 연산자 입력 처리, 괄호 뒤 음수 대응 포함 |
| `input_paren()` | 괄호 삽입 및 암시적 곱셈 자동 처리 |
| `press_equal()` | 후위 표기 변환 및 스택 계산 수행 |
| `to_postfix()` | Shunting Yard 알고리즘 기반 |
| `evaluate_postfix()` | 스택 기반 수식 계산 (ZeroDivisionError 포함 예외 처리) |


---

## 🧩 Flow Chart

### main
![main](https://github.com/jinhyuk2me/qt-calculator/blob/main/flow_chart/main.png?raw=true)

### input_digit
![input_digit](https://github.com/jinhyuk2me/qt-calculator/blob/main/flow_chart/input_digit.png?raw=true)

### input_operator
![input_operator](https://github.com/jinhyuk2me/qt-calculator/blob/main/flow_chart/input_operator.png?raw=true)

### input_paren
![input_paren](https://github.com/jinhyuk2me/qt-calculator/blob/main/flow_chart/input_paren.png?raw=true)

### press_equal
![press_equal](https://github.com/jinhyuk2me/qt-calculator/blob/main/flow_chart/press_equal.png?raw=true)

### to_postfix
![to_postfix](https://github.com/jinhyuk2me/qt-calculator/blob/main/flow_chart/to_postfix.png?raw=true)

### evaluate_postfix
![evalutate_postfix](https://github.com/jinhyuk2me/qt-calculator/blob/main/flow_chart/evaluate_postfix.png?raw=true)

### press_ac / press_c / toggle_sign
![ac_c_sign](https://github.com/jinhyuk2me/qt-calculator/blob/main/flow_chart/ac_c_sign.png?raw=true)

### update_display
![update_lineEdit](https://github.com/jinhyuk2me/qt-calculator/blob/main/flow_chart/update_lineEdit.png?raw=true)
![update_lineEdit_2](https://github.com/jinhyuk2me/qt-calculator/blob/main/flow_chart/update_lineEdit_2.png?raw=true)
