def parseJson(content):
    flag=0
    seperated = []
    if content.index("load_more_widget_html")> content.index("content_html") :
        
        seperated = content.split("load_more_widget_html",1)
    else:
        flag = 1
        seperated = content.split("content_html",1)

    # getting content
    main_content = seperated[0]
    main_content = main_content.split(":",1)[1].split('"',1)[1].rsplit('"',1)[0]
    main_content = main_content.replace("\\","")
    
    widget_content =seperated[1]
    widget_content = widget_content.split('"',1)[1].rsplit('"',1)[0]
    widget_contet = widget_content.replace("\\","")

    
    if flag==1:
        return {'content_html':widget_content,'load_more_widget_html':main_content}

    return {'content_html':main_content,'load_more_widget_html':widget_content}
