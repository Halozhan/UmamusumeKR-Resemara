path = "./"

import shutil
import glob

count = 4

for instance in range(1, count+1, 1):
    instance = str(instance)
    
    # shutil.rmtree()
    # shutil.copytree(path+"0", path+str(instance))
    try:
        shutil.copytree(path+"0", path+instance)
    except FileExistsError:
        print(instance+"의 파일이 존재합니다.")
    except:
        print("암튼 뭔지 오류남")
        pass
    
    # for file in glob.glob(path+instance+"/iMax*.exe"):
        
        # shutil.move(file, path+instance+"/iMax_"+instance+".exe") 막힘

    read_file = open(path+instance+"/ini/리세마라.ini", mode = "r")

    text = []
    for line in read_file.readlines():
        
        if "TWAName" in line:
            text.append("TWAName=BlueStacks "+instance+"\n")
        elif "TWBName" in line:
            text.append("TWBName=BlueStacks "+instance+"\n")
        else:
            text.append(line)

    read_file.close()

    write_file = open(path+instance+"/ini/리세마라.ini", mode = "w")

    write_file.writelines(text)
    
    # TWA, TWB
    read_file = open(path+instance+"/리세마라/리세마라.xml", mode = "r")

    text = []
    for line in read_file.readlines():
        
        if "TWAName" in line:
            text.append("        <TWAName>BlueStacks "+instance+"</TWAName>"+"\n")
        elif "TWBName" in line:
            text.append("        <TWBName>BlueStacks "+instance+"</TWBName>"+"\n")
        else:
            text.append(line)

    read_file.close()

    write_file = open(path+instance+"/리세마라/리세마라.xml", mode = "w")

    write_file.writelines(text)
    

    write_file.close()