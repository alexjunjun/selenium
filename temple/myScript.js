/**
 * Created by bamboo.chen on 2017/11/22.
 */
function displayDate() {
    document.getElementById("date").innerHTML=Date();
}

function myFunction(){
    var tips,ret;
    var valu =document.getElementById("username").value;
    if (valu !=="" && valu !==null){
        tips = "输入的用户名:"+valu;
        ret = true;
    }else{
        tips = "用户名必填!"
        ret = false;
    }
    document.getElementById("demo").innerHTML=tips;
    return ret;
}

function numCheck(){
    var txt;
    obj = document.getElementById("num");
    console.log(obj.childNodes);
    if ( isNaN(obj.value)){
        document.getElementById("numtips").style.color="red";
        txt = "Num为非数字！"
    }else{
        if(obj.value==''){
            document.getElementById("numtips").style.color="red";
            txt = "Num为空！"
        }else {
            if (obj.validity.tooLong) {
                txt = "输入不能超过3位";
            } else {
                if (obj.validity.rangeUnderflow) {
                    document.getElementById("numtips").style.color = "red";
                    txt = "太小了";
                } else if (obj.validity.rangeOverflow) {
                    document.getElementById("numtips").style.color = "red";
                    txt = "太大了";
                } else {
                    txt = "正确";
                    document.getElementById("numtips").style.color = "green";
                }
            }
        }
    }

    document.getElementById("numtips").innerHTML=txt;

}


function bigImage(x) {
    x.style.height = "534px";
    x.style.width = "400px";

}

function nomalImage(x) {
    x.style.height = "267px";
    x.style.width = "200px";

}

function validateForm(){
    var x=document.forms["myForm"]["email"].value;
    var atpos=x.indexOf("@");
    var dotpos=x.lastIndexOf(".");
    if (atpos<1 || dotpos<atpos+2 || dotpos+2>=x.length){
        document.getElementById("emailtps").innerHTML="不是一个有效的 e-mail 地址";
        return false;
    }else{
        document.getElementById("emailtps").innerHTML="";
        return true;
    }
}

function changeBC(obj) {
    obj.style.backgroundColor='yellow';
    console.log( window.innerHeight,window.innerWidth,window.outerHeight,window.outerWidth);
}

function newelement() {
    ele = document.getElementsByTagName("body")[0];
    element = document.createElement("p");
    element.innerHTML="我是新创建的段落";
    ele.appendChild(element);

}

