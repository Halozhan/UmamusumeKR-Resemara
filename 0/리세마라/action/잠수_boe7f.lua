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


-- �� ���� ���� ���� �Ǵ� �ð�, �˻� ���� (����:��)
STOP_JUDGE_SV = 40
STOP_CHECK_PERIOD_SV = 5

-- ����ϴ� ���� �ػ󵵳� ����� ���� ���� �ʼ�! ������, ����(w,h)
local screen_size = {w = 540, h = 960}
local roi = {0, 0, screen_size.w, screen_size.h}

-- ���� ȭ�� ���� �ν��Ͻ� ���� �� ��ũ��ĸ��
if screen == nil then
    screen = NewBits(screen_size.w, screen_size.h)
    CaptureScreen(screen, roi)
    stop_check_period = setClock()
end

-- �� �����Ǵ� �˻� ���� �ð� ����, ĸ�ĵ� �ν��Ͻ��� ����ȭ�� ��
if getClock(stop_check_period) >= STOP_CHECK_PERIOD_SV then
    local acc, fx, fy = BitsSearch({bits = screen, w = screen_size.w, h= screen_size.h}, roi)
    print('>> �� ���� üũ ���� ('..STOP_CHECK_PERIOD_SV..'�� ���� �˻�)')
    print('( ȭ�����絵(acc)�� 99 �̻��� ��� ���� ���� �ǽ� )')
    print('[ acc : '..acc, 'fx : '..fx, 'fy : '..fy..' ]')

    -- ���絵�� 99 �̻��Ͻ� �� ������ �Ǵ�
    if acc >= 99 then
        if stop_check_time == nil then
            stop_check_time = setClock()
        end
        
        local sec = math.floor(getClock(stop_check_time))
        print('- �� ���� ����� �ð� : '..sec..' / '..STOP_JUDGE_SV..' sec')
        
        -- �� ���� �Ǵ� ���� �ð� ���� �̻� ���� Ȯ�ν� ����
        if getClock(stop_check_time) >= STOP_JUDGE_SV then
            print('- �� ���� üũ ��� : ���� ���� �ǽ�!')
            print('=============================================')
            EnableImage(true, '�ƹ��ų�Ŭ��')

            -- �Ⱦ� OpenScript('reboot') -- �� ����� ��ũ��Ʈ ����
        end
        
    else
        -- ���絵�� 90 �̸��Ͻ� �� ���������� �Ǵ�, �ʱ�ȭ
        ReleaseBits(screen)
        screen = nil
        stop_check_period = nil
        stop_check_time = nil
        print('- �� ���� üũ ��� : ���� ��ȣ!')
        print('=============================================')
        EnableImage(false, '�ƹ��ų�Ŭ��')
    end
end