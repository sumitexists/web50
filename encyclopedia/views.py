from django.shortcuts import render, redirect
import markdown
import random
from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def topic(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html", {"error": 0})
    
    content = util.get_entry(title)
    html = markdown.markdown(content)
    return render(request, "encyclopedia/topic.html",{"title":title, "html":html , "entries": util.list_entries()})


def NewPage(request):
    if request.method == "POST":
        new_title = request.POST.get("title")
        new_content = request.POST.get("blog")
        if new_title in util.list_entries():
            return render(request, 'encyclopedia/error.html', {"error" : 1})
        if new_title == "" or new_content == "":
            return render (request, "encyclopedia/NewPage.html" , {"error" : 2, "title" : new_title, "content" : new_content}) 
        util.save_entry(new_title,new_content)
        return redirect('encyclopedia:topic', title=new_title)
        
        

    return render (request, "encyclopedia/NewPage.html" ,{"entries": util.list_entries()})

def EditPage(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        new_content = request.POST.get("update")
        util.save_entry(title, new_content)
        return redirect("encyclopedia:topic",title = title )
    return render(request, 'encyclopedia/EditPage.html',{"html" : content , "title" : title , "entries": util.list_entries()})


def RandomPage(request):
    random_entry = random.choice(util.list_entries())
    return redirect('encyclopedia:topic', title=random_entry)

def Search(request):
    if request.method == "POST":
        title = request.POST.get("q")
        if title in util.list_entries():
            return redirect('encyclopedia:topic', title = title)
        elif title == "":
            return redirect('encyclopedia:index')
        else:
            return redirect('encyclopedia:result', title = title)
        

def Result(request, title):
    matched = []
    for entry in util.list_entries():
        if title.lower() in entry.lower():
            matched.append(entry)
    if len(matched)>0 :
        return render(request, "encyclopedia/result.html" , {"entries" : matched})
    else :
        return render(request, 'encyclopedia/error.html', {"title" : title , "error" : 2})