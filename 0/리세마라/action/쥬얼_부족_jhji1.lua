-- 카카오판 초기화
if read_book then
  EnableImage(false, "뽑기_이동")
  EnableImage(true, "메뉴로")
  EnableImage(true, "계정_정보")
else
  EnableImage(false, "뽑기_이동")
  EnableImage(true, "메뉴로")
  EnableImage(true, "도감열기")
end