from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Trip,Myuser,Package
from .form import Userlogin,Userregister,Planner
from django.views.generic import View,CreateView,UpdateView,DeleteView,ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
class Home(ListView):
    template_name = "myapp/home.html"
    context_object_name = "trips"
    def get_queryset(self):
        return Trip.objects.all()

class Logins(View):
    def get(self,request):
        x=Userlogin(None)
        return render(request, "myapp/login.html", {'form': x})
    def post(self,request):
        x = Userlogin(request.POST)
        if x.is_valid():
            user=x.cleaned_data.get('Username_Email')
            try:
                userobj=Myuser.objects.get(Username=user)
            except:
                userobj = Myuser.objects.get(email=user)
            response=redirect('myapp:userhome')
            response.set_cookie('username',user)
            return response
        return render(request, "myapp/login.html", {'form': x})

class Signup(View):
    def get(self,request):
        x=Userregister(None)
        return render(request, "myapp/register.html", {'form': x})
    def post(self,request):
        x = Userregister(request.POST)
        if x.is_valid():
            form=x.save(commit=False)
            pass1=x.cleaned_data.get('password')
            pass2=x.cleaned_data.get('confirm_password')
            if pass1==pass2:
                form.password=pass1
                form.save()
                return redirect('myapp:signin')
        return render(request, "myapp/register.html", {'form': x})

def myhome(request):
    try:
        user=request.COOKIES.get('username')
        try:
            userobj=Myuser.objects.get(Username=user)
        except:
            userobj = Myuser.objects.get(email=user)
        if userobj.agent:
            data = Package.objects.filter(u_id=userobj)
            return render(request, 'myapp/newagenthome.html', {'trip': data})
        else:
            data=Trip.objects.filter(u_id=userobj)
            return render(request,'myapp/newhome.html',{'trip':data})
    except Exception as e:
        print(e)
        return redirect('myapp:signin')

class Addpost(CreateView):
    model = Trip
    template_name = 'myapp/addtrip.html'
    fields = ["slug","discription",'date','duration','image']
    success_url = '/cetpa/home'
    def form_valid(self,form):
        self.object = form.save(commit=False)
        try:
            user = self.request.COOKIES.get('username')
            try:
                userobj = Myuser.objects.get(Username=user)
            except:
                userobj = Myuser.objects.get(email=user)
            if userobj.agent:
                return redirect('myapp:signin')
            else:
                self.object.u_id = userobj
                self.object.save()
        except:
            return redirect('myapp:signin')
        return super(Addpost, self).form_valid(form)

class Updatepost(UpdateView):
    model =Trip
    template_name = 'myapp/addtrip.html'
    fields = ["slug", "discription", 'date', 'duration', 'image']
    success_url = '/cetpa/home'

class Delpost(DeleteView):
    model = Trip
    success_url = reverse_lazy('myapp:userhome')
    template_name = 'myapp/addtrip.html'

class Addpack(CreateView):
    model = Package
    template_name = 'myapp/addtrip.html'
    fields = ["slug","location","description",'price','duration','image']
    success_url = '/cetpa/home'
    def form_valid(self,form):
        self.object = form.save(commit=False)
        try:
            user = self.request.COOKIES.get('username')
            try:
                userobj = Myuser.objects.get(Username=user)
            except:
                userobj = Myuser.objects.get(email=user)
            if userobj.agent:
                self.object.u_id = userobj
                self.object.save()
            else:
                return redirect('myapp:signin')
        except:
            return redirect('myapp:signin')
        return super(Addpack, self).form_valid(form)


class Updatepack(UpdateView):
    model =Package
    template_name = 'myapp/addtrip.html'
    fields = ["slug","location","description",'price','duration','image']
    success_url = '/cetpa/home'

class Delpack(DeleteView):
    model = Package
    success_url = reverse_lazy('myapp:userhome')
    template_name = 'myapp/addtrip.html'


class Pack(ListView):
    template_name = "myapp/package.html"
    context_object_name = 'pack'
    def get_queryset(self):
        return Package.objects.all()

class Plannerpost(View):
    def get(self,request):
        form=Planner(None)
        return render(request,'myapp/planner.html',{'form':form})
    def post(self,request):
        form = Planner(request.POST)
        if form.is_valid():
            price=form.cleaned_data.get("price")
            dur = form.cleaned_data.get("duration")
            loc = form.cleaned_data.get("location")
            val=Package.objects.filter(location__contains=loc,price__lte=price,duration__lte=dur)
            return render(request,'myapp/package.html',{'pack':val})
        return render(request, 'myapp/planner.html', {'form': form})
