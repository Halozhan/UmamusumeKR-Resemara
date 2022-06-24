-- SSR 개수 5개 이상 및
-- 파인모션 1장 이상 및
-- 슈퍼크릭 1장 이상
if SSR_count >= 5 and motion >= 1 and creek >=1 then
 SendKakaoTalk(0, "", true)
 Stop()
end