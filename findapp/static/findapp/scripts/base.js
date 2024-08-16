document.addEventListener("DOMContentLoaded", () => {
    const bubblesContainer = document.getElementById("bubbles-container");
  
    function createBubble() {
      const bubble = document.createElement("div");
      bubble.className = "bubble";
  
      bubble.style.left = `${Math.random() * 100}%`;
  
      const size = Math.random() * 20 + 10;
      bubble.style.width = `${size}px`;
      bubble.style.height = `${size}px`;
  
      const animationDuration = Math.random() * 5 + 3;
      bubble.style.animationDuration = `${animationDuration}s`;
  
      bubblesContainer.appendChild(bubble);
  
      bubble.addEventListener("animationend", () => {
        bubble.remove();
      });
    }
  
    // Create new bublles each 3 seconds.
    setInterval(createBubble, 3000);
  });

//+++++++++++++++++++++++++++++++++++ MODAL +++++++++++++++++++++++++++++++++++//
var modal = document.getElementById("social-modal");
var btn = document.getElementById("open-modal");
var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
}

// Add event listener for the Esc key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' || event.key === 'Esc') {
      modal.style.display = "none";
    }
});