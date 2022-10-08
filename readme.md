# ni sensor read
ni daqmx 에서 데이터를 획득하여 csv 형태로 저장하는 프로그램입니다.
저장할 장치, 채널, 샘플링레이트, 파일명 을 입력하면 채널마다 파일이 생성 됩니다.
사용의 편의 성을 위해 우선 cli 형태로 제작 되었으며 추후 명령어 기반으로 개선할 예정 입니다.

## how to use
dist 디렉토리에 존재하는 ni.exe 를 실행 하시면 됩니다.
종료 하실때에는 cntl+c 를 누르면 안전하게 종료됩니다.

## build
pyinstaller 를 사용하여 exe 파일을 제작 하였기 때문에
```pyinstaller ni.spec```
```pyinstaller ni.py -F --copy-metadata nidaqmx --collect-all pyfiglet```
명령어를 이용하시면 빌드가 가능합니다.
