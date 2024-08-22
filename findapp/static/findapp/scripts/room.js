//+++++++++++++++++++++++++++++ EXPRESSION REGULIÈRE +++++++++++++++++++++++++++++//

function filterInput(input) {
    // Expression régulière pour autoriser uniquement les lettres, les chiffres, les caractères accentués, les tirets, les apostrophes, les accents circonflexes et les guillemets
    const regex = /[^\p{L}\p{N}\-'\s^¨]/gu;
    input.value = input.value.replace(regex, '');
}


//+++++++++++++++++++++++++++++++++++ TOOLTIP +++++++++++++++++++++++++++++++++++//
function showTooltipImage(rangeInput) {
    const tooltipImage = document.getElementById('tooltip-image');
    const tooltipImageContainer = document.getElementById('tooltip-image-container');

    // Définir les images pour chaque palier
    const images = {
        1: '/static/findapp/images/crying_emoji.png',
        2: '/static/findapp/images/sniffa_emoji.png',
        3: '/static/findapp/images/neutral_emoji.png',
        4: '/static/findapp/images/yum_emoji.png',
        5: '/static/findapp/images/happy_emoji.png'
    };

    // Obtenir la valeur actuelle du range
    const value = rangeInput.value;

    // Définir la source de l'image en fonction de la valeur
    tooltipImage.src = images[value];

    // Afficher l'image
    tooltipImage.style.display = 'block';

    // Masquer l'image après un court délai (par exemple, 2 secondes)
    setTimeout(() => {
        tooltipImage.style.display = 'none';
    }, 2000);
}

const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket(
    'wss://'
    + window.location.host
    + '/ws/findword/room/'
    + roomName
    + '/'
);

console.log(chatSocket);


//+++++++++++++++++++++++++++++++++++ RECEIVER +++++++++++++++++++++++++++++++++++//
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);
    
    if (data.message === 'start') {
        document.getElementById('find-word-form').submit();
    }

    if (data.message === 'ready_state') {
        const button = document.querySelector('#ready-button');
        if (data.state === 'notready') {
            button.textContent = 'pas prêt';
        } else {
            button.textContent = 'prêt';
        }
    }

    if (data.message === 'username') {
        const username = document.getElementById('username').value.trim();
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


//+++++++++++++++++++++++++++++++++++ HANDLER +++++++++++++++++++++++++++++++++++//
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

// Gestionnaire d'événement beforeunload pour gérer la déconnexion propre
window.addEventListener('beforeunload', function(event) {
    chatSocket.send(JSON.stringify({ 'message': 'disconnect' }));
});

// when page loads send a message to the server
chatSocket.onopen = function(e) {
    username = document.getElementById('username').value;
    chatSocket.send(JSON.stringify({ 
        'message': 'connect',
        'user': username
    }));
};


//+++++++++++++++++++++++++++++++++++ SENDER +++++++++++++++++++++++++++++++++++//
// Gestionnaire d'événement pour le bouton "Ready"
document.querySelector('#ready-button').onclick = function(e) {
    e.preventDefault();
    username = document.getElementById('username').value;
    console.log(username);
    const button = e.target;
    if (button.textContent === 'prêt') {
        state = 'notready';
        button.classList.replace('btn-green', 'btn-red');
        button.textContent = 'pas prêt';
    } else {
        state = 'ready';
        button.classList.replace('btn-red', 'btn-green');
        button.textContent = 'prêt';
    }
    chatSocket.send(JSON.stringify({
        'message': 'ready_state',
        'state': state,
        'user': username
    }));
};

// Gestionnaire d'événement pour le changement de valeur de l'input
document.querySelector('#rating-slider').addEventListener('input', function(e) {
    username = document.getElementById('username').value;
    const value = e.target.value;
    console.log(value);
    chatSocket.send(JSON.stringify({
        'message': 'rate',
        'note': value,
        'user': username
    }));
});