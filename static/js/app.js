var query = window.location.search;
const urlParams = new URLSearchParams(query);

const sid = urlParams.get('sid');
const rid = urlParams.get('rid');

var messages = [];
var msg_length = 0;

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
        fetch('/api/get_room?sid=' + sid + '&rid=' + rid + "&l=" + msg_length)
            .then(data => data.text())
            .then((text) => {
                new_messages = JSON.parse(text);
                
                if(new_messages.length != 0){
                    msg_length += new_messages.length;
                    reload(new_messages);
                    window.scrollTo(0,document.body.scrollHeight);
                }
            })
    }
}

function reload(new_messages){
    if(new_messages.length == 0) {
        return;
    }

    const view = document.getElementById('channel_view');

    for(var i = 0; i < new_messages.length; i++){
        var msg_box = document.createElement("div");
        msg_box.className = 'msg_box';

        var msg_sender = document.createElement("p");
        msg_sender.className = 'msg_sender';
        msg_box.appendChild(msg_sender);

        var msg_content = document.createElement("p");
        msg_content.className = 'msg_content';
        msg_box.appendChild(msg_content);

        msg_sender.innerHTML = new_messages[i].sender.name + " at " + new_messages[i].hour;
        msg_content.innerHTML = new_messages[i].content;

        if(new_messages[i].url != ""){
            var msg_url = document.createElement("a");
            msg_url.className = 'msg_url';
            msg_url.appendChild(msg_content);
            msg_url.innerHTML = new_messages[i].url;
        }

        view.appendChild(msg_box);
        messages.push(new_messages[i]);
    }

    //messages.push(new_messages);
}