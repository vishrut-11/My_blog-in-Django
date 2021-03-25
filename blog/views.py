from django.shortcuts import redirect, render
from blog.models import Post, BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    allPost = Post.objects.all() 
    context = {'allPost' : allPost}
    return render(request, 'blogHome.html', context)

def blogPost(request, slug): 
    post=Post.objects.filter(slug=slug).first()
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    repDict = {}

    #reply handling 
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)
    # print(comments, replies)
    print(repDict)
    context={'post':post, 'comments': comments, 'user': request.user,'repDict': repDict} 
    return render(request, "blogPost.html", context)



# def postComment(request):
#     if request.method == "POST":
#         comment=request.POST.get('comment')
#         user=request.user
#         postSno =request.POST.get('postSno')
#         post= Post.objects.get(sno=postSno)
#         comment=BlogComment(comment= comment, user=user, post=post)
#         # comment.save()
#         messages.success(request, "Your comment has been posted successfully")
        

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
            
    return redirect(f"/blog/{post.slug}")





