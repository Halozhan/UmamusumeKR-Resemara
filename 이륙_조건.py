# 이륙 조건식 -----------------------------------------------
def 이륙_조건(Support_Cards):
    SCT = Support_Cards
    if SCT["SSR_파인_모션"] and SCT["SSR_슈퍼_크릭"] and SCT["SSR_하야카와_타즈나"]:
        return True
    
    # if SCT["SSR_파인_모션"] and SCT["SSR_비코_페가수스"] and SCT["SSR_하야카와_타즈나"]:
    #     return True
    
    # if SCT["SSR_파인_모션"] and SCT["SSR_사쿠라_바쿠신_오"] and SCT["SSR_하야카와_타즈나"]:
    #     return True
        
    if SCT["SSR_파인_모션"] >= 2 and (SCT["SSR_슈퍼_크릭"] or SCT["SSR_하야카와_타즈나"]):
        return True
        
    if SCT["SSR_슈퍼_크릭"] >= 2  and (SCT["SSR_파인_모션"] or SCT["SSR_하야카와_타즈나"]):
        return True
    
    # if SCT["SSR_비코_페가수스"] >= 2 and (SCT["SSR_슈퍼_크릭"] or SCT["SSR_하야카와_타즈나"]):
    #     return True
    
    # if SCT["SSR_사쿠라_바쿠신_오"] >= 2 and (SCT["SSR_파인_모션"] or SCT["SSR_슈퍼_크릭"] or SCT["SSR_하야카와_타즈나"]):
    #     return True
    
    if SCT["SSR_파인_모션"] >= 3:
        return True
        
    if SCT["SSR_슈퍼_크릭"] >= 3:
        return True
    
    # if SCT["SSR_비코_페가수스"] >= 3:
    #     return True
    
    # if SCT["SSR_사쿠라_바쿠신_오"] >= 3:
    #     return True
    
    if SCT["SSR_하야카와_타즈나"] >= 3:
        return True
    
    if SCT["SR_스윕_토쇼"] >= 5 and SCT["SSR_파인_모션"] and SCT["SSR_하야카와_타즈나"] and (SCT["SSR_슈퍼_크릭"] or SCT["SSR_비코_페가수스"] or SCT["SSR_사쿠라_바쿠신_오"]):
        return True

    if SCT["SSR_메지로_파머"] >= 4:
        return True

    return False