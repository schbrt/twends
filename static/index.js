var socket = io.connect('http://localhost:5000/data');

socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});
 socket.on('json', function(msg){
    console.log(msg);
});
