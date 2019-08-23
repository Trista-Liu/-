import os
import zipfile
import tarfile 
import zipfile
import gzip
import string

def find_string(content,key_word):
    try: 
        return content.find(key_word) != -1
    except(ValueError):         
        return False

def unzip_single(root, file):
    shotname, _ = os.path.splitext(os.path.join(root,file))
    if os.path.exists(shotname):
        return ""
    zf = zipfile.ZipFile(os.path.join(root,file))
    try:
        zf.extractall(path=root)
        file = file.replace(".zip", "")
        return os.path.join(root,file) 
    except RuntimeError as e:
        print("unzip file error: ",e)
    zf.close()

def readKeyWordFromGzAndWrite(key_word, file_path, des_dir): 
    f = gzip.open(file_path) 
    file_path = file_path.replace(".gz","")
    writeFile = open(file_path, mode="wb")
    targetFile = open(des_dir, mode="a")
    readFile = open(file_path, mode='r',errors='ignore')
    try:
        shotname, _ = os.path.splitext(file_path)
        if os.path.exists(shotname):
            return
        
        file_content = f.read()
        writeFile.write(file_content)
        targetFile.write(file_path+"\n")
        file_content = readFile.readline()

        while file_content:
            if find_string(file_content, key_word):
                targetFile.write(file_content)
            file_content = readFile.readline()
    
    except Exception as e:
        print("readKeyWordFromGzAndWrite and write error: ",e)  
    finally:  
        f.close()
        writeFile.close()
        targetFile.close()
        readFile.close()

def readKeyWordAndWrite(file_path, key_word, des_dir):
    file = open(file_path, mode='r', errors='ignore')  
    writeFile = open(des_dir, mode="a")
    writeFile.write(file_path+"\n")
    try:
        text_line = file.readline()
        while text_line:
            if text_line.find(key_word) != -1:
                writeFile.write(text_line)
            text_line = file.readline()
    except Exception as e:
        print("read key word and write error: ",e)
    finally:
        file.close()
        writeFile.close()

def handleDir(key_word, file_path, des_dir):  
    for root, _, files in os.walk(file_path): 
        for file in files: 
            handleInputAndOutput(key_word, os.path.join(root,file), des_dir)
        
def handleInputAndOutput(key_word, intput_file_src, key_word_file_path):
    if os.path.isdir(intput_file_src):  
        handleDir(key_word, intput_file_src, key_word_file_path)
    elif os.path.splitext(intput_file_src)[1]=='.zip':  
        filepath, tmpfilename = os.path.split(intput_file_src)    
        unzip_file = unzip_single(filepath, tmpfilename)
        if unzip_file != "":
            handleDir(key_word,unzip_file,key_word_file_path)
    elif os.path.splitext(intput_file_src)[1]=='.gz':
        readKeyWordFromGzAndWrite(key_word, intput_file_src,key_word_file_path)
    elif os.path.splitext(intput_file_src)[1]=='.txt' or find_string(os.path.splitext(intput_file_src)[1],"log"): 
        readKeyWordAndWrite(intput_file_src,key_word,key_word_file_path)

def main():
    # key_word = input("Please input key word: ")
    # if key_word == "":
    #     key_word = "[KPI][init]"

    key_word = "[KPI][init]"
    # intput_file_src = input("Please input file path: ")
    # if intput_file_src == "":
    #     intput_file_src = os.getcwd()
    intput_file_src = os.getcwd()

    key_word_file_path = os.path.join(intput_file_src,"keyword.txt")
    if os.path.exists(key_word_file_path):
        os.remove(key_word_file_path)

    handleInputAndOutput(key_word, intput_file_src, key_word_file_path)
    print("Finding files completed！")
    
main()




