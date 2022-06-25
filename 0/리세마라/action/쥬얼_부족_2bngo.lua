-- 게스트판 초기화
if read_book then
  EnableImage(true, "초기화_활성화")
else
  EnableImage(false, "뽑기_이동")
  EnableImage(true, "메뉴로")
  EnableImage(true, "메뉴로_단축")
end