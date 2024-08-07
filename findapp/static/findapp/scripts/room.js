function filterInput(input) {
    // Expression régulière pour autoriser uniquement les lettres et les chiffres
    const regex = /[^a-zA-Z0-9 ]/g;
    input.value = input.value.replace(regex, '');
}

const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/findword/room/'
    + roomName
    + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);
    
    if (data.message === 'start') {
        document.getElementById('find-word-form').submit();
    }

    if (data.message === 'ready_state') {
        const button = document.querySelector('#ready-button');
        if (data.state === 'notready') {
            button.value = 'ready';
        } else {
            button.value = 'notready';
        }
    }

    if (data.message === 'username') {
        const username = document.getElementById('username').textContent.trim();
        const player1_name = document.getElementById('player1').textContent.trim();
        const player2_name = document.getElementById('player2').textContent.trim();
        if (username !== data.user) {
            if (player1_name === '') {
                document.getElementById('player1').textContent = data.user;
            } else if (player2_name === '') {
                document.getElementById('player2').textContent = data.user;
            }
        }
    }
};

chatSocket.onclose = function(e) {
    if (e.code === 4000) {
        window.location.href = '/findword/lobby/';
        window.alert('Room is full. Redirecting to lobby...');
    } else if (e.code === 4001) {
        window.location.href = '/findword/lobby/';
        window.alert('You are already in the room. Redirecting to lobby...');
    } else {
        console.error('Chat socket closed unexpectedly');
        window.reload();
    }
};

// Gestionnaire d'événement pour le bouton "Ready"
document.querySelector('#ready-button').onclick = function(e) {
    const button = e.target;
    const state = button.value === 'notready' ? 'notready' : 'ready';
    chatSocket.send(JSON.stringify({
        'message': 'ready_state',
        'state': state
    }));
    button.value = state === 'notready' ? 'ready' : 'notready';
};

// Gestionnaire d'événement beforeunload pour gérer la déconnexion propre
window.addEventListener('beforeunload', function(event) {
    chatSocket.send(JSON.stringify({ 'message': 'disconnect' }));
});

// when page loads send a message to the server
chatSocket.onopen = function(e) {
    username = document.getElementById('username').textContent;
    chatSocket.send(JSON.stringify({ 
        'message': 'connect',
        'user': username
    }));
};