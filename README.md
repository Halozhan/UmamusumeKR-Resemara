# 우마뾰이하는 리세마라 매크로
![우마뾰이](umapyoi.gif)


# Installation
1. [Python 다운로드](https://www.python.org/) 및 설치  
2. [ADB 다운로드](https://developer.android.com/studio/releases/platform-tools) 및 platform-tools 이름으로 압축풀기


# Initialization

## 공통
윈도우 화면 및 절전에서 화면 끄기와 절전 상태로 전환을 안 함으로 변경 필수(실제 모니터 전원은 꺼도 됨)  
```Instances example.txt``` 파일을 복제하여 ```Instances.txt``` 이름으로 변경  
```Instances example.txt``` 파일을 참고하여 윈도우 이름과 ADB 포트를 각각 적어주고 저장합니다.

## 블루스택 설정

### 퍼포먼스
```
CPU 설정: 중간 (2 코어)  
메모리 설정: 중간 (2 GB)  
성능 모드: 고성능  
프레임 속도: 30 (25까진 괜찮을 듯, 그 이하는 느림)  
```

### 디스플레이
```
화면 해상도: 세로모드, 540 x 960 해상도  
화소 밀도: 160 DPI(낮음)
```

### 고급 기능 설정
안드로이드 디버그 브리지(ADB) 활성화 및 127.0.0.1:```XXXX``` 뒤에 포트 번호를 위의 ```Instance.txt``` 파일에 기입

### 우마무스메
플레이 스토어에서 다운받고 복사한 인스턴스마다 데이터 삭제 권장


# Usage
```run.bat``` 파일 실행 후  
우마뾰이 창이 열리면 탭 1~10으로 이동해 각각 인스턴스의 설정을 해준다.  
추가로 Main 탭에서 CPU 성능에 맞게 속도를 조절해줄 수 있다.


# Contributing
풀 리퀘스트 및 이슈 지적 환영


# License
[MIT](https://choosealicense.com/licenses/mit/)