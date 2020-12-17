var query = window.location.search;
const urlParams = new URLSearchParams(query);

const sid = urlParams.get('sid');
const rid = urlParams.get('rid');

var toTheBottom = false;

var room_before_update = null;
var room = null;

window.setInterval('refresh()', 5000);

window.onscroll = function(ev) {
       if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
        toTheBottom = true;
       }else{
        toTheBottom = false;
    }
};

window.onload = function(ev){
    refresh();
}

function refresh(){
    var str = document.forms['message_sender'].text.value;

    if(str.replace(/\s+/, '').length == 0) {
        fetch('/api/room?server_id=' + sid + '&room_id=' + rid)
            .then(data => data.text())
            .then((text) => {
                room_before_update = room;
                room = JSON.parse(text);

                if(room != room_before_update){
                    reload(room_before_update, room);
                }
            })

        if(toTheBottom){
            window.scrollTo(0,document.body.scrollHeight);
        }
    }
}

function reload(ancient_room, new_room){
    if(new_room == null) {
        return;
    }

    var ancient_length = 0;
    if(ancient_room != null) ancient_length = ancient_room.messages.length;

    for(var i = ancient_length; i < new_room.messages.length; i++){
        var msg_box = document.createElement("div");
        msg_box.className = 'msg_box';

        var msg_sender = document.createElement("p");
        msg_sender.className = 'msg_sender';
        msg_box.appendChild(msg_sender);

        var msg_content = document.createElement("p");
        msg_content.className = 'msg_content';
        msg_box.appendChild(msg_content);

        msg_sender.innerHTML = new_room.messages[i].sender.name + " (" + new_room.messages[i].hour + ")";
        msg_content.innerHTML = new_room.messages[i].content;

        if(new_room.messages[i].url != ""){
            var msg_url = document.createElement("a");
            msg_url.className = 'msg_url';
            msg_url.appendChild(msg_content);
            msg_url.innerHTML = new_room.messages[i].url;
        }

        document.getElementById('channel_view').appendChild(msg_box);
    }
}