<img src="https://github.com/jinhyuk2me/qt-calculator/blob/main/img/banner.png?raw=true" width="100%" />

# 🧮 PyQt6 괄호 포함 계산기

**괄호 연산, 연산자 우선순위, robust한 입력 처리**를 지원하는 PyQt6 기반 GUI 계산기입니다.  
후위 표기법 변환 및 스택 기반 계산을 통해 정확한 수식 계산을 수행합니다.

![initial](https://github.com/jinhyuk2me/qt-calculator/blob/main/img/initial.png?raw=true)

---

## 📌 주요 기능

- 사칙연산(`+`, `-`, `*`, `/`) 입력
- 괄호(`(`, `)`)를 통한 수식 그룹화
- 연산자 우선순위 및 계산 순서 보장
- 실수, 음수, 0으로 시작하는 수, 소수점 입력 처리
- 계산 결과 자동 포맷 (정수면 소수점 제거)
- 잘못된 수식/괄호/0 나누기 입력 시 `"Error"` 처리
- 입력값 초기화 (`AC`), 현재 항목만 삭제 (`C`), 부호 전환 (`±`)
- 후위 표기법 변환 알고리즘 (Shunting Yard)
- 스택 기반 수식 계산기 (`evaluate_postfix()`)

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
