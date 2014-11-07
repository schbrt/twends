var socket = io.connect('http://localhost:5000/data');

socket.on('connect', function() {
    console.log('Socket connection opened (Client).');
});

socket.on('json', function(msg){
    console.log(msg);
});
