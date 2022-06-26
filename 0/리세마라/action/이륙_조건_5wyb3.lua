-- SSR 개수 6개 이상 및
-- 파인모션 1장 이상 및
-- 박신 1장 이상
if SSR_count >= 6 and motion >= 1 and bakushin >=1 then
 SendKakaoTalk(0, "", true)
 Stop()
end