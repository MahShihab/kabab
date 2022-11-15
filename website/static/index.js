function addTOorder(itemID,inputID){
    // alert("Added");
    var el = document.createElement("div");
    el.setAttribute("style","position:fixed;top:10%;left:40%;background-color:black;color: white;;width:200px;height:50px;border-radius: 15px;text-align:center;padding:10px;");
    el.innerHTML = 'Added';
    setTimeout(function(){
     el.parentNode.removeChild(el);
    },1000);
    document.body.appendChild(el);
    
    const itemcount = document.getElementById(inputID).value;
    var value = [itemID,itemcount]
    localStorage.setItem(inputID, JSON.stringify(value));
    // var test = JSON.parse(localStorage.getItem(inputID));
    // alert(test);

    // const itemcount = document.getElementById(inputID).value;
    // fetch('/addItem', {
    //     method: 'POST',
    //     body: JSON.stringify({ itemID: itemID , itemcount: itemcount })
    // })
}

function viewOrder(){
    // alert("sdfds");  
    const MyID = [];
    const MyCount = [];
    const MyKeys = [];
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        // if(key == "tagSelected"){
        //     break;
        // }
        console.log(key);
        // console.log(`${key}: ${localStorage.getItem(key)}`)
        var test = JSON.parse(localStorage.getItem(key));
        console.log(key);
        MyKeys.push(key);
        MyID.push(test[0]);
        MyCount.push(test[1]);
        console.log(MyCount);
        console.log(MyID);
      }
     fetch('/viewOrder', {
         method: 'POST',
         body: JSON.stringify({ MyID: MyID , MyCount: MyCount , MyKeys: MyKeys })
     }).then((response)=>{
        return response.text();
    }).then((html)=>{
        document.body.innerHTML = html
    });
    //   console.log("clear");
    //   localStorage.clear();
}

function RemoveFromOrder(itemKey){
    console.log("itemKey");
    localStorage.removeItem(itemKey);
    const MyID = [];
    const MyCount = [];
    const MyKeys = [];
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        // if(key == "tagSelected"){
        //     break;
        // }
        console.log(key);
        // console.log(`${key}: ${localStorage.getItem(key)}`)
        var test = JSON.parse(localStorage.getItem(key));
        console.log(key);
        MyKeys.push(key);
        MyID.push(test[0]);
        MyCount.push(test[1]);
        // console.log(MyCount);
        // console.log(MyID);
      }
      fetch('/viewOrder', {
        method: 'POST',
        body: JSON.stringify({ MyID: MyID , MyCount: MyCount , MyKeys: MyKeys })
    }).then((response)=>{
       return response.text();
   }).then((html)=>{
       document.body.innerHTML = html
   });
}

function cancel(){
    console.log("clear");
    localStorage.clear();
    const MyID = [];
    const MyCount = [];
    const MyKeys = [];
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        // if(key == "tagSelected"){
        //     break;
        // }
        console.log(key);
        // console.log(`${key}: ${localStorage.getItem(key)}`)
        var test = JSON.parse(localStorage.getItem(key));
        console.log(key);
        MyKeys.push(key);
        MyID.push(test[0]);
        MyCount.push(test[1]);
        // console.log(MyCount);
        // console.log(MyID);
      }
      fetch('/viewOrder', {
        method: 'POST',
        body: JSON.stringify({ MyID: MyID , MyCount: MyCount , MyKeys: MyKeys })
    }).then((response)=>{
       return response.text();
   }).then((html)=>{
       document.body.innerHTML = html
   });
}

function deleteMyLocal(){
    console.log("clear");
    localStorage.clear();
    // fetch('/confirm',{
    //     method: 'POST',
    //     body: JSON.stringify({ OrderPrice : OrderPrice })
    //  })//.then((_res)=>{
    // //     window.location.href = "/rating";
    // // })
}

function ShowOrder(OrderNum,OrderID){
    fetch('/Home',{
        method: 'POST',
        body: JSON.stringify({ OrderNum : OrderNum , OrderID : OrderID })
    }).then((response)=>{
        return response.text();
    }).then((html)=>{
        document.body.innerHTML = html
    });
}

function Done(OrderID){
    fetch('/Done',{
        method: 'POST',
        body: JSON.stringify({ OrderID : OrderID })
    }).then((_res)=>{
        window.location.href = "/Home";
    })
}

function rate(rateValue){
    const star = document.getElementById(rateValue).value;
    fetch('/rate',{
        method: 'POST',
        body: JSON.stringify({ star : star })
    })
}

function special(){
    const special = document.getElementById("Op").value;
    const rival = document.getElementById("rival").value;
    fetch('/special',{
        method: 'POST',
        body: JSON.stringify({ special : special , rival:rival })
    })
}