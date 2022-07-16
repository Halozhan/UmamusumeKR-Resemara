# 우마뾰이하는 리세마라 매크로
우마뾰이 우마뾰이

## Installation
[Python 다운로드](https://www.python.org/) 및 설치  
프로젝트 폴더에서 cmd를 열어서 옆의 명령어 실행
```bash
python moduleInstaller.py
```

[ADB 다운로드](https://developer.android.com/studio/releases/platform-tools) 및 platform-tools 이름으로 압축풀기

## Initialization

### 공통
Instances example.txt 파일을 복제하여 Instances.txt 이름으로 변경  
Instances example.txt 파일을 참고하여 윈도우 이름과 ADB 포트를 각각 적어주고 저장합니다.

### 블루스택 설정
#### 퍼포먼스
CPU 설정: 낮음 (1 코어)  
메모리 설정: 중간 (2 GB)  
성능 모드: 고성능  
프레임 속도: 30 (25까진 괜찮을 듯, 그 이하는 느림)  

#### 디스플레이
화면 해상도: 세로모드, 540 x 960 해상도  
화소 밀도: 160 DPI(낮음)

#### 단축키
모두 다 지우고 "최근 앱"만 ScrlLock 키로 변경

#### 고급 기능 설정
안드로이드 디버그 브리지(ADB) 활성화 및 127.0.0.1:XXXX 뒤에 포트 번호를 위의 Instance.txt 파일에 기입

#### 우마무스메
플레이 스토어에서 다운받고 각 인스턴스마다 데이터 삭제 권장

#### Firefox
플레이 스토어에서 [Firefox: 빠르고 안전한 사생활 보호 웹 브라우저]를 다운로드  
플러그인 추가해서 프록시 연결 권장.  
프록시를 사용해 호스트의 아이피가 바뀌더라도 IP 변경으로 인한 카카오 계정 페이지의 로그아웃을 방지함


### MAC 주소 초기화

#### MANUAL 버전 (그 이외 공유기)
IP로 인한 횟수 제한이 감지되면 자동으로 매크로가 멈추니 수동으로 MAC 주소를 변경 후 시작을 눌러주세요.

#### ASUS 공유기 MAC 주소 변경 (공유기)
ASUS_ROUTER_CONFIG example.py 파일을 복제하여 ASUS_ROUTER_CONFIG.py 이름으로 변경  
GATEWAY 주소와 ID, PW를 입력하고 저장

#### Technitium MAC Address Changer 버전 (모뎀 직렬 연결)
[Technitium MAC Address Changer 다운로드](https://technitium.com/tmac/) 및 설치  
PyAutoGui 모듈을 사용하기 때문에 윈도우 활성 클릭을 하므로 항상 프로그램을 (우측 상단에) 띄워두고 사용합니다.


## Usage
run.bat 파일 실행 후  
우마뾰이 창이 열리면 탭 1~10으로 이동해 각각 인스턴스의 설정을 해준다.  
추가로 Main 탭에서 CPU 성능에 맞게 속도를 조절해줄 수 있다.


## Contributing
풀 리퀘스트 및 이슈 지적 환영


## License
[MIT](https://choosealicense.com/licenses/mit/)