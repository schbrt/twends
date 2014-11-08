var socket = io.connect('/data');

socket.on('connect', function() {
    console.log('Socket connection opened (Client).');
});

socket.on('disconnect', function() {
    console.log('Socket connection closed (Client).');
});

socket.on('event', function(msg) {
    console.log(msg)
    inner_set(msg.text)
});

inner_set = function(msg)  {
    document.getElementById("content").innerHTML = msg;
};

window.onload = function() {
    inner_set("loading")
};
