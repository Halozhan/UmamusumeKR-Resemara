-- SSR ���� 5�� �̻�
if SSR_count == nil then
  SSR_count = 0
end
if SSR_count >= 5 then
 SendKakaoTalk(0, "", true)
 Stop()
end