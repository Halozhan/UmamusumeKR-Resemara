# pip install pure-python-adb
from ast import arg
import WindowsAPIInput
import adbInput
from OpenCV_imread import imreadUnicode
from ImageSearch import ImageSearch
from ImageSearch import screenshotToOpenCVImg
import time
import argparse
from datetime import datetime
from threading import Thread, Event


# 찾을 이미지
우마무스메_실행 = imreadUnicode(r"./Images/우마무스메_실행.png")
게스트_로그인 = imreadUnicode(r"./Images/게스트_로그인.png")
게스트로_로그인_하시겠습니까 = imreadUnicode(r"./Images/게스트로_로그인_하시겠습니까.png")
전체_동의 = imreadUnicode(r"./Images/전체_동의.png")
시작하기 = imreadUnicode(r"./Images/시작하기.png")
TAP_TO_START = imreadUnicode(r"./Images/TAP_TO_START.png")
계정_연동_설정_요청 = imreadUnicode(r"./Images/계정_연동_설정_요청.png")
게임_데이터_다운로드 = imreadUnicode(r"./Images/게임_데이터_다운로드.png")
SKIP = imreadUnicode(r"./Images/SKIP.png")
출전 = imreadUnicode(r"./Images/출전.png")
울려라_팡파레 = imreadUnicode(r"./Images/울려라_팡파레.png")
닿아라_골까지 = imreadUnicode(r"./Images/닿아라_골까지.png")
라이브_메뉴 = imreadUnicode(r"./Images/라이브_메뉴.png")
라이브_스킵 = imreadUnicode(r"./Images/라이브_스킵.png")
타즈나_씨와_레이스를_관전한 = imreadUnicode(r"./Images/타즈나_씨와_레이스를_관전한.png")
일본_우마무스메_트레이닝_센터_학원 = imreadUnicode(r"./Images/일본_우마무스메_트레이닝_센터_학원.png")
레이스의_세계를_꿈꾸는_아이들이 = imreadUnicode(r"./Images/레이스의_세계를_꿈꾸는_아이들이.png")
환영 = imreadUnicode(r"./Images/환영.png")
느낌표물음표 = imreadUnicode(r"./Images/느낌표물음표.png")
아키카와_이사장님 = imreadUnicode(r"./Images/아키카와_이사장님.png")
장래_유망한_트레이너의_등장에 = imreadUnicode(r"./Images/장래_유망한_트레이너의_등장에.png")
나는_이_학원의_이사장 = imreadUnicode(r"./Images/나는_이_학원의_이사장.png")
자네에_대해_가르쳐_주게나 = imreadUnicode(r"./Images/자네에_대해_가르쳐_주게나.png")
트레이너_정보를_입력해주세요 = imreadUnicode(r"./Images/트레이너_정보를_입력해주세요.png")
등록한다 = imreadUnicode(r"./Images/등록한다.png")
이_내용으로_등록합니다_등록하시겠습니까 = imreadUnicode(r"./Images/이_내용으로_등록합니다_등록하시겠습니까.png")
자네는_트레센_학원의_일원일세 = imreadUnicode(r"./Images/자네는_트레센_학원의_일원일세.png")
담당_우마무스메와_함께 = imreadUnicode(r"./Images/담당_우마무스메와_함께.png")
학원에_다니는_우마무스메의 = imreadUnicode(r"./Images/학원에_다니는_우마무스메의.png")
자네는_트레이너로서_담당_우마무스메를 = imreadUnicode(r"./Images/자네는_트레이너로서_담당_우마무스메를.png")
가슴에_단_트레이너_배지에 = imreadUnicode(r"./Images/가슴에_단_트레이너_배지에.png")
실전_연수를_하러_가시죠 = imreadUnicode(r"./Images/실전_연수를_하러_가시죠.png")
프리티_더비_뽑기_5번_뽑기_무료 = imreadUnicode(r"./Images/프리티_더비_뽑기_5번_뽑기_무료.png")
튜토리얼_용_프리티_더비_뽑기 = imreadUnicode(r"./Images/튜토리얼_용_프리티_더비_뽑기.png")
서포트_카드_화살표 = imreadUnicode(r"./Images/서포트_카드_화살표.png")
서포트_카드_화살표2 = imreadUnicode(r"./Images/서포트_카드_화살표2.png")
서포트_카드_뽑기_10번_뽑기_무료 = imreadUnicode(r"./Images/서포트_카드_뽑기_10번_뽑기_무료.png")
튜토리얼_용_서포트_카드_뽑기 = imreadUnicode(r"./Images/튜토리얼_용_서포트_카드_뽑기.png")
육성_화살표 = imreadUnicode(r"./Images/육성_화살표.png")
육성_시나리오를_공략하자 = imreadUnicode(r"./Images/육성_시나리오를_공략하자.png")
다음_화살표 = imreadUnicode(r"./Images/다음_화살표.png")
트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자 = imreadUnicode(r"./Images/트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자.png")
마음에_드는_우마무스메를_육성하자 = imreadUnicode(r"./Images/마음에_드는_우마무스메를_육성하자.png")
다이와_스칼렛_클릭 = imreadUnicode(r"./Images/다이와_스칼렛_클릭.png")
다음_화살표_육성_우마무스메_선택 = imreadUnicode(r"./Images/다음_화살표_육성_우마무스메_선택.png")
플러스_계승_우마무스메_선택_화살표 = imreadUnicode(r"./Images/플러스_계승_우마무스메_선택_화살표.png")
계승_보드카_선택_화살표 = imreadUnicode(r"./Images/계승_보드카_선택_화살표.png")
보드카_결정_화살표 = imreadUnicode(r"./Images/보드카_결정_화살표.png")
자동_선택_화살표 = imreadUnicode(r"./Images/자동_선택_화살표.png")
자동_선택_확인_OK_화살표 = imreadUnicode(r"./Images/자동_선택_확인_OK_화살표.png")
마음을_이어서_꿈을_이루자 = imreadUnicode(r"./Images/마음을_이어서_꿈을_이루자.png")
계승_최종_다음_화살표 = imreadUnicode(r"./Images/계승_최종_다음_화살표.png")
서포트_카드를_편성해서_육성_효율_UP = imreadUnicode(r"./Images/서포트_카드를_편성해서_육성_효율_UP.png")
서포트_카드의_타입에_주목 = imreadUnicode(r"./Images/서포트_카드의_타입에_주목.png")
우정_트레이닝이_육성의_열쇠를_쥐고_있다 = imreadUnicode(r"./Images/우정_트레이닝이_육성의_열쇠를_쥐고_있다.png")
서포트_자동_편성_화살표 = imreadUnicode(r"./Images/서포트_자동_편성_화살표.png")
육성_시작_화살표 = imreadUnicode(r"./Images/육성_시작_화살표.png")
TP를_소비해_육성_시작_화살표 = imreadUnicode(r"./Images/TP를_소비해_육성_시작_화살표.png")
초록색_역삼각형 = imreadUnicode(r"./Images/초록색_역삼각형.png")
TAP = imreadUnicode(r"./Images/TAP.png")
우마무스메에겐_저마다_다른_목표가_있습니다 = imreadUnicode(r"./Images/우마무스메에겐_저마다_다른_목표가_있습니다.png")
이쪽은_육성을_진행할_때_필요한_커맨드입니다 = imreadUnicode(r"./Images/이쪽은_육성을_진행할_때_필요한_커맨드입니다.png")
커맨드를_하나_실행하면_턴을_소비합니다 = imreadUnicode(r"./Images/커맨드를_하나_실행하면_턴을_소비합니다.png")
우선_트레이닝을_선택해_보세요 = imreadUnicode(r"./Images/우선_트레이닝을_선택해_보세요.png")
이게_실행할_수_있는_트레이닝들입니다 = imreadUnicode(r"./Images/이게_실행할_수_있는_트레이닝들입니다.png")
한_번_스피드를_골라_보세요 = imreadUnicode(r"./Images/한_번_스피드를_골라_보세요.png")
파란색_역삼각형 = imreadUnicode(r"./Images/파란색_역삼각형.png")
약속 = imreadUnicode(r"./Images/약속.png")
서둘러_가봐 = imreadUnicode(r"./Images/서둘러_가봐.png")
그때_번뜩였다 = imreadUnicode(r"./Images/그때_번뜩였다.png")
다이와_스칼렛의_성장으로_이어졌다 = imreadUnicode(r"./Images/다이와_스칼렛의_성장으로_이어졌다.png")
다음으로_육성_우마무스메의_체력에_관해_설명할게요 = imreadUnicode(r"./Images/다음으로_육성_우마무스메의_체력에_관해_설명할게요.png")
우선_아까처럼_트레이닝을_선택해_보세요 = imreadUnicode(r"./Images/우선_아까처럼_트레이닝을_선택해_보세요.png")
여기_실패율에_주목해_주세요 = imreadUnicode(r"./Images/여기_실패율에_주목해_주세요.png")
남은_체력이_적을수록_실패율이_높아지게_돼요 = imreadUnicode(r"./Images/남은_체력이_적을수록_실패율이_높아지게_돼요.png")
트레이닝에_실패하면_능력과_컨디션이 = imreadUnicode(r"./Images/트레이닝에_실패하면_능력과_컨디션이.png")
돌아간다_화살표 = imreadUnicode(r"./Images/돌아간다_화살표.png")
체력이_적을_때는_우마무스메를 = imreadUnicode(r"./Images/체력이_적을_때는_우마무스메를.png")
먼저_여기_스킬을_선택해보세요 = imreadUnicode(r"./Images/먼저_여기_스킬을_선택해보세요.png")
다음으로_배울_스킬을_선택하세요 = imreadUnicode(r"./Images/다음으로_배울_스킬을_선택하세요.png")
이번에는_이_스킬을_습득해_보세요 = imreadUnicode(r"./Images/이번에는_이_스킬을_습득해_보세요.png")
스킬_결정_화살표 = imreadUnicode(r"./Images/스킬_결정_화살표.png")
스킬_획득_화살표 = imreadUnicode(r"./Images/스킬_획득_화살표.png")
스킬_획득_돌아간다_화살표 = imreadUnicode(r"./Images/스킬_획득_돌아간다_화살표.png")
이졔_준비가_다_끝났어요_레이스에_출전해_봐요 = imreadUnicode(r"./Images/이졔_준비가_다_끝났어요_레이스에_출전해_봐요.png")
출전_화살표 = imreadUnicode(r"./Images/출전_화살표.png")
_1등이_되기_위해서도_말야 = imreadUnicode(r"./Images/_1등이_되기_위해서도_말야.png")
패덕에서는_레이스에_출전하는_우마무스메의 = imreadUnicode(r"./Images/패덕에서는_레이스에_출전하는_우마무스메의.png")
우선_예상_표시에_관해서_설명할게요 = imreadUnicode(r"./Images/우선_예상_표시에_관해서_설명할게요.png")
_3개의_표시는_전문가들의_예상을_나타내며 = imreadUnicode(r"./Images/_3개의_표시는_전문가들의_예상을_나타내며.png")
능력과_컨디션이_좋을수록_많은_기대를_받게_돼서 = imreadUnicode(r"./Images/능력과_컨디션이_좋을수록_많은_기대를_받게_돼서.png")
물론_반드시_우승하게_되는_건_아니지만 = imreadUnicode(r"./Images/물론_반드시_우승하게_되는_건_아니지만.png")
또_패덕에서는_우마무스메의_작전을 = imreadUnicode(r"./Images/또_패덕에서는_우마무스메의_작전을.png")
선행A_화살표 = imreadUnicode(r"./Images/선행A_화살표.png")
작전_결정 = imreadUnicode(r"./Images/작전_결정.png")
이것으로_준비는_다_됐어요 = imreadUnicode(r"./Images/이것으로_준비는_다_됐어요.png")
첫_우승_축하_드려요 = imreadUnicode(r"./Images/첫_우승_축하_드려요.png")
좋아 = imreadUnicode(r"./Images/좋아.png")
목표_달성 = imreadUnicode(r"./Images/목표_달성.png")
육성_목표_달성 = imreadUnicode(r"./Images/육성_목표_달성.png")
육성_수고하셨습니다 = imreadUnicode(r"./Images/육성_수고하셨습니다.png")
스킬_포인트가_남았다면 = imreadUnicode(r"./Images/스킬_포인트가_남았다면.png")
육성은_이것으로_종료입니다 = imreadUnicode(r"./Images/육성은_이것으로_종료입니다.png")
또_연수_기간은_짧았지만 = imreadUnicode(r"./Images/또_연수_기간은_짧았지만.png")
육성_완료_화살표 = imreadUnicode(r"./Images/육성_완료_화살표.png")
육성_완료_확인_완료한다_화살표 = imreadUnicode(r"./Images/육성_완료_확인_완료한다_화살표.png")
육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후 = imreadUnicode(r"./Images/육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후.png")
최고_랭크를_목표로_힘내세요 = imreadUnicode(r"./Images/최고_랭크를_목표로_힘내세요.png")
랭크_육성 = imreadUnicode(r"./Images/랭크_육성.png")
육성을_끝낸_우마무스메는_인자를 = imreadUnicode(r"./Images/육성을_끝낸_우마무스메는_인자를.png")
계승_우마무스메로_선택하면_새로운_우마무스메에게 = imreadUnicode(r"./Images/계승_우마무스메로_선택하면_새로운_우마무스메에게.png")
인자획득 = imreadUnicode(r"./Images/인자획득.png")
우마무스메_상세_닫기_화살표 = imreadUnicode(r"./Images/우마무스메_상세_닫기_화살표.png")
평가점 = imreadUnicode(r"./Images/평가점.png")
보상획득 = imreadUnicode(r"./Images/보상획득.png")
강화_편성_화살표 = imreadUnicode(r"./Images/강화_편성_화살표.png")
레이스_화살표 = imreadUnicode(r"./Images/레이스_화살표.png")
팀_경기장_화살표 = imreadUnicode(r"./Images/팀_경기장_화살표.png")
오리지널_팀을_결성_상위_CLASS를_노려라 = imreadUnicode(r"./Images/오리지널_팀을_결성_상위_CLASS를_노려라.png")
하이스코어를_기록해서_CLASS_승급을_노리자 = imreadUnicode(r"./Images/하이스코어를_기록해서_CLASS_승급을_노리자.png")
기간_중에_개최되는_5개의_레이스에 = imreadUnicode(r"./Images/기간_중에_개최되는_5개의_레이스에.png")
서포트_카드의_Lv을_UP해서 = imreadUnicode(r"./Images/서포트_카드의_Lv을_UP해서.png")
팀_편성 = imreadUnicode(r"./Images/팀_편성.png")
전당_입성_우마무스메로_자신만의_팀을_결성 = imreadUnicode(r"./Images/전당_입성_우마무스메로_자신만의_팀을_결성.png")
팀_랭크를_올려서_최강의_팀이_되자 = imreadUnicode(r"./Images/팀_랭크를_올려서_최강의_팀이_되자.png")
팀_평가를_높이는_것이_팀_경기짱을_공략하는_열쇠 = imreadUnicode(r"./Images/팀_평가를_높이는_것이_팀_경기짱을_공략하는_열쇠.png")
팀_편성_다이와_스칼렛_화살표_클릭 = imreadUnicode(r"./Images/팀_편성_다이와_스칼렛_화살표_클릭.png")
출전_우마무스메_선택_다이와_스칼렛_화살표 = imreadUnicode(r"./Images/출전_우마무스메_선택_다이와_스칼렛_화살표.png")
팀_편성_확정_화살표 = imreadUnicode(r"./Images/팀_편성_확정_화살표.png")
편성을_확정합니다_진행하시겠습니까 = imreadUnicode(r"./Images/편성을_확정합니다_진행하시겠습니까.png")
팀_최고_평가점_갱신_닫기 = imreadUnicode(r"./Images/팀_최고_평가점_갱신_닫기.png")
홈_화살표 = imreadUnicode(r"./Images/홈_화살표.png")
공지사항_X = imreadUnicode(r"./Images/공지사항_X.png")
메인_스토리가_해방되었습니다 = imreadUnicode(r"./Images/메인_스토리가_해방되었습니다.png")
여러_스토리를_해방할_수_있게_되었습니다 = imreadUnicode(r"./Images/여러_스토리를_해방할_수_있게_되었습니다.png")


# 가챠
선물_이동 = imreadUnicode(r"./Images/선물_이동.png")
선물_일괄_수령 = imreadUnicode(r"./Images/선물_일괄_수령.png")
상기의_선물을_수령했습니다 = imreadUnicode(r"./Images/상기의_선물을_수령했습니다.png")
받을_수_있는_선물이_없습니다 = imreadUnicode(r"./Images/받을_수_있는_선물이_없습니다.png")
뽑기_이동 = imreadUnicode(r"./Images/뽑기_이동.png")
프리티_더비_뽑기 = imreadUnicode(r"./Images/프리티_더비_뽑기.png")
서포트_카드_뽑기 = imreadUnicode(r"./Images/서포트_카드_뽑기.png")
무료_쥬얼부터_먼저_사용됩니다 = imreadUnicode(r"./Images/무료_쥬얼부터_먼저_사용됩니다.png")
뽑기_결과 = imreadUnicode(r"./Images/뽑기_결과.png")
한_번_더_뽑기 = imreadUnicode(r"./Images/한_번_더_뽑기.png")
쥬얼이_부족합니다 = imreadUnicode(r"./Images/쥬얼이_부족합니다.png")
상점_화면을_표시할_수_없습니다 = imreadUnicode(r"./Images/상점_화면을_표시할_수_없습니다.png")


# 연동하기
메뉴 = imreadUnicode(r"./Images/메뉴.png")
메뉴_단축 = imreadUnicode(r"./Images/메뉴_단축.png")
계정_정보 = imreadUnicode(r"./Images/계정_정보.png")
카카오_로그인 = imreadUnicode(r"./Images/카카오_로그인.png")
확인하고_계속하기 = imreadUnicode(r"./Images/확인하고_계속하기.png")
확인하고_계속하기2 = imreadUnicode(r"./Images/확인하고_계속하기2.png")
확인하고_계속하기3 = imreadUnicode(r"./Images/확인하고_계속하기3.png")
계속하기 = imreadUnicode(r"./Images/계속하기.png")
정보_확인_중 = imreadUnicode(r"./Images/정보_확인_중.png")
Google_계정으로_로그인 = imreadUnicode(r"./Images/Google_계정으로_로그인.png")
인증되지_않는_로그인_방법_입니다 = imreadUnicode(r"./Images/인증되지_않는_로그인_방법_입니다.png")
카카오_로그인_연동에_성공하였습니다 = imreadUnicode(r"./Images/카카오_로그인_연동에_성공하였습니다.png")
로그아웃 = imreadUnicode(r"./Images/로그아웃.png")


# 초기화
모두_지우기 = imreadUnicode(r"./Images/모두_지우기.png")
크롬_실행 = imreadUnicode(r"./Images/크롬_실행.png")
크롬_실행2 = imreadUnicode(r"./Images/크롬_실행2.png")
연결된_서비스_관리 = imreadUnicode(r"./Images/연결된_서비스_관리.png")
우마무스메_서비스 = imreadUnicode(r"./Images/우마무스메_서비스.png")
모든_정보_삭제 = imreadUnicode(r"./Images/모든_정보_삭제.png")
이_서비스의_모든_정보를_삭제하시겠습니까 = imreadUnicode(r"./Images/이_서비스의_모든_정보를_삭제하시겠습니까.png")
이_서비스의_모든_정보를_삭제하시겠습니까2 = imreadUnicode(r"./Images/이_서비스의_모든_정보를_삭제하시겠습니까2.png")
모든_정보_삭제_빨간_박스 = imreadUnicode(r"./Images/모든_정보_삭제_빨간_박스.png")
비밀번호 = imreadUnicode(r"./Images/비밀번호.png")
자동완성_Continue = imreadUnicode(r"./Images/자동완성_Continue.png")
자동완성_계속 = imreadUnicode(r"./Images/자동완성_계속.png")
비밀번호_확인 = imreadUnicode(r"./Images/비밀번호_확인.png")
삭제_완료 = imreadUnicode(r"./Images/삭제_완료.png")


# 특수 이벤트
튜토리얼을_스킵하시겠습니까 = imreadUnicode(r"./Images/튜토리얼을_스킵하시겠습니까.png")
타이틀_화면으로 = imreadUnicode(r"./Images/타이틀_화면으로.png")
_2단계_인증 = imreadUnicode(r"./Images/_2단계_인증.png")
확인 = imreadUnicode(r"./Images/확인.png")
앱_닫기 = imreadUnicode(r"./Images/앱_닫기.png")
날짜가_변경됐습니다 = imreadUnicode(r"./Images/날짜가_변경됐습니다.png")
추가_데이터를_다운로드합니다 = imreadUnicode(r"./Images/추가_데이터를_다운로드합니다.png")


# 서포트 카드
SR_스윕_토쇼 = imreadUnicode(r"./Supporter_cards/SR_스윕_토쇼.png")
SSR_골드_쉽 = imreadUnicode(r"./Supporter_cards/SSR_골드_쉽.png")
SSR_골드_시티 = imreadUnicode(r"./Supporter_cards/SSR_골드_시티.png")
SSR_그래스_원더 = imreadUnicode(r"./Supporter_cards/SSR_그래스_원더.png")
SSR_니시노_플라워 = imreadUnicode(r"./Supporter_cards/SSR_니시노_플라워.png")
SSR_보드카 = imreadUnicode(r"./Supporter_cards/SSR_보드카.png")
SSR_비코_페가수스 = imreadUnicode(r"./Supporter_cards/SSR_비코_페가수스.png")
SSR_사일런스_스즈카 = imreadUnicode(r"./Supporter_cards/SSR_사일런스_스즈카.png")
SSR_사쿠라_바쿠신_오 = imreadUnicode(r"./Supporter_cards/SSR_사쿠라_바쿠신_오.png")
SSR_세이운_스카이 = imreadUnicode(r"./Supporter_cards/SSR_세이운_스카이.png")
SSR_슈퍼_크릭 = imreadUnicode(r"./Supporter_cards/SSR_슈퍼_크릭.png")
SSR_스마트_팔콘 = imreadUnicode(r"./Supporter_cards/SSR_스마트_팔콘.png")
SSR_스페셜_위크 = imreadUnicode(r"./Supporter_cards/SSR_스페셜_위크.png")
SSR_아이네스_후진 = imreadUnicode(r"./Supporter_cards/SSR_아이네스_후진.png")
SSR_에어_샤커 = imreadUnicode(r"./Supporter_cards/SSR_에어_샤커.png")
SSR_엘_콘도르_파사 = imreadUnicode(r"./Supporter_cards/SSR_엘_콘도르_파사.png")
SSR_오구리_캡 = imreadUnicode(r"./Supporter_cards/SSR_오구리_캡.png")
SSR_위닝_티켓 = imreadUnicode(r"./Supporter_cards/SSR_위닝_티켓.png")
SSR_타마모_크로스 = imreadUnicode(r"./Supporter_cards/SSR_타마모_크로스.png")
SSR_토카이_테이오 = imreadUnicode(r"./Supporter_cards/SSR_토카이_테이오.png")
SSR_트윈_터보 = imreadUnicode(r"./Supporter_cards/SSR_트윈_터보.png")
SSR_파인_모션 = imreadUnicode(r"./Supporter_cards/SSR_파인_모션.png")
SSR_하야카와_타즈나 = imreadUnicode(r"./Supporter_cards/SSR_하야카와_타즈나.png")







class Umamusume:
    def __init__(self, InstanceName, InstancePort, isDoneTutorial, output):
        self.InstanceName = InstanceName
        self.InstancePort = InstancePort
        self.GlobalisDoneTutorial = isDoneTutorial # 미리 튜토리얼 진행했으면 활성화하는게 작업 성능이 빨라짐
        self.output = output
        self.isAlive = False
        
        print(self.InstanceName, self.InstancePort, self.GlobalisDoneTutorial)
        
        self.resetCount = 0
        # Thread.__init__(self)
            
        
    def start(self):
        self.isAlive = True
        self.th = Thread(target=self.thread, daemon=True)
        self.th.start()
        
    def stop(self):
        self.isAlive = False
    
    def thread(self):
        while self.isAlive:
            isSuccessed = self.main(self.InstanceName, self.InstancePort, self.GlobalisDoneTutorial)
            print("-"*50)
            now = datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S"))
            print("튜토리얼 스킵 여부:", self.GlobalisDoneTutorial)
            if isSuccessed == "Failed":
                self.resetCount += 1
            if isSuccessed == "Stop":
                print("This thread was terminated.")
            print("리세 횟수:", self.resetCount)
            print("-"*50)
            if isSuccessed == True:
                break
            
        print("리세 종료")
        
    def main(self, InstanceName="BlueStacks Dev", InstancePort=6205, isDoneTutorial=True):
        hwndMain = WindowsAPIInput.GetHwnd(InstanceName) # hwnd ID 찾기
        WindowsAPIInput.SetWindowSize(hwndMain, 574, 994)
        instancePort = InstancePort
        device = adbInput.AdbConnect(instancePort)
        isPAUSED = False
        is뽑기_이동 = True
        is뽑기_결과 = True
        is쥬얼부족 = False
        is연동하기 = False
        is초기화하기 = False
        updateTime = time.time() # 타임 아웃 터치
        
        # 서포트 카드 총 갯수
        SR_스윕_토쇼_total = 0
        SSR_골드_쉽_total = 0
        SSR_골드_시티_total = 0
        SSR_그래스_원더_total = 0
        SSR_니시노_플라워_total = 0
        SSR_보드카_total = 0
        SSR_비코_페가수스_total = 0
        SSR_사일런스_스즈카_total = 0
        SSR_사쿠라_바쿠신_오_total = 0
        SSR_세이운_스카이_total = 0
        SSR_슈퍼_크릭_total = 0
        SSR_스마트_팔콘_total = 0
        SSR_스페셜_위크_total = 0
        SSR_아이네스_후진_total = 0
        SSR_에어_샤커_total = 0
        SSR_엘_콘도르_파사_total = 0
        SSR_오구리_캡_total = 0
        SSR_위닝_티켓_total = 0
        SSR_타마모_크로스_total = 0
        SSR_토카이_테이오_total = 0
        SSR_트윈_터보_total = 0
        SSR_파인_모션_total = 0
        SSR_하야카와_타즈나_total = 0
        
        
        while self.isAlive:
            
            # 잠수 클릭 20초 터치락 해제
            if isDoneTutorial and time.time() >= updateTime + 20:
                print("20초 정지 터치락 해제!!! "*3)
                adbInput.BlueStacksClick(device=device, position=(0,0,0,0))
                time.sleep(2)
            
            # 잠수 클릭 40초 이상 앱정지
            if isDoneTutorial and time.time() >= updateTime + 40:
                print("40초 정지 앱 강제종료!!! "*3)
                WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_SCROLL)
                time.sleep(2)
                
            
            img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
            
            count = 0
            count, position = ImageSearch(img, 우마무스메_실행, confidence=0.99, grayscale=False)
            if count and is초기화하기 == False:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0])
                print("우마무스메_실행 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                continue
            
            count = 0
            count, position = ImageSearch(img, 게스트_로그인, 232, 926, 77, 14)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("게스트_로그인 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                continue
            
            count = 0
            count, position = ImageSearch(img, 게스트로_로그인_하시겠습니까, 162, 534, 218, 17, confidence = 0.9)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX = 120, offsetY = 117, deltaX=5, deltaY=5)
                print("게스트로_로그인_하시겠습니까 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                continue
            
            count = 0
            count, position = ImageSearch(img, 전체_동의, 23, 117, 22, 22, confidence=0.95, grayscale=False)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX = 0, offsetY = 0, deltaX=5, deltaY=5)
                print("전체_동의 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                continue
                
            count = 0
            count, position = ImageSearch(img, 시작하기, 237, 396, 67, 23, grayscale=False)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("시작하기 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                continue
                
            count = 0
            count, position = ImageSearch(img, TAP_TO_START, 150, 860, 241, 34)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("TAP_TO_START " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                continue
                
            count = 0
            count, position = ImageSearch(img, 계정_연동_설정_요청, 176, 327, 186, 29)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX = -121, offsetY = 316, deltaX=5, deltaY=5)
                print("계정_연동_설정_요청 " + str(count) + "개")
                print(position)
                time.sleep(2) # 빨리 터치하면 튜토리얼 하기 부분에서도 같은 부분 클릭해버림
                continue
            
            count = 0
            count, position = ImageSearch(img, 게임_데이터_다운로드, 170, 329, 200, 27)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX = 132, offsetY = 316, deltaX=5, deltaY=5)
                print("게임_데이터_다운로드 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                continue
            
            count = 0
            count, position = ImageSearch(img, SKIP, confidence=0.85)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("SKIP " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                continue
            
            count = 0
            count, position = ImageSearch(img, 트레이너_정보를_입력해주세요)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetY=61, deltaX=5)
                time.sleep(0.5)
                adbInput.BlueStacksClick(device=device, position=position[0], offsetY=555, deltaX=5)
                print("트레이너_정보를_입력해주세요 " + str(count) + "개")
                time.sleep(0.2)
                print(position)
                for _ in range(10):
                    WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_BACK)
                time.sleep(0.2)
                WindowsAPIInput.WindowsAPIKeyboardInputString(hwndMain, "UmaPyoi")
                time.sleep(0.5)
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
            
            count = 0
            count, position = ImageSearch(img, 등록한다, 206, 620, 106, 52)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("등록한다 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                continue

            count = 0
            count, position = ImageSearch(img, 이_내용으로_등록합니다_등록하시겠습니까, 72, 569, 333, 49)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX=136, offsetY=54, deltaX=5, deltaY=5)
                print("이_내용으로_등록합니다_등록하시겠습니까 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                continue
                
            if isDoneTutorial == False: # 튜토리얼 진행, 귀찮아서 튜토리얼 멈추면 알아서 하셈
                updateTime = time.time()
                
                count = 0
                count, position = ImageSearch(img, 출전)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("출전 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 울려라_팡파레)
                if count and isPAUSED == False:
                    ConvertedPosition = []
                    ConvertedPosition.append(position[0][0] / 1.750503018108652) # 1740 / 994 가로화면 가로배율
                    ConvertedPosition.append(position[0][1] / 1.750503018108652)
                    ConvertedPosition.append(position[0][2] / 1.729965156794425) # 993 / 574 가로화면 세로배율
                    ConvertedPosition.append(position[0][3] / 1.729965156794425)
                    adbInput.BlueStacksClick(device=device, position=ConvertedPosition, deltaX=5, deltaY=5)
                    print("울려라_팡파레 " + str(count) + "개")
                    print(position)
                    isPAUSED = True
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 닿아라_골까지)
                if count and isPAUSED == False:
                    ConvertedPosition = []
                    ConvertedPosition.append(position[0][0] / 1.750503018108652)
                    ConvertedPosition.append(position[0][1] / 1.750503018108652)
                    ConvertedPosition.append(position[0][2] / 1.729965156794425)
                    ConvertedPosition.append(position[0][3] / 1.729965156794425)
                    adbInput.BlueStacksClick(device=device, position=ConvertedPosition, deltaX=5, deltaY=5)
                    print("닿아라_골까지 " + str(count) + "개")
                    print(position)
                    isPAUSED = True
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 라이브_메뉴)
                if count:
                    ConvertedPosition = []
                    ConvertedPosition.append(position[0][0] / 1.750503018108652)
                    ConvertedPosition.append(position[0][1] / 1.750503018108652)
                    ConvertedPosition.append(position[0][2] / 1.729965156794425)
                    ConvertedPosition.append(position[0][3] / 1.729965156794425)
                    adbInput.BlueStacksClick(device=device, position=ConvertedPosition, deltaX=5, deltaY=5)
                    print("라이브_메뉴 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 라이브_스킵)
                if count:
                    ConvertedPosition = []
                    ConvertedPosition.append(position[0][0] / 1.750503018108652)
                    ConvertedPosition.append(position[0][1] / 1.750503018108652)
                    ConvertedPosition.append(position[0][2] / 1.729965156794425)
                    ConvertedPosition.append(position[0][3] / 1.729965156794425)
                    adbInput.BlueStacksClick(device=device, position=ConvertedPosition, deltaX=5, deltaY=5)
                    print("라이브_스킵 " + str(count) + "개")
                    print(position)
                    isPAUSED = False
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 타즈나_씨와_레이스를_관전한, 124, 808, 268, 52)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("타즈나_씨와_레이스를_관전한 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 일본_우마무스메_트레이닝_센터_학원, 78, 844, 345, 53)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("일본_우마무스메_트레이닝_센터_학원 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 레이스의_세계를_꿈꾸는_아이들이, 73, 810, 369, 70)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("레이스의_세계를_꿈꾸는_아이들이 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 환영, 180, 811, 156, 68)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("환영 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 느낌표물음표, 35, 449, 52, 54)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("느낌표물음표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 아키카와_이사장님, 181, 811, 181, 49)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("아키카와_이사장님 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 장래_유망한_트레이너의_등장에, 145, 808, 284, 50)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("장래_유망한_트레이너의_등장에 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 나는_이_학원의_이사장, 98, 821, 209, 49)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("나는_이_학원의_이사장 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 자네에_대해_가르쳐_주게나, 155, 833, 250, 48)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("자네에_대해_가르쳐_주게나 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                # 트레이너 정보 입력 -----------
                # 위에 빼둠
                # -----------------------------
            
                count = 0
                count, position = ImageSearch(img, 자네는_트레센_학원의_일원일세, 150, 833, 282, 49)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("자네는_트레센_학원의_일원일세 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 담당_우마무스메와_함께, 172, 798, 224, 49)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("담당_우마무스메와_함께 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 학원에_다니는_우마무스메의, 86, 798, 259, 50)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("학원에_다니는_우마무스메의 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 자네는_트레이너로서_담당_우마무스메를, 79, 810, 358, 51)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("자네는_트레이너로서_담당_우마무스메를 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 가슴에_단_트레이너_배지에, 159, 811, 248, 48)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("가슴에_단_트레이너_배지에 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 실전_연수를_하러_가시죠, 207, 813, 224, 46)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("실전_연수를_하러_가시죠 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 프리티_더비_뽑기_5번_뽑기_무료, 191, 710, 135, 125)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("프리티_더비_뽑기_5번_뽑기_무료 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 튜토리얼_용_프리티_더비_뽑기, 130, 432, 258, 69)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=180, deltaX=5, deltaY=5)
                    print("튜토리얼_용_프리티_더비_뽑기 " + str(count) + "개")
                    print(position)
                    print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 서포트_카드_화살표, 410, 508, 124, 135)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("서포트_카드_화살표 " + str(count) + "개") # 느림
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 서포트_카드_화살표2, 410, 508, 124, 135)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("서포트_카드_화살표2 " + str(count) + "개") # 느림
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 서포트_카드_뽑기_10번_뽑기_무료)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("서포트_카드_뽑기_10번_뽑기_무료 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 튜토리얼_용_서포트_카드_뽑기, 124, 431, 266, 71)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=180, deltaX=5, deltaY=5)
                    print("튜토리얼_용_서포트_카드_뽑기 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 육성_화살표, 350, 712, 117, 172)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=50, deltaX=5, deltaY=5)
                    print("육성_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                
                # 이미지 바꿀 예정
                count = 0
                count, position = ImageSearch(img, 육성_시나리오를_공략하자, 59, 664, 399, 77)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=223, deltaX=5, deltaY=5)
                    print("육성_시나리오를_공략하자 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 다음_화살표, 195, 742, 120, 117)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("다음_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자, 53, 614, 414, 125)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=248, deltaX=5, deltaY=5)
                    print("트윙클_시리즈에_도전_우마무스메의_꿈을_이뤄주자 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 마음에_드는_우마무스메를_육성하자, 21, 670, 473, 71)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=217, deltaX=5, deltaY=5)
                    print("마음에_드는_우마무스메를_육성하자 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 다이와_스칼렛_클릭, 0, 496, 138, 138)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("다이와_스칼렛_클릭 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 다음_화살표_육성_우마무스메_선택, 212, 747, 91, 116)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("다음_화살표_육성_우마무스메_선택 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 플러스_계승_우마무스메_선택_화살표, 19, 520, 103, 152)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("플러스_계승_우마무스메_선택_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 계승_보드카_선택_화살표, 209, 496, 93, 161)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("계승_보드카_선택_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 보드카_결정_화살표, 213, 740, 90, 120)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("보드카_결정_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 자동_선택_화살표, 329, 668, 105, 105)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("자동_선택_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 자동_선택_확인_OK_화살표, 334, 559, 84, 117) # 느림
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("자동_선택_확인_OK_화살표 " + str(count) + "개")
                    print(position)
                    print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 마음을_이어서_꿈을_이루자, 73, 661, 371, 79)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=218, deltaX=5, deltaY=5)
                    print("마음을_이어서_꿈을_이루자 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 계승_최종_다음_화살표)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=35, deltaX=5, deltaY=5)
                    print("계승_최종_다음_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 서포트_카드를_편성해서_육성_효율_UP, 67, 615, 383, 120)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=247, deltaX=5, deltaY=5)
                    print("서포트_카드를_편성해서_육성_효율_UP " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 서포트_카드의_타입에_주목, 38, 662, 439, 69)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=225, deltaX=5, deltaY=5)
                    print("서포트_카드의_타입에_주목 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 우정_트레이닝이_육성의_열쇠를_쥐고_있다)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=212, deltaX=5, deltaY=5)
                    print("우정_트레이닝이_육성의_열쇠를_쥐고_있다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 서포트_자동_편성_화살표, 324, 629, 107, 102)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("서포트_자동_편성_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 육성_시작_화살표, 184, 732, 160, 129)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("육성_시작_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, TP를_소비해_육성_시작_화살표, 305, 816, 142, 119)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("TP를_소비해_육성_시작_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 초록색_역삼각형, confidence=0.95) # 역 삼각형
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("초록색_역삼각형 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                
                count = 0
                count, position = ImageSearch(img, TAP)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("TAP " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, TAP)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("TAP " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 우마무스메에겐_저마다_다른_목표가_있습니다)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("우마무스메에겐_저마다_다른_목표가_있습니다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 이쪽은_육성을_진행할_때_필요한_커맨드입니다)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("이쪽은_육성을_진행할_때_필요한_커맨드입니다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 커맨드를_하나_실행하면_턴을_소비합니다)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("커맨드를_하나_실행하면_턴을_소비합니다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 우선_트레이닝을_선택해_보세요)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetX=60, offsetY=178, deltaX=5, deltaY=5)
                    print("우선_트레이닝을_선택해_보세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 이게_실행할_수_있는_트레이닝들입니다)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("이게_실행할_수_있는_트레이닝들입니다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 한_번_스피드를_골라_보세요)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetX=-143, offsetY=228, deltaX=5, deltaY=5)
                    print("한_번_스피드를_골라_보세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 파란색_역삼각형, confidence=0.98) # 역 삼각형
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("파란색_역삼각형 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                
                count = 0
                count, position = ImageSearch(img, 약속, 38, 614, 80, 57)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("약속 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 서둘러_가봐, 38, 617, 132, 53)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("서둘러_가봐 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 그때_번뜩였다, 22, 740, 289, 102)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("그때_번뜩였다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 다이와_스칼렛의_성장으로_이어졌다, 23, 741, 328, 55)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("다이와_스칼렛의_성장으로_이어졌다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 다음으로_육성_우마무스메의_체력에_관해_설명할게요)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("다음으로_육성_우마무스메의_체력에_관해_설명할게요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 우선_아까처럼_트레이닝을_선택해_보세요)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetX=90, offsetY=173, deltaX=5, deltaY=5)
                    print("우선_아까처럼_트레이닝을_선택해_보세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 여기_실패율에_주목해_주세요)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("여기_실패율에_주목해_주세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 남은_체력이_적을수록_실패율이_높아지게_돼요)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("남은_체력이_적을수록_실패율이_높아지게_돼요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 트레이닝에_실패하면_능력과_컨디션이)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("트레이닝에_실패하면_능력과_컨디션이 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 돌아간다_화살표)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("돌아간다_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 체력이_적을_때는_우마무스메를)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetX=-125, offsetY=180, deltaX=5, deltaY=5)
                    print("체력이_적을_때는_우마무스메를 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 먼저_여기_스킬을_선택해보세요)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetX=-70, offsetY=170, deltaX=5, deltaY=5)
                    print("먼저_여기_스킬을_선택해보세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 다음으로_배울_스킬을_선택하세요)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("다음으로_배울_스킬을_선택하세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 이번에는_이_스킬을_습득해_보세요)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetX=273, offsetY=183, deltaX=5, deltaY=5)
                    print("이번에는_이_스킬을_습득해_보세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 스킬_결정_화살표)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("스킬_결정_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 스킬_획득_화살표)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("스킬_획득_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 스킬_획득_돌아간다_화살표, 1, 857, 100, 115)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("스킬_획득_돌아간다_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 이졔_준비가_다_끝났어요_레이스에_출전해_봐요, 85, 621, 191, 69)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetX=207, offsetY=168, deltaX=5, deltaY=5)
                    print("이졔_준비가_다_끝났어요_레이스에_출전해_봐요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 출전_화살표)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("출전_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, _1등이_되기_위해서도_말야, 37, 615, 252, 58)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("_1등이_되기_위해서도_말야 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 패덕에서는_레이스에_출전하는_우마무스메의)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("패덕에서는_레이스에_출전하는_우마무스메의 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 우선_예상_표시에_관해서_설명할게요)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("우선_예상_표시에_관해서_설명할게요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, _3개의_표시는_전문가들의_예상을_나타내며)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("_3개의_표시는_전문가들의_예상을_나타내며 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 능력과_컨디션이_좋을수록_많은_기대를_받게_돼서)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("능력과_컨디션이_좋을수록_많은_기대를_받게_돼서 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 물론_반드시_우승하게_되는_건_아니지만)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("물론_반드시_우승하게_되는_건_아니지만 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 또_패덕에서는_우마무스메의_작전을)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetX=210, offsetY=157, deltaX=5, deltaY=5)
                    print("또_패덕에서는_우마무스메의_작전을 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 선행A_화살표)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("선행A_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 작전_결정)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("작전_결정 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 이것으로_준비는_다_됐어요)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetX=145, offsetY=161, deltaX=5, deltaY=5)
                    print("이것으로_준비는_다_됐어요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 첫_우승_축하_드려요)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=847, deltaX=5, deltaY=5)
                    print("첫_우승_축하_드려요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 좋아, 37, 613, 80, 59)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("좋아 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 목표_달성, 114, 222, 293, 100)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=578, deltaX=5, deltaY=5)
                    print("목표_달성 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 육성_목표_달성, 31, 227, 469, 96)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=578, deltaX=5, deltaY=5)
                    print("육성_목표_달성 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 육성_수고하셨습니다)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("육성_수고하셨습니다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 스킬_포인트가_남았다면)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("스킬_포인트가_남았다면 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 육성은_이것으로_종료입니다)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("육성은_이것으로_종료입니다 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 또_연수_기간은_짧았지만)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("또_연수_기간은_짧았지만 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 육성_완료_화살표)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=40, deltaX=5, deltaY=5)
                    print("육성_완료_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 육성_완료_확인_완료한다_화살표)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("육성_완료_확인_완료한다_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("육성을_끝낸_우마무스메는_일정_기준으로_평가받은_후 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 최고_랭크를_목표로_힘내세요)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("최고_랭크를_목표로_힘내세요 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 랭크_육성)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=837, deltaX=5, deltaY=5)
                    print("랭크_육성 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 육성을_끝낸_우마무스메는_인자를)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("육성을_끝낸_우마무스메는_인자를 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 계승_우마무스메로_선택하면_새로운_우마무스메에게)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("계승_우마무스메로_선택하면_새로운_우마무스메에게 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 인자획득)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=829, deltaX=5, deltaY=5)
                    print("인자획득 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 우마무스메_상세_닫기_화살표)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("우마무스메_상세_닫기_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 평가점, 293, 327, 75, 50)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetX=-75, offsetY=552, deltaX=5, deltaY=5)
                    print("평가점 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 보상획득, 113, 21, 287, 103)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=834, deltaX=5, deltaY=5)
                    print("보상획득 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                count = 0
                count, position = ImageSearch(img, 강화_편성_화살표, 0, 854, -1, -1, grayscale=False) # [(18, 879, 72, 102)]
                                                                                    # (-7, 854, 97, 127)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("강화_편성_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 레이스_화살표, 333, 842, -1, -1) # [(358, 867, 74, 111)]
                                                                                    # (333, 842, 99, 136)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("레이스_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 팀_경기장_화살표, 82, 542, 130, 83)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=50, deltaX=5, deltaY=5)
                    print("팀_경기장_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 오리지널_팀을_결성_상위_CLASS를_노려라, 81, 622, 358, 118)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=244, deltaX=5, deltaY=5)
                    print("오리지널_팀을_결성_상위_CLASS를_노려라 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 하이스코어를_기록해서_CLASS_승급을_노리자, 78, 614, 362, 125)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=250, deltaX=5, deltaY=5)
                    print("하이스코어를_기록해서_CLASS_승급을_노리자 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 기간_중에_개최되는_5개의_레이스에, 8, 617, 504, 121)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=236, deltaX=5, deltaY=5)
                    print("기간_중에_개최되는_5개의_레이스에 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 서포트_카드의_Lv을_UP해서, 61, 630, 396, 111)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=244, deltaX=5, deltaY=5)
                    print("서포트_카드의_Lv을_UP해서 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 팀_편성, 264, 699, 126, 72)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                    print("팀_편성 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 전당_입성_우마무스메로_자신만의_팀을_결성, 59, 616, 395, 122)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=247, deltaX=5, deltaY=5)
                    print("전당_입성_우마무스메로_자신만의_팀을_결성 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 팀_랭크를_올려서_최강의_팀이_되자, 128, 616, 262, 122)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=238, deltaX=5, deltaY=5)
                    print("팀_랭크를_올려서_최강의_팀이_되자 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 팀_평가를_높이는_것이_팀_경기짱을_공략하는_열쇠, 84, 619, 352, 123)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=246, deltaX=5, deltaY=5)
                    print("팀_평가를_높이는_것이_팀_경기짱을_공략하는_열쇠 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 팀_편성_다이와_스칼렛_화살표_클릭, 200, 341, 116, 160)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("팀_편성_다이와_스칼렛_화살표_클릭 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 출전_우마무스메_선택_다이와_스칼렛_화살표, 0, 591, 121, 138)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("출전_우마무스메_선택_다이와_스칼렛_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 팀_편성_확정_화살표, 190, 736, 136, 124)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("팀_편성_확정_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 편성을_확정합니다_진행하시겠습니까, 177, 524, 165, 75)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetX=121, offsetY=77, deltaX=5, deltaY=5)
                    print("편성을_확정합니다_진행하시겠습니까 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 팀_최고_평가점_갱신_닫기, 223, 840, 98, 95)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("팀_최고_평가점_갱신_닫기 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                    
                count = 0
                count, position = ImageSearch(img, 홈_화살표, 188, 845, 144, 134)
                if count:
                    adbInput.BlueStacksClick(device=device, position=position[0], offsetY=25, deltaX=5, deltaY=5)
                    print("홈_화살표 " + str(count) + "개")
                    print(position)
                    time.sleep(0.5)
                    continue
                
                
            # ------------------------------ 리세 -----------------------------    
            # ------------------------------ 리세 -----------------------------    
            # ------------------------------ 리세 -----------------------------    
            
            
            count = 0
            count, position = ImageSearch(img, 공지사항_X, 495, 52, 23, 22)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("공지사항_X " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
            
                
            count = 0
            count, position = ImageSearch(img, 메인_스토리가_해방되었습니다)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetY=90, deltaX=5, deltaY=5)
                print("메인_스토리가_해방되었습니다 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 여러_스토리를_해방할_수_있게_되었습니다)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetY=50, deltaX=5, deltaY=5)
                print("여러_스토리를_해방할_수_있게_되었습니다 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
            
            
            # 가챠
            count = 0
            count, position = ImageSearch(img, 선물_이동, 456, 672, 47, 53)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("선물_이동 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, 선물_일괄_수령, 319, 879, 115, 54, confidence=0.99, grayscale=False)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("선물_일괄_수령 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, 상기의_선물을_수령했습니다)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetY=50, deltaX=5, deltaY=5)
                print("상기의_선물을_수령했습니다 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, 받을_수_있는_선물이_없습니다, 143, 460, 231, 51)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX=-125, offsetY=420, deltaX=5, deltaY=5)
                print("받을_수_있는_선물이_없습니다 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, 뽑기_이동, 464, 666, 52, 62)
            if count and is뽑기_이동:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetY=245, deltaX=5, deltaY=5)
                print("뽑기_이동 " + str(count) + "개")
                print(position)
                time.sleep(1)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, 프리티_더비_뽑기, 154, 551, 175, 93, confidence=0.6)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX=254, deltaX=5, deltaY=5)
                print("프리티_더비_뽑기 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, 서포트_카드_뽑기, 160, 552, 154, 94, confidence=0.6)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX=196, offsetY=186, deltaX=5, deltaY=5)
                print("서포트_카드_뽑기 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, 무료_쥬얼부터_먼저_사용됩니다)
            if count:
                updateTime = time.time()
                is뽑기_결과 = True
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX=112, offsetY=55, deltaX=5, deltaY=5)
                print("무료_쥬얼부터_먼저_사용됩니다 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(1.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 뽑기_결과, 208, 48, 97, 47)
            if count and is뽑기_결과:
                updateTime = time.time()
                is뽑기_결과 = False
                print("뽑기_결과 " + str(count) + "개")
                print(position)
                
                SR_스윕_토쇼_count = 0
                SSR_골드_쉽_count = 0
                SSR_골드_시티_count = 0
                SSR_그래스_원더_count = 0
                SSR_니시노_플라워_count = 0
                SSR_보드카_count = 0
                SSR_비코_페가수스_count = 0
                SSR_사일런스_스즈카_count = 0
                SSR_사쿠라_바쿠신_오_count = 0
                SSR_세이운_스카이_count = 0
                SSR_슈퍼_크릭_count = 0
                SSR_스마트_팔콘_count = 0
                SSR_스페셜_위크_count = 0
                SSR_아이네스_후진_count = 0
                SSR_에어_샤커_count = 0
                SSR_엘_콘도르_파사_count = 0
                SSR_오구리_캡_count = 0
                SSR_위닝_티켓_count = 0
                SSR_타마모_크로스_count = 0
                SSR_토카이_테이오_count = 0
                SSR_트윈_터보_count = 0
                SSR_파인_모션_count = 0
                SSR_하야카와_타즈나_count = 0
                
                for i in range(3):
                    updateTime = time.time()
                    time.sleep(0.25)
                    img = screenshotToOpenCVImg(hwndMain)
                    
                    count = 0
                    count, position = ImageSearch(img, SR_스윕_토쇼, grayscale=False)
                    if count:
                        if SR_스윕_토쇼_count < count:
                            SR_스윕_토쇼_count = count
                        print("SR_스윕_토쇼 " + str(SR_스윕_토쇼_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_골드_쉽, grayscale=False)
                    if count:
                        if SSR_골드_쉽_count < count:
                            SSR_골드_쉽_count = count
                        print("SSR_골드_쉽 " + str(SSR_골드_쉽_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_골드_시티, grayscale=False)
                    if count:
                        if SSR_골드_시티_count < count:
                            SSR_골드_시티_count = count
                        print("SSR_골드_시티 " + str(SSR_골드_시티_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_그래스_원더, grayscale=False)
                    if count:
                        if SSR_그래스_원더_count < count:
                            SSR_그래스_원더_count = count
                        print("SSR_그래스_원더 " + str(SSR_그래스_원더_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_니시노_플라워, grayscale=False)
                    if count:
                        if SSR_니시노_플라워_count < count:
                            SSR_니시노_플라워_count = count
                        print("SSR_니시노_플라워 " + str(SSR_니시노_플라워_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_보드카, grayscale=False)
                    if count:
                        if SSR_보드카_count < count:
                            SSR_보드카_count = count
                        print("SSR_보드카 " + str(SSR_보드카_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_비코_페가수스, grayscale=False)
                    if count:
                        if SSR_비코_페가수스_count < count:
                            SSR_비코_페가수스_count = count
                        print("SSR_비코_페가수스 " + str(SSR_비코_페가수스_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_사일런스_스즈카, grayscale=False)
                    if count:
                        if SSR_사일런스_스즈카_count < count:
                            SSR_사일런스_스즈카_count = count
                        print("SSR_사일런스_스즈카 " + str(SSR_사일런스_스즈카_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_사쿠라_바쿠신_오, grayscale=False)
                    if count:
                        if SSR_사쿠라_바쿠신_오_count < count:
                            SSR_사쿠라_바쿠신_오_count = count
                        print("SSR_사쿠라_바쿠신_오 " + str(SSR_사쿠라_바쿠신_오_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_세이운_스카이, grayscale=False)
                    if count:
                        if SSR_세이운_스카이_count < count:
                            SSR_세이운_스카이_count = count
                        print("SSR_세이운_스카이 " + str(SSR_세이운_스카이_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_슈퍼_크릭, grayscale=False)
                    if count:
                        if SSR_슈퍼_크릭_count < count:
                            SSR_슈퍼_크릭_count = count
                        print("SSR_슈퍼_크릭 " + str(SSR_슈퍼_크릭_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_스마트_팔콘, grayscale=False)
                    if count:
                        if SSR_스마트_팔콘_count < count:
                            SSR_스마트_팔콘_count = count
                        print("SSR_스마트_팔콘 " + str(SSR_스마트_팔콘_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_스페셜_위크, grayscale=False)
                    if count:
                        if SSR_스페셜_위크_count < count:
                            SSR_스페셜_위크_count = count
                        print("SSR_스페셜_위크 " + str(SSR_스페셜_위크_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_아이네스_후진, grayscale=False)
                    if count:
                        if SSR_아이네스_후진_count < count:
                            SSR_아이네스_후진_count = count
                        print("SSR_아이네스_후진 " + str(SSR_아이네스_후진_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_에어_샤커, grayscale=False)
                    if count:
                        if SSR_에어_샤커_count < count:
                            SSR_에어_샤커_count = count
                        print("SSR_에어_샤커 " + str(SSR_에어_샤커_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_엘_콘도르_파사, grayscale=False)
                    if count:
                        if SSR_엘_콘도르_파사_count < count:
                            SSR_엘_콘도르_파사_count = count
                        print("SSR_엘_콘도르_파사 " + str(SSR_엘_콘도르_파사_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_오구리_캡, grayscale=False)
                    if count:
                        if SSR_오구리_캡_count < count:
                            SSR_오구리_캡_count = count
                        print("SSR_오구리_캡 " + str(SSR_오구리_캡_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_위닝_티켓, grayscale=False)
                    if count:
                        if SSR_위닝_티켓_count < count:
                            SSR_위닝_티켓_count = count
                        print("SSR_위닝_티켓 " + str(SSR_위닝_티켓_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_타마모_크로스, grayscale=False)
                    if count:
                        if SSR_타마모_크로스_count < count:
                            SSR_타마모_크로스_count = count
                        print("SSR_타마모_크로스 " + str(SSR_타마모_크로스_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_토카이_테이오, grayscale=False)
                    if count:
                        if SSR_토카이_테이오_count < count:
                            SSR_토카이_테이오_count = count
                        print("SSR_토카이_테이오 " + str(SSR_토카이_테이오_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_트윈_터보, grayscale=False)
                    if count:
                        if SSR_트윈_터보_count < count:
                            SSR_트윈_터보_count = count
                        print("SSR_트윈_터보 " + str(SSR_트윈_터보_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_파인_모션, grayscale=False)
                    if count:
                        if SSR_파인_모션_count < count:
                            SSR_파인_모션_count = count
                        print("SSR_파인_모션 " + str(SSR_파인_모션_count) + "개")
                        print(position)
                            
                    count = 0
                    count, position = ImageSearch(img, SSR_하야카와_타즈나, grayscale=False)
                    if count:
                        if SSR_하야카와_타즈나_count < count:
                            SSR_하야카와_타즈나_count = count
                        print("SSR_하야카와_타즈나 " + str(SSR_하야카와_타즈나_count) + "개")
                        print(position)
                
                SR_스윕_토쇼_total += SR_스윕_토쇼_count
                SSR_골드_쉽_total += SSR_골드_쉽_count
                SSR_골드_시티_total += SSR_골드_시티_count
                SSR_그래스_원더_total += SSR_그래스_원더_count
                SSR_니시노_플라워_total += SSR_니시노_플라워_count
                SSR_보드카_total += SSR_보드카_count
                SSR_비코_페가수스_total += SSR_비코_페가수스_count
                SSR_사일런스_스즈카_total += SSR_사일런스_스즈카_count
                SSR_사쿠라_바쿠신_오_total += SSR_사쿠라_바쿠신_오_count
                SSR_세이운_스카이_total += SSR_세이운_스카이_count
                SSR_슈퍼_크릭_total += SSR_슈퍼_크릭_count
                SSR_스마트_팔콘_total += SSR_스마트_팔콘_count
                SSR_스페셜_위크_total += SSR_스페셜_위크_count
                SSR_아이네스_후진_total += SSR_아이네스_후진_count
                SSR_에어_샤커_total += SSR_에어_샤커_count
                SSR_엘_콘도르_파사_total += SSR_엘_콘도르_파사_count
                SSR_오구리_캡_total += SSR_오구리_캡_count
                SSR_위닝_티켓_total += SSR_위닝_티켓_count
                SSR_타마모_크로스_total += SSR_타마모_크로스_count
                SSR_토카이_테이오_total += SSR_토카이_테이오_count
                SSR_트윈_터보_total += SSR_트윈_터보_count
                SSR_파인_모션_total += SSR_파인_모션_count
                SSR_하야카와_타즈나_total +=  SSR_하야카와_타즈나_count

                
                print("-"*50)
                if SR_스윕_토쇼_total:
                    print("SR_스윕_토쇼_total:", SR_스윕_토쇼_total)
                if SSR_골드_쉽_total:
                    print("SSR_골드_쉽_total:", SSR_골드_쉽_total)
                if SSR_골드_시티_total:
                    print("SSR_골드_시티_total:", SSR_골드_시티_total)
                if SSR_그래스_원더_total:
                    print("SSR_그래스_원더_total:", SSR_그래스_원더_total)
                if SSR_니시노_플라워_total:
                    print("SSR_니시노_플라워_total:", SSR_니시노_플라워_total)
                if SSR_보드카_total:
                    print("SSR_보드카_total:", SSR_보드카_total)
                if SSR_비코_페가수스_total:
                    print("SSR_비코_페가수스_total:", SSR_비코_페가수스_total)
                if SSR_사일런스_스즈카_total:
                    print("SSR_사일런스_스즈카_total:", SSR_사일런스_스즈카_total)
                if SSR_사쿠라_바쿠신_오_total:
                    print("SSR_사쿠라_바쿠신_오_total:", SSR_사쿠라_바쿠신_오_total)
                if SSR_세이운_스카이_total:
                    print("SSR_세이운_스카이_total:", SSR_세이운_스카이_total)
                if SSR_슈퍼_크릭_total:
                    print("SSR_슈퍼_크릭_total:", SSR_슈퍼_크릭_total)
                if SSR_스마트_팔콘_total:
                    print("SSR_스마트_팔콘_total:", SSR_스마트_팔콘_total)
                if SSR_스페셜_위크_total:
                    print("SSR_스페셜_위크_total:", SSR_스페셜_위크_total)
                if SSR_아이네스_후진_total:
                    print("SSR_아이네스_후진_total:", SSR_아이네스_후진_total)
                if SSR_에어_샤커_total:
                    print("SSR_에어_샤커_total:", SSR_에어_샤커_total)
                if SSR_엘_콘도르_파사_total:
                    print("SSR_엘_콘도르_파사_total:", SSR_엘_콘도르_파사_total)
                if SSR_오구리_캡_total:
                    print("SSR_오구리_캡_total:", SSR_오구리_캡_total)
                if SSR_위닝_티켓_total:
                    print("SSR_위닝_티켓_total:", SSR_위닝_티켓_total)
                if SSR_타마모_크로스_total:
                    print("SSR_타마모_크로스_total:", SSR_타마모_크로스_total)
                if SSR_토카이_테이오_total:
                    print("SSR_토카이_테이오_total:", SSR_토카이_테이오_total)
                if SSR_트윈_터보_total:
                    print("SSR_트윈_터보_total:", SSR_트윈_터보_total)
                if SSR_파인_모션_total:
                    print("SSR_파인_모션_total:", SSR_파인_모션_total)
                if SSR_하야카와_타즈나_total:
                    print("SSR_하야카와_타즈나_total:", SSR_하야카와_타즈나_total)
                print("-"*50)
                
                
                # 이륙 조건식 -----------------------------------------------
                # 이륙 조건식 -----------------------------------------------
                # 이륙 조건식 -----------------------------------------------
                
                if SSR_파인_모션_total and SSR_슈퍼_크릭_total and SSR_하야카와_타즈나_total:
                    return True
                
                if SSR_파인_모션_total and SSR_비코_페가수스_total and SSR_하야카와_타즈나_total :
                    return True
                
                if SSR_파인_모션_total and SSR_사쿠라_바쿠신_오_total and SSR_하야카와_타즈나_total:
                    return True
                    
                if SSR_파인_모션_total >= 2 and (SSR_슈퍼_크릭_total or SSR_하야카와_타즈나_total):
                    return True
                    
                if SSR_슈퍼_크릭_total >= 2 and (SSR_파인_모션_total or SSR_하야카와_타즈나_total):
                    return True
                    
                if SSR_비코_페가수스_total >= 2 and (SSR_슈퍼_크릭_total or SSR_하야카와_타즈나_total):
                    return True
                    
                if SSR_사쿠라_바쿠신_오_total >= 2 and (SSR_파인_모션_total or SSR_슈퍼_크릭_total or SSR_하야카와_타즈나_total):
                    return True
                    
                if SSR_파인_모션_total >= 3:
                    return True
                    
                if SSR_슈퍼_크릭_total >= 3:
                    return True
                    
                if SSR_비코_페가수스_total >= 3:
                    return True
                    
                if SSR_사쿠라_바쿠신_오_total >= 3:
                    return True
                    
                if SSR_하야카와_타즈나_total >= 3:
                    return True
                    
                if SR_스윕_토쇼_total >= 5 and SSR_파인_모션_total and SSR_하야카와_타즈나_total and (SSR_슈퍼_크릭_total or SSR_비코_페가수스_total or SSR_사쿠라_바쿠신_오_total):
                    return True
                            
            count = 0
            count, position = ImageSearch(img, 한_번_더_뽑기)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("한_번_더_뽑기 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 쥬얼이_부족합니다)
            if count:
                updateTime = time.time()
                # adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                is쥬얼부족 = True
                is뽑기_이동 = False
                is연동하기 = True
                adbInput.Key_event(device=device, key_code="keyevent 4") # "KEYCODE_BACK" 
                time.sleep(0.5)
                adbInput.Key_event(device=device, key_code="keyevent 4")
                print("쥬얼이_부족합니다 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 상점_화면을_표시할_수_없습니다)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetY=147, deltaX=5, deltaY=5)
                print("상점_화면을_표시할_수_없습니다 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 메뉴, 452, 48, 57, 48)
            if count and is연동하기:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX=5, offsetY=5)
                print("메뉴 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 메뉴_단축, 511, 73, 19, 31, confidence=0.98, grayscale=False)
            if count and is연동하기:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX=4)
                print("메뉴_단축 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 계정_정보, 354, 635, 111, 51)
            if count and is연동하기:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("계정_정보 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 카카오_로그인, 211, 446, 115, 50)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("카카오_로그인 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 확인하고_계속하기, 186, 623, 144, 53)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("확인하고_계속하기 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 확인하고_계속하기2, 186, 625, 143, 50)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("확인하고_계속하기2 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 확인하고_계속하기3)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("확인하고_계속하기3 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 계속하기, 214, 620, 85, 47)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("계속하기 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 정보_확인_중, 105, 167, 188, 49)
            if count:
                updateTime = time.time()
                adbInput.Key_event(device=device, key_code="keyevent 4")
                print("정보_확인_중 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, Google_계정으로_로그인)
            if count:
                updateTime = time.time()
                adbInput.Key_event(device=device, key_code="keyevent 4")
                print("Google_계정으로_로그인 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 인증되지_않는_로그인_방법_입니다)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetY=143, deltaX=5, deltaY=5)
                print("인증되지_않는_로그인_방법_입니다 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 카카오_로그인_연동에_성공하였습니다, 68, 469, 384, 65)
            if count:
                updateTime = time.time()
                is초기화하기 = True
                # adbInput.Key_event(device=device, key_code="keyevent 1") # KEYCODE_MENU
                WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_SCROLL)
                print("카카오_로그인_연동에_성공하였습니다 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, 로그아웃)
            if count:
                updateTime = time.time()
                is초기화하기 = True
                # adbInput.Key_event(device=device, key_code="keyevent 1") # KEYCODE_MENU
                WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_SCROLL)
                print("로그아웃 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)

            count = 0
            count, position = ImageSearch(img, 모두_지우기, 428, 40, 96, 48)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0])
                print("모두_지우기 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 크롬_실행)
            if count and is초기화하기:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0])
                print("크롬_실행 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 크롬_실행2)
            if count and is초기화하기:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0])
                print("크롬_실행 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            count = 0
            count, position = ImageSearch(img, 연결된_서비스_관리)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("연결된_서비스_관리 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.1)
                img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                
            count = 0
            count, position = ImageSearch(img, 우마무스메_서비스)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("우마무스메_서비스 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.2)
                img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                
            count = 0
            count, position = ImageSearch(img, 모든_정보_삭제, 202, 390, 116, 50)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("모든_정보_삭제 " + str(count) + "개")
                print(position)
                time.sleep(0.2)
                img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                
            count = 0
            count, position = ImageSearch(img, 이_서비스의_모든_정보를_삭제하시겠습니까)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX=258, offsetY=92, deltaX=5, deltaY=5)
                time.sleep(0.5)
                for _ in range(15):
                    WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_BACK)
                time.sleep(0.2)
                WindowsAPIInput.WindowsAPIKeyboardInputString(hwndMain, "우마무스메 프리티 더비")
                print("이_서비스의_모든_정보를_삭제하시겠습니까 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.2)
                img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷

            count = 0
            count, position = ImageSearch(img, 이_서비스의_모든_정보를_삭제하시겠습니까2)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX=258, offsetY=92, deltaX=5, deltaY=5)
                time.sleep(0.5)
                for _ in range(15):
                    WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_BACK)
                time.sleep(0.2)
                WindowsAPIInput.WindowsAPIKeyboardInputString(hwndMain, "우마무스메 프리티 더비")
                print("이_서비스의_모든_정보를_삭제하시겠습니까 " + str(count) + "개")
                print(position)
                print((position[0][0] - 25, position[0][1] - 25, position[0][2] + 25, position[0][3] + 25))
                time.sleep(0.2)
                img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                
            count = 0
            count, position = ImageSearch(img, 모든_정보_삭제_빨간_박스, 204, 559, 108, 50, confidence=0.99, grayscale=False)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("모든_정보_삭제_빨간_박스 " + str(count) + "개")
                print(position)
                time.sleep(0.2)
                img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                
            count = 0
            count, position = ImageSearch(img, 비밀번호, 0, 242, 78, 51, confidence=0.99, grayscale=False)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("비밀번호 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                
            count = 0
            count, position = ImageSearch(img, 자동완성_Continue, 214, 923, 90, 47)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("자동완성_Continue " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                
            count = 0
            count, position = ImageSearch(img, 자동완성_계속, 226, 907, 62, 49)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("자동완성_계속 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                
            count = 0
            count, position = ImageSearch(img, 비밀번호_확인, 231, 356, 55, 46, confidence=0.99, grayscale=False)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("비밀번호_확인 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain) # 윈도우의 스크린샷
                
            count = 0
            count, position = ImageSearch(img, 삭제_완료, confidence=0.99)
            if count:
                updateTime = time.time()
                WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_SCROLL)
                print("삭제_완료 " + str(count) + "개")
                GlobalisDoneTutorial = True
                print(position)
                time.sleep(0.5)
                return "Failed"
                
                
                
                
            # 특수 이벤트
            count = 0
            count, position = ImageSearch(img, 튜토리얼을_스킵하시겠습니까)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX=120, offsetY=140, deltaX=5, deltaY=5)
                print("튜토리얼을_스킵하시겠습니까 " + str(count) + "개")
                print(position)
                img = screenshotToOpenCVImg(hwndMain)
            
            count = 0
            count, position = ImageSearch(img, 타이틀_화면으로)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("타이틀_화면으로 " + str(count) + "개")
                print(position)
                img = screenshotToOpenCVImg(hwndMain)
            
            count = 0
            count, position = ImageSearch(img, _2단계_인증)
            if count:
                updateTime = time.time()
                WindowsAPIInput.WindowsAPIKeyboardInput(hwndMain, WindowsAPIInput.win32con.VK_SCROLL)
                print("_2단계_인증 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
            
            count = 0
            count, position = ImageSearch(img, 확인)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("확인 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
            
            count = 0
            count, position = ImageSearch(img, 앱_닫기, 78, 425, 391, 205)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
                print("앱_닫기 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
            
            count = 0
            count, position = ImageSearch(img, 날짜가_변경됐습니다)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetY=142, deltaX=5, deltaY=5)
                print("날짜가_변경됐습니다 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
            
            count = 0
            count, position = ImageSearch(img, 추가_데이터를_다운로드합니다)
            if count:
                updateTime = time.time()
                adbInput.BlueStacksClick(device=device, position=position[0], offsetX=125, offsetY=155, deltaX=5, deltaY=5)
                print("추가_데이터를_다운로드합니다 " + str(count) + "개")
                print(position)
                time.sleep(0.5)
                img = screenshotToOpenCVImg(hwndMain)
                
            time.sleep(0.5)
            
        if self.isAlive == False:
                return "Stop"
    
                
    # def str2bool(v):
    #     if isinstance(v, bool):
    #     return v
    #     if v.lower() in ('yes', 'true', 't', 'y', '1'):
    #         return True
    #     elif v.lower() in ('no', 'false', 'f', 'n', '0'):
    #         return False
    #     else:
    #         raise argparse.ArgumentTypeError('Boolean value expected.')
    #     # https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse






# if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="메인 함수입니다. 매개변수에 (윈도우 이름, ADB 포트)를 적어서 사용하세요")
    
    # parser.add_argument("--InstanceName", type=str, default="BlueStacks 8", help="윈도우의 이름을 적어주세요")
    # parser.add_argument("--InstancePort", type=int, default=6165, help="인스턴스의 고유 adb포트를 적어주세요")
    # parser.add_argument("--isDoneTutorial", type=str2bool, default=True, help="튜토리얼 완료 여부")
    # args = parser.parse_args()
    
    
        
# count = 0
# count, position = ImageSearch(img, 우마무스메_실행) # 스크린샷, 찾을 이미지, ROI, 정확도, 명암 변화, 추출
# if count:
#     adbInput.BlueStacksClick(device=device, position=position[0], deltaX=5, deltaY=5)
#     print("시작하기 " + str(count) + "개") # 찾은 갯수
#     print(position) # 박스 위치 출력
#     time.sleep(0.5)