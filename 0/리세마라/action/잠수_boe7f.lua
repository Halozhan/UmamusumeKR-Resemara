-- set/get delay timer
function setClock()
    return os.clock()
end

function getClock(clock)
    if clock ~= nil then
        return os.clock() - clock
    else
        print(clock..' is null value now')
    end
end


-- 앱 동작 정지 감시 판단 시간, 검사 간격 (단위:초)
STOP_JUDGE_SV = 40
STOP_CHECK_PERIOD_SV = 5

-- 사용하는 앱의 해상도나 사이즈에 따라 변경 필수! 가로폭, 높이(w,h)
local screen_size = {w = 540, h = 960}
local roi = {0, 0, screen_size.w, screen_size.h}

-- 현재 화면 저장 인스턴스 생성 및 스크린캡쳐
if screen == nil then
    screen = NewBits(screen_size.w, screen_size.h)
    CaptureScreen(screen, roi)
    stop_check_period = setClock()
end

-- 앱 정지판단 검사 간격 시간 도달, 캡쳐된 인스턴스와 현재화면 비교
if getClock(stop_check_period) >= STOP_CHECK_PERIOD_SV then
    local acc, fx, fy = BitsSearch({bits = screen, w = screen_size.w, h= screen_size.h}, roi)
    print('>> 앱 정지 체크 시작 ('..STOP_CHECK_PERIOD_SV..'초 마다 검사)')
    print('( 화면유사도(acc)가 99 이상일 경우 동작 정지 의심 )')
    print('[ acc : '..acc, 'fx : '..fx, 'fy : '..fy..' ]')

    -- 유사도가 99 이상일시 앱 정지로 판단
    if acc >= 99 then
        if stop_check_time == nil then
            stop_check_time = setClock()
        end
        
        local sec = math.floor(getClock(stop_check_time))
        print('- 앱 정지 모니터 시간 : '..sec..' / '..STOP_JUDGE_SV..' sec')
        
        -- 앱 정지 판단 설정 시간 보다 이상 정지 확인시 동작
        if getClock(stop_check_time) >= STOP_JUDGE_SV then
            print('- 앱 정지 체크 결과 : 동작 정지 의심!')
            print('=============================================')
            EnableImage(true, '아무거나클릭')

            -- 안씀 OpenScript('reboot') -- 앱 재실행 스크립트 변경
        end
        
    else
        -- 유사도가 90 미만일시 앱 정상동작으로 판단, 초기화
        ReleaseBits(screen)
        screen = nil
        stop_check_period = nil
        stop_check_time = nil
        print('- 앱 정지 체크 결과 : 동작 양호!')
        print('=============================================')
        EnableImage(false, '아무거나클릭')
    end
end