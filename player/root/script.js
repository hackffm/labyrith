var ws;
var msgbuf = "";
Number.prototype.map = function(in_min, in_max, out_min, out_max) {
  return (this - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
var rect;

window.onload = function() {
  ws = new WebSocket("ws://"+hostname+":9090/websocket");

  ws.onmessage = function(e) {
    dispatchMsg(e.data);
  };
  var canvas = document.getElementById("myCanvas");
  var ctx = canvas.getContext("2d");
  rect = canvas.getBoundingClientRect();
  var mdown = false;
  var pos;
  var width = canvas.offsetWidth;
  var height = canvas.offsetHeight;
  canvas.addEventListener("mousedown", inputStart, false);
  canvas.addEventListener("mouseup", inputEnd, false);
  canvas.addEventListener("mouseout", function(e) {
    mdown = false;
  }, false);
  canvas.addEventListener('mousemove', inputMove, false);
  canvas.addEventListener("touchstart", inputStart, false);
  canvas.addEventListener("touchend", inputEnd, false);
  canvas.addEventListener("touchmove", inputMove, false);

  
  resizeTouchArea();
  
  function inputStart() {
    mdown = true;
  }

  function inputEnd() {
    inputMove({
      clientX: Math.round(rect.width / 2 + rect.left),
      clientY: Math.round(rect.height / 2 + rect.top)
    });
    mdown = false;
  }

  function inputMove(e) {
    if (mdown) {
      if (e.touches && e.touches.length > 0) {
        pos = getMousePos(e.touches[0]);
      } else {
        pos = getMousePos(e);
      }

      centerPos(pos);
      //mapCenterPos(pos);
      toLeftRight(pos);
      printPos(pos);
      drawHandle(pos);
    }
  }

  function getMousePos(evt) {
    var pos = {
      x: Math.round(evt.clientX) - Math.round(rect.left),
      y: Math.round(evt.clientY) - Math.round(rect.top)
    };
    pos.ox = pos.x;
    pos.oy = pos.y;
    console.log("Mouse: " + pos.x + "   " + pos.y);
    return pos;
  }

  function centerPos(pos) {
    pos.cx = pos.x - rect.width / 2;
    pos.cy = rect.height / 2 - pos.y;
    console.log("cx: " + pos.cx + "   cy: " + pos.cy);
  }

  function toLeftRight(pos) {
    pos.left = Math.round(Math.min(pos.cy + pos.cx, width / 2));
    pos.right = Math.round(Math.min(pos.cy - pos.cx, height / 2));
    return pos;
  }

  function mapCenterPos(pos) {
    pos.cx = Math.round(pos.cx.map(0, rect.width / 2, 0, width / 2));
    pos.cy = 254 - Math.round(pos.cy.map(0, rect.height / 2, 0, height / 2));
  }

  function printPos(pos) {
    document.getElementById("xy").innerHTML = "x:" + pos.x + "  y:" + pos.y;
    document.getElementById("cxcy").innerHTML = "cx:" + pos.cx + "  cy:" + pos.cy;
	if(pos.left > 255) pos.left = 255;
	if(pos.left < -255) pos.left = -255;
	if(pos.right > 255) pos.right = 255;
	if(pos.right < -255) pos.right = -255;
    document.getElementById("lr").innerHTML = "l:" + pos.left + "  r:" + pos.right;
    ws.send("{ \"component\": \"base\", \"left\": " + pos.left + ", \"right\": " + pos.right + " }\r");
    console.log("l:" + pos.left + "   r:" + pos.right + "\r");
  }

  function drawHandle(pos) {
    ctx.clearRect(0, 0, rect.width, rect.height);
    var s = 10;
    ctx.fillRect(pos.ox - s / 2, pos.oy - s / 2, s, s);

    ctx.beginPath();
    ctx.moveTo(rect.width / 2, rect.height / 2);
    ctx.lineTo(pos.ox, pos.oy);
    ctx.stroke();
  }
  
  function resizeTouchArea() {
      var wh = $('#video').height();
      var ww = $('#video').width();
      
      var length = Math.min(wh, ww)/100*70;   
      
      var canvas = document.getElementById("myCanvas");
      canvas.style.top = wh/2-length/2+"px";
      canvas.style.left = ww/2-length/2+"px";
      canvas.style.width = length+"px";
      canvas.style.height = length+"px";
      
      var ctx = canvas.getContext("2d");
      ctx.canvas.width = length;
      ctx.canvas.height = length;
      
      rect = canvas.getBoundingClientRect();
      width = canvas.offsetWidth;
      height = canvas.offsetHeight;
  }
  
  window.onresize = resizeTouchArea;
}




function sendMsg() {
  ws.send(document.getElementById('msg').value  + "\r");
}

function echo() {
  ws.send("echo\r");
}

function soundSheep() {
    ws.send("s1\r");
}

function fetchStats() {
    //ws.send("V\r");
    //ws.send("v\r");
    ws.send("{ \"component\": \"stats\" }\r");
}

function dispatchMsg(msg) {
    var tokens = msg.split(':');
    if(msg.startsWith('V')) {
        document.getElementById('vbus').innerHTML = tokens[1];
    } else
    if(msg.startsWith('v')) {
        document.getElementById('vbat').innerHTML = tokens[1];
    } else {
        document.getElementById('out').value += msg;
    }
}
function updateStats(msg) {
    console.log(msg);
}
function playSound(name) {
    ws.send("{ \"component\": \"sound\", \"sound\": \"" + name + "\" }\r");
}
function startCam() {
    ws.send("{ \"component\": \"cam\", \"action\": \"start\" }\r");
}

function stopCam() {
    ws.send("{ \"component\": \"cam\", \"action\": \"stop\" }\r");
}
