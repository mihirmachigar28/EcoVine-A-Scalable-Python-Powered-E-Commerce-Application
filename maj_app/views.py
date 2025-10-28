from django.contrib.auth.models import User 
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

from maj_app.models import *

from random import randrange
from django.views.decorators.http import require_POST
import razorpay

from django.db.models import Q


from maj_app.models import *
print(saved.objects.all())

# def home(request):
#     context = {}
#     p = plants.objects.all()
#     context['plants'] = p
#     return render(request,'index.html',context)

def home(request):
    context = {}
    query = request.GET.get('q')

    if query:
        p = plants.objects.filter(Q(Name__icontains=query) | Q(description__icontains=query))
        context['search_query'] = query
    else:
        p = plants.objects.all()
    
    context['plants'] = p
    return render(request, 'index.html', context)

    





def user_login(request):
    if request.method == 'POST':
        uname =request.POST.get('uname')
        upsw = request.POST.get('upsw')
        context = {}
        if uname == "" or upsw == "":
            context["errormsg"] = 'Fields can not be empty'
            return render(request,'login.html',context)
        else:
            u = authenticate(username=uname, password=upsw)
            # print(u)
            if u is not None:
                login(request,u)
                return redirect("index")
            else:
                context["errormsg"] = "Invalid username and password"
                return render(request,'login.html',context)
    else:
        return render(request,"login.html")

def user_register(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        uemail = request.POST.get('uemail')
        upsw = request.POST.get('upsw')
        ucpsw = request.POST.get('ucpsw')
        context = {}
        if uname == "" or uemail == "" or upsw == "" or ucpsw == "":
            context["errormsg"] = "Field can not be empty" 
            return render(request,'register.html',context)
        elif upsw != ucpsw:
            context["errormsg"] = "password and confirm password didn't match"
            return render(request,'register.html',context)
        else:
            try:
                u = User.objects.create(username=uname,password=upsw,email=uemail)
                u.set_password(upsw)
                u.save()
                context["success"] = "User created successfully"
                return render(request,'register.html',context)
            except Exception:
                context["errormsg"]="User with same Username already present"
                return render(request, "register.html",context)
    else:
        return render(request,"register.html") 
    

def user_logout(request):
    logout(request)
    return redirect('index')


def product_details(request,pid):
    context = {}
    p = plants.objects.get(id = pid)
    context["plants"] = p
    return render(request, "product_details.html",context)


def addtocart(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    user = request.user
    product = plants.objects.get(id=pid)
    
    context['plants'] = product

    exists = cart.objects.filter(uid=user, pid=product).exists()

    if exists:
        context['errmsg'] = "This Product is already in your Cart !!"
    else:
        cart.objects.create(uid=user, pid=product)
        context['success'] = "Product added to Your Cart Successfully!"

    return render(request, "product_details.html", context )

def cart_view(request):
    context = {}
    t = 0
    uid = request.user.id
    c = cart.objects.filter(uid = uid)
    np = len(c)
    for p in c:
        t = t+ p.pid.discount_price * p.qty
    context['plants'] = c
    context['n'] = np
    context['total'] = t
    return render(request, 'cart.html',context)

def updateqty(request, qv,cid):
    cart_items = cart.objects.filter(id=cid)

    if not cart_items:
        return redirect('cart')
    
    cart_item = cart_items[0] # get the single cart object

    if qv == '1':
        #Increase qantity by 1
        cart_item.qty = cart_item.qty + 1
        cart_item.save()
    else:
        #Decrese qantity by 1 only if quantity is more than 1
        if cart_item.qty > 1:
            cart_item.qty = cart_item.qty - 1
            cart_item.save()
    return redirect('cart')

def removepc(request,cid):
    c = cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')

def placeorder(request):
    context = {}
    userid = request.user.id
    c = cart.objects.filter(uid=userid)
    print(c)
    oid = randrange(1000, 99909)
    for x in c:
        o = Order.objects.create(order_id=oid, pid=x.pid, uid=x.uid, qty=x.qty)
        o.save()
        x.delete()

    orders = Order.objects.filter(uid=request.user.id, order_id=oid)
    context['product'] = orders
    np = len(orders)
    s = 0
    for p in orders:
        s = s + p.pid.discount_price * p.qty
    context['total'] = s
    context['n'] = np     

    return render(request, "place_order.html", context)

def pay(request):
    context = {}
    s = 0

    orders = Order.objects.filter(uid=request.user.id).order_by('-order_id')

    if orders:
        oid = orders[0].order_id  
        orders = Order.objects.filter(uid=request.user.id, order_id=oid)

        for p in orders:
            s = s + p.pid.discount_price * p.qty

        client = razorpay.Client(auth=("#", "#"))
        data = { "amount": s * 100, "currency": "INR", "receipt": "order_rcptid_" + str(oid) }
        payment = client.order.create(data=data)
        print(payment)
        context['data'] = payment

    return render(request, 'pay.html', context)

def add_to_saved(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    product = plants.objects.get(id=pid)

    exists = saved.objects.filter(uid=user, pid=product).exists()

    context = {"plants": product}
    
    if exists:
        context['errmsg'] = "This plant is already saved!"
    else:
        saved.objects.create(uid=user, pid=product)
        context['success'] = "Plant saved successfully!"

        print("Saved item created:", product.Name)

    return render(request, "product_details.html", context)


def view_saved(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    saved_items = saved.objects.filter(uid=user).select_related('pid')

    print("Current user:", request.user)
    print("Saved items found:", saved_items)

    print("Saved items:", saved_items)

    context = {
        'saved_plants': saved_items
    }
    return render(request, "saved.html", context)

def contactus(request):
    return render(request, 'contactus.html')
