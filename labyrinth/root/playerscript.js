var ws;
var msgbuf = "";

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}

window.onload = function() {
  urlVars = getUrlVars();
  msgPrefixCar = '{ "tid":"car1", "component":'
  ws = new WebSocket("ws://"+hostname+":3000/ws");
  ws.onopen = function(e) {
    ws.send('{ "tid": "ctrl1", "init":"true" }');
  }
  ws.onmessage = function(e) {
    dispatchMsg(e.data);
  };
  
  $(document).on('input', '#white_led', function() {
      whiteLED();
  });
  $(document).on('input', '#laser', function() {
      laser();
  });
  $(document).on('input', '#servo_h', function() {
      servoHorizontal();
  });
  $(document).on('input', '#servo_v', function() {
      servoVertical();
  });
  $(document).on('click', '#led_uv', function() {
      ledUV();
  });
  $(document).on('click', '#switch_ir_code', function() {
      irCodeSimulation();
  });
  $(document).on('click', '#switch_ir_code_list', function() {
      irCodeList();
  });
  $(document).on('click', '#switch_off', function() {
      switchOff();
  });
  
}

function dispatchMsg(message) {
    console.log(message);
    if(!message.startsWith("{")) return;

    var msg = JSON.parse(message)
    if(msg.component == 'items') {
        if(msg.action == 'add') {
            addItem(msg)
        } else
        if(msg.action == 'rem') {
            remItem(msg)
        }
    }
}
function addItem(msg) {
    $("#items").append('<li id="'+msg.item+'" style="color:white;"><i class="fa-li fa fa-key" ></i>'+msg.item+'</li>');
}
function remItem(msg) {
    $('#'+msg.item).remove();
}


function updateStats(msg) {
    console.log(msg);
}
function playSound(name) {
    ws.send(msgPrefixCar + '"sound", "sound":"' + name + '" }\r');
}
function startCam() {
    ws.send(msgPrefixCar + '"cam", "action": "start" }\r');
}
function startGame() {
    ws.send('{ "tid": "ctrl1", "component": "showmessage", "text": "start"}\r');
}
function rfid(id, from, action) {
    ws.send('{ "tid":"rfid", "id":"'+id+'", "car":"'+from+'", "action":"'+action+'" }\r');
}
function move(id, l, r) {
    //ws.send('{ "tid":"'+id+'", "component":"base", "left":'+l+', "right":'+r+' }\r');
}
function whiteLED() {
    ws.send(msgPrefixCar + '"light", "type":"white", "intensity":"'+$('#white_led').val()+'" }\r');
}
function laser() {
    ws.send(msgPrefixCar + '"light", "type":"laser", "intensity":"'+$('#laser').val()+'" }\r');
}
function ledUV() {
    var val = '0';
   if($('#led_uv').prop("checked") == true){
       val = '1';
   }
   ws.send(msgPrefixCar + '"light", "type":"uv", "intensity":"'+val+'" }\r'); 
}
function servoHorizontal() {
    ws.send(msgPrefixCar + '"servo", "type":"h", "intensity":"'+$('#servo_h').val()+'" }\r');
}
function servoVertical() {
    ws.send(msgPrefixCar + '"servo", "type":"v", "intensity":"'+$('#servo_v').val()+'" }\r');
}
function irCodeSimulation() {
    ws.send(msgPrefixCar + '"ir", "code":"simulation" }\r');
}
function irCodeList() {
    ws.send(msgPrefixCar + '"ir" }\r');
}
function switchOff() {
    ws.send(msgPrefixCar+'"base", "switchoff":"true" }\r');
}
    