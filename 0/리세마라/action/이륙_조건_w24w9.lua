-- SSR 개수 6개 이상
if SSR_count == nil then
  SSR_count = 0
end
if SSR_count >= 6 then
 SendKakaoTalk(0, "", true)
 Stop()
end