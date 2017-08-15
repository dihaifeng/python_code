from django.shortcuts import render,HttpResponse,redirect
import os

# Create your views here.
#User_Dict = {
#    'k1':'admin',
#    'k2':'guest',
#    'k3':'devlop',
#    'k4':'test'
#}

User_Dict = {
    '1':{'name':'admin','email':'admin@weibo.com'},
    '2':{'name':'guest','email':'guest@weibo.com'},
    '3':{'name':'devlop','email':'devlop@weibo.com'},
    '4':{'name':'test','email':'test@weibo.com'}
}

def index(request):
    return render(request,'index.html',{'user_dict':User_Dict})


#基于get请求以?分割来获取数据
#def detail(request):
#    nid = request.GET.get('nid')
#    detail_info = User_Dict[nid]
#    return render(request,'detail.html',{'detail_info':detail_info})

#def detail(request,nid):    #如果是(\d+)就是用*args,如果使用分组的话，使用**kwargs
#    detail_info = User_Dict[nid]
#    return render(request,'detail.html',{'detail_info':detail_info})

"""
def login(request):
    if request .method == "GET":
        return render(request,'login.html')
    elif request.method == "POST":
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        if u == 'haifeng18' and p == '123456':
            return redirect('/index')
        else:
            return render(request,'login.html')
    else:
        return redirect('/index')    # redirect跳转界面
"""

def login(request):
    if request .method == "GET":
        return render(request,'login.html')
    elif request.method == "POST":
        #radio
        #v =  request.POST.get('gender')
        #print(v)

        #checkbox
        #v = request.POST.getlist('favor')   #获取多个值，列表
        #print(v)

        obj = request.FILES.get('fa')     #上传文件
        file_path = os.path.join('upload',obj.name)
        f = open(file_path,mode="wb")

        for i in obj.chunks():
            f.write(i)
        f.close()


        return render(request, 'login.html')
    else:
        return redirect('/index')

from django.views import View

class Home(View):
    def dispatch(self, request, *args, **kwargs):
        #super调用父类中的dispatch方法
        result = super(Home, self).dispatch(request,*args,**kwargs)
        return result


    def get(self,request):
        return render(request,'home.html')

    def post(self,request):
        return render(request, 'home.html')
