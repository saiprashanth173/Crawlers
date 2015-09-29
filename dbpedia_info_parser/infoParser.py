
import urllib2
from pymongo import MongoClient as MC

#this is used for opening the csv file 
def openPageDocument(doc_name):
    return open(doc_name,"r")

#this performs major operations
def performOperation(file_object,count):
    title = ""
    for i in range(0,count):
        file_object.readline()
    content = file_object.readline()
    dicti={}
    while content:
        print content
        main_content= content.split("\t")
        
        if (len(main_content)>2 and "/" not in  main_content[0] and "upload.wikimedia.org" not in main_content[0] and "Template" not in main_content[1] and "reviews" not in main_content[1]):
            main_key = urllib2.unquote(main_content[0].strip())
            if title!=main_key:
                
                
                if title!="":
                    insertDB(dicti)
                open("track_file","w").write(str(count))
                dicti={}
                title= main_key
                dicti[main_key]={}
                dicti[main_key]["keys"] = [main_content[1].strip()]
                dicti[main_key][main_content[1].strip().replace(".","##dot##")]=[]
                

            key = main_content[1].strip().replace(".","##dot##")
            
            if key not in dicti[main_key]:
                dicti[main_key]["keys"].append(key)
                dicti[main_key][key] = []

            if len(main_content)!=4 and len(main_content)>2:
                dicti[main_key][key].append(main_content[2].strip())
                getTillObtained(file_object,dicti,main_key,key,count)

            elif len(main_content)>2:
                dicti[main_key][key].append(main_content[2].strip())

        content = file_object.readline()
        count+=1

                
                                   


def getTillObtained(file_object,dicti,main_key,key,count):
    count+=1
    main_content = file_object.readline()
    while "\t" not in main_content:
        dicti[main_key][key].append(main_content.strip())
        main_content = file_object.readline()
        
    main_content= main_content.split("\t")[0].strip()
    dicti[main_key][key].append(main_content)
    

#this is used to store the content
def insertDB(dicti):
    if "_id" in dicti:
        dicti.pop('_id')
    #print dicti
    keys = dicti.keys()[0]
    content = dicti[keys]
    content["wiki_title"]=keys
    if "_id" in content:
        content.pop("_id")
   # print content
    client = MC()
    db = client.wiki_info
    db.info_box.insert(content)
def main():
    fo = openPageDocument("/home/prashanth/Downloads/infobox_en.csv")
    count = int(open("track_file","r").read().strip())
    performOperation(fo,count)
main()
