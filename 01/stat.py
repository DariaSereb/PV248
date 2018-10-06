import re
import string
import sys





if sys.argv[1] == "composer":
    
    frequency = {}
    document_text = open('scorelib.txt',encoding="utf8")
    text_string = document_text.read()
    
    for  lines in re.findall(r'(?<=Composer: )(.*)', text_string):
         match_pattern = re.split(r'; ', lines)
         for  lines in match_pattern:
             if re.findall (r".*\(\d*.*\)$|.*\(\d*.*\) $|.*\(\d*.*\)  $|.*\(\d*.*\)   $|\s*", lines):
                 match_pattern3 = re.findall(r"\S*..\S*..\S*..[a-z]+|\S*..\[a-z]+", lines)

                 for lines in match_pattern3:
                     count = frequency.get(lines,0)
                     frequency[lines] = count + 1
                     frequency_list = frequency.keys()
             else:
                 for lines in match_pattern:
                     count = frequency.get(lines,0)
                     frequency[lines] = count + 1
    frequency_list = frequency.keys()
    
    for lines in frequency_list:
    
        print (lines,':',frequency[lines])

        

if sys.argv[1] == "century":

    frequency = {}
    document_text = open('scorelib.txt',encoding="utf8")
    text_string = document_text.read()
    match_pattern = re.findall(r'(?<=Composition Year: 15\d{2})', text_string)

    for word in match_pattern:
      count = frequency.get(word,0)
      frequency[word] = count + 1

 
    frequency_list = frequency.keys()
    for words in frequency_list:
   
       print ('16th century:',frequency[words])

    frequency.clear()

    match_pattern = re.findall(r'(?<=Composition Year: 16\d{2})', text_string)
    match_pattern2 = re.findall(r'(?<=Composition Year: 17th)', text_string)

    for word in match_pattern:
       count = frequency.get(word,0)
       frequency[word] = count + 1
    for word in match_pattern2:
       count = frequency.get(word,0)
       frequency[word] = count + 1

 
    frequency_list = frequency.keys()
    
    for words in frequency_list:
   
       print ('17th century:',frequency[words])
     
    frequency.clear()

    match_pattern = re.findall(r'(?<=Composition Year: 17\d{2})', text_string)
    match_pattern2 = re.findall(r'(?<=Composition Year: 18th)', text_string)

    for word in match_pattern:
       count = frequency.get(word,0)
       frequency[word] = count + 1
    for word in match_pattern2:
       count = frequency.get(word,0)
       frequency[word] = count + 1

 
    frequency_list = frequency.keys()
    
    for words in frequency_list:
   
       print ('18th century:',frequency[words])

    frequency.clear()


