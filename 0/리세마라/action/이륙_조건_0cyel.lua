-- SSR 개수 6개 이상 및
-- 슈퍼크릭 1장 이상 및
-- 타즈나 1장 이상
if SSR_count >= 6 and creek >= 1 and tazuna >=1 then
 SendKakaoTalk(0, "", true)
 Stop()
end