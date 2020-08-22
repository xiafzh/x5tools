

function query_data(data, cb_fun){
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "/index/queryqq", true);
	xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	xhr.setRequestHeader("Access-Control-Allow-Origin", "http://127.0.0.1");
	xhr.setRequestHeader("Access-Control-Allow-Credentials", "true");

	xhr.onreadystatechange = function(){
		var XMLHttpReq = xhr;
		if (XMLHttpReq.readyState == 4) {
			if (XMLHttpReq.status == 200) {                
				var data = XMLHttpReq.responseText;
				var json;
				try{
					json = JSON.parse(data)
				}
				catch(exception){
					console.log(data)
				}
				cb_fun(json);
			}else if(XMLHttpReq.status == 100){
			}else if(XMLHttpReq.status == 300){
			}else if(XMLHttpReq.status == 400){
			}else if(XMLHttpReq.status == 500){
			}else if(XMLHttpReq.status == 0){
			}
		}
	};
   xhr.send(JSON.stringify(data));
}

function setCookie(cname, cvalue){
	document.cookie = cname + "=" + cvalue + ";"
}

function getCookie(cname){
	var name = cname + "="
	var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name)==0) { return c.substring(name.length,c.length); }
    }
    return "";
}

function delCookie(name){ 
    var date=new Date(); 
    date.setTime(date.getTime()-10000); 
    document.cookie=name+"=v; expires="+date.toGMTString(); 
}
