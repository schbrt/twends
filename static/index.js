var socket = io.connect('ws://localhost:5000/data');

socket.on('connect', function() {
    console.log('Socket connection opened (Client).');
});

socket.on('disconnect', function() {
    console.log('Socket connection closed (Client).');
});

socket.on('event', function(msg) {
    console.log(msg)
});
