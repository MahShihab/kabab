from asyncio.windows_events import NULL
from flask import Blueprint,render_template,redirect,url_for,flash,request,jsonify
from flask_login import login_manager,login_required,current_user
from .models import Admin,Order,OrderLine,Item,Rating
from datetime import date
from . import db
import json
from sqlalchemy.sql import func
import stripe

views = Blueprint('views',__name__) 

theItemname  = [] 
theItemprice = []
theItemcuont = []
theItemID = []
theItemKey = []
theItemPic = []
totalPrice: float=0
totalPriceSe:float = 0
global NumofItemsInO
NumofItemsInO = 0
OrderNum = 0
OrderNumUser = 0
ShowNameU = []
ShowNumU = []
ShowPriceU = []
ShowTypeU = []
# specialID = 0



@views.route('/')
def mainHome():
    # global specialID

    items = Item.query.all()
    platters = Item.query.filter_by(ItemType = "platters").all() 
    sandwiches = Item.query.filter_by(ItemType = "sandwiches").all() 
    salad = Item.query.filter_by(ItemType = "salad").all() 
    desserts = Item.query.filter_by(ItemType = "desserts").all() 
    kids = Item.query.filter_by(ItemType = "kids").all() 
    appelizers = Item.query.filter_by(ItemType = "appelizers").all() 
    sides = Item.query.filter_by(ItemType = "sides").all() 
    drinks = Item.query.filter_by(ItemType = "drinks").all() 
    Soup = Item.query.filter_by(ItemType = "Soup").all() 
    SI = Item.query.filter_by(Special = "yes").first() 

    return render_template("home.html",user=current_user,items = items , numberOfAllItems = len(items),
    Platters = platters , numOfPlatters = len(platters),
    Sandwiches = sandwiches , numOfSandwiches = len(sandwiches),
    Salad = salad , numOfSalad = len(salad),
    Desserts = desserts , numOfDesserts = len(desserts),
    Kids = kids , numOfKids = len(kids),
    Appelizers = appelizers , numOfAppelizers = len(appelizers),
    Sides = sides , numOfSides = len(sides),
    Drinks = drinks , numOfDrinks = len(drinks),
    Soup = Soup , numOfSoup = len(Soup),
    SI = SI)

@views.route('/Home')
@login_required
def admin():
    global OrderNum
    AllOrders = Order.query.filter_by(status = "sent").all() 
    platters = Item.query.filter_by(ItemType = "platters").all() 
    sandwiches = Item.query.filter_by(ItemType = "sandwiches").all() 
    salad = Item.query.filter_by(ItemType = "salad").all() 
    desserts = Item.query.filter_by(ItemType = "desserts").all() 
    kids = Item.query.filter_by(ItemType = "kids").all() 
    appelizers = Item.query.filter_by(ItemType = "appelizers").all() 
    sides = Item.query.filter_by(ItemType = "sides").all() 
    drinks = Item.query.filter_by(ItemType = "drinks").all()
    Soup = Item.query.filter_by(ItemType = "Soup").all()

    Avg_rate = db.session.query(func.avg(Rating.rate)).scalar()


    if Avg_rate:
        res = "{:.2f}".format(Avg_rate)
    else:
        res = 0    


    print("meawhh",res)

    return render_template("admin.html",user=current_user,
    Platters = platters , numOfPlatters = len(platters),
    Sandwiches = sandwiches , numOfSandwiches = len(sandwiches),
    Salad = salad , numOfSalad = len(salad),
    Desserts = desserts , numOfDesserts = len(desserts),
    Kids = kids , numOfKids = len(kids),
    Appelizers = appelizers , numOfAppelizers = len(appelizers),
    Sides = sides , numOfSides = len(sides),
    Drinks = drinks , numOfDrinks = len(drinks),
    Soup = Soup , numOfSoup = len(Soup),
    AllOrders = AllOrders,NumOfAllOrders = len(AllOrders),
    OrderNum = OrderNum , numberofLinesU = len(ShowNameU),
    ShowNameU=ShowNameU,ShowNumU=ShowNumU,ShowPriceU=ShowPriceU,ShowTypeU = ShowTypeU,
    res = res)

@views.route('/rating')
def rating():
    global OrderNumUser
    
    max_OId = db.session.query(func.max(Order.id)).scalar()

    if max_OId < 1000:
        OrderNumUser = max_OId
    else:
        OrderNumUser = max_OId%1000    

    return render_template("rateing.html",user=current_user,OrderNumUser = OrderNumUser )

@views.route('/viewOrder')
def viewOrder():
    global totalPrice
    totalPrice = 0

    for x in range(len(theItemprice)):
        totalPrice = totalPrice+theItemprice[x]


    return render_template("Order.html",user=current_user,NumofItemsInO = NumofItemsInO,theItemKey = theItemKey,theItemPic=theItemPic,
    totalPrice=totalPrice,theItemcuont=theItemcuont,theItemprice=theItemprice,theItemname=theItemname,theItemID = theItemID,numofItemOrdered = len(theItemID))


@views.route('/addItem',methods=['GET','POST'])
def Add_item():  
    theItemID.clear()
    theItemname.clear()
    theItemprice.clear()
    theItemcuont.clear() 
    theItemKey.clear()
    theItemPic.clear()
    
    MyIdANDCount = json.loads(request.data)
    ItemID = MyIdANDCount['MyID']
    ItemCount = MyIdANDCount['MyCount']
    ItemKey = MyIdANDCount['MyKeys']
    
    print(ItemID[0] , ItemCount[0] , "hhhhhhhhhhhhhhhhhhhh")  
    
    global NumofItemsInO
    NumofItemsInO = len(ItemCount)          

    Sitem = Item.query.filter_by(Special="yes").first() 
    specialID = Sitem.id 
    rivalval = Sitem.rival

    for x in range (len(ItemCount)):
        items = Item.query.filter_by(id=ItemID[x]).first()
        ItemName = items.ItemName
        ItemPrice = items.ItemPrice
        if (int(ItemID[x])  == int(specialID)):
          print("hhhhhhhhhhhhhhhhhhmeaw")
          ItemPrice = float(ItemPrice - (ItemPrice* rivalval/100))
        ItemPrice = ItemPrice * int(ItemCount[x])
        theItemID.append(ItemID)
        theItemname.append(ItemName)
        theItemprice.append(ItemPrice) 
        theItemcuont.append(ItemCount[x]) 
        theItemKey.append(ItemKey[x]) 
        theItemPic.append(items.pic)

    print(theItemname[0] , theItemprice[0] , theItemcuont[0] )
      
    return jsonify({})   

@views.route('/removeItem',methods=['POST'])
def Remove_item():
    theItemID.clear()
    theItemcuont.clear()
    theItemprice.clear()
    theItemname.clear()
    theItemKey.clear()
    theItemPic.clear()

    MyIdANDCount = json.loads(request.data)
    ItemID = MyIdANDCount['MyID']
    ItemCount = MyIdANDCount['MyCount']
    ItemKey = MyIdANDCount['MyKeys']
    
    # print(ItemID[0] , ItemCount[0] , "hhhhhhhhhhhhhhhhhhhh")  
    
    global NumofItemsInO
    NumofItemsInO = len(ItemCount)          

    Sitem = Item.query.filter_by(Special="yes").first() 
    specialID = Sitem.id 
    rivalval = Sitem.rival

    if (NumofItemsInO > 0):
        for x in range (len(ItemCount)):
            items = Item.query.filter_by(id=ItemID[x]).first()
            ItemName = items.ItemName
            ItemPrice = items.ItemPrice
            if (int(ItemID[x])  == int(specialID)):
              print("hhhhhhhhhhhhhhhhhhmeaw")
              ItemPrice = float(ItemPrice - (ItemPrice*rivalval/100))
            ItemPrice = ItemPrice * int(ItemCount[x])
            theItemID.append(ItemID)
            theItemname.append(ItemName)
            theItemprice.append(ItemPrice) 
            theItemcuont.append(ItemCount[x]) 
            theItemKey.append(ItemKey[x])
            theItemPic.append(items.pic) 

    # print(theItemname[0] , theItemprice[0] , theItemcuont[0] )
      
    return jsonify({})  


@views.route('/cancel')   
def cancel():
    global NumofItemsInO
    NumofItemsInO = 0
    theItemID.clear()
    theItemcuont.clear()
    theItemprice.clear()
    theItemname.clear()
    theItemKey.clear()
    theItemPic.clear()
    return jsonify({})      




@views.route('/ShowOrder',methods=['GET','POST'])   
def ShowOrder():
    print("jjjjjjjjjjjjjjjjjjjjjjjjjjj")
    ShowNameU.clear()
    ShowNumU.clear()
    ShowPriceU.clear()
    ShowTypeU.clear()
    # items = []
    OI = json.loads(request.data)
    OrderId = OI['OrderID']
    global OrderNum
    # global OrderNumUser
    OrderNum = OI['OrderNum']
    # OrderNumUser = OI['OrderNum']
    
    orderLine = OrderLine.query.filter_by(Order_id=OrderId).all()
    Sitem = Item.query.filter_by(Special="yes").first() 
    specialID = Sitem.id 
    rivalval = Sitem.rival

    for x in range(len(orderLine)):
        itemID=orderLine[x].Item_id 
        print(itemID,"hhhhhhhhhhhhhhhhhhhhhhhhhhh")
        items = Item.query.filter_by(id=itemID).first()
        ShowNumU.append(orderLine[x].ItemNum)
        if (int(itemID)  == int(specialID)):
           print("hhhhhhhhhhhhhhhhhhmeaw")
           ShowPriceU.append(items.ItemPrice -(items.ItemPrice*rivalval/100))
        else:
            ShowPriceU.append(items.ItemPrice)   
        ShowTypeU.append(items.ItemType)
        ShowNameU.append(items.ItemName)

    return jsonify({})  

@views.route('/Done',methods=['GET','POST'])   
def Done():
    global OrderNum
    OrderNum = 0

    OI = json.loads(request.data)
    OrderId = OI['OrderID']  

    doneOrder = Order.query.filter_by(id = OrderId).first()   
    doneOrder.status="done"
    db.session.commit()

    return jsonify({})


@views.route('/rate',methods=['GET','POST'])   
def rate():
    rate = json.loads(request.data)
    rateValue = rate['star']

    new_rate=Rating( rate = rateValue )
    db.session.add(new_rate)
    db.session.commit()

    return jsonify({})  


@views.route('/special',methods=['GET','POST'])   
def special():

    SID = json.loads(request.data)
    specialID = SID['special']
    rivalVal = SID['rival']

    print(specialID)

    SpecialO = Item.query.filter_by(Special = "yes").first() 

    if SpecialO:
        SpecialO.Special = "no"
        SpecialO.rival = 0

    SpecialO = Item.query.filter_by(id = specialID).first() 
    SpecialO.Special = "yes"
    SpecialO.rival = rivalVal
    db.session.commit()

    return jsonify({})        


@views.route('/confirm/<tata>/<toto>',methods=['GET','POST'])   
def confirm(tata,toto):
    print(tata,"hhhh",toto)

    totalPrice: float=0
    x=0
    IIDs = []
    ICs = []

    while(x < len(toto)):
        if toto[x].isnumeric():
            if toto[x+1].isnumeric():
                IIDs.append(int(float(toto[x])) * 10 + int(float(toto[x+1])))
                x = x+1
            else:
                IIDs.append(toto[x]) 
        x += 1           

    for x in range(len(tata)):
        if tata[x].isnumeric():
            ICs.append(tata[x])

    print(IIDs,"hhhh",ICs)   

    for x in range(len(IIDs)):
        TheItem = Item.query.filter_by(id = IIDs[x]).first()
        if(TheItem.Special == "yes"):
            totalPrice = totalPrice + float((TheItem.ItemPrice - (TheItem.ItemPrice  * TheItem.rival / 100)) * int(ICs[x]))
        else:    
            totalPrice = totalPrice + float(TheItem.ItemPrice * int(ICs[x]))
        pass  

    
    print ("hi")
    print ("hi")
    txt = "Amaount to pay" 

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'product_data': {
                        'name': txt,
                    },
                    'unit_amount': int(float(totalPrice*100)),
                    'currency': 'usd',
                },
                'quantity':1
            },
        ],
        payment_method_types=['card'],
        mode='payment',
        success_url=request.host_url + '/success',
        cancel_url=request.host_url + '/viewOrder',
    )
    print ("hi")
    return redirect(checkout_session.url)
    


@views.route('/success')
def success():
    global NumofItemsInO
    NumofItemsInO = 0
    global totalPrice
    OrderPrice =totalPrice
    new_Order=Order(status = "sent",OrderPrice=OrderPrice )
    db.session.add(new_Order)
    db.session.commit()
    max_OId = db.session.query(func.max(Order.id)).scalar()
    # Orders = db.session.query(Order).filter(Order.id == max_OId).all()

    # print("hjhjhj",theItemID[0][2])
    
    for x in range(len(theItemID)):
       new_OrderLine=OrderLine(Order_id = max_OId , Item_id = theItemID[0][x],ItemNum=theItemcuont[x] )
       db.session.add(new_OrderLine)
       db.session.commit()

    theItemID.clear()
    theItemcuont.clear()
    theItemprice.clear()
    theItemname.clear()
    theItemPic.clear()
    return redirect(url_for('views.rating'))


   