//++++++++++++++++++++++++++++ BULLES ++++++++++++++++++++++++++++//
var bubbleCount = 30;
var bubbleField = document.getElementById("bubble-field");

//generate bubbles with randomly timed animation durations
for (i = 0; i < bubbleCount; i++) {
  var randNum = Math.floor(Math.random() * 20) + 1;
  var animDur = 2 + (0.5 * randNum);
  moveEl = document.createElement('div');
  moveEl.setAttribute('class', 'bubble-rise');
  moveEl.setAttribute('style', 'animation-duration: ' + animDur + 's;');
  
  bubbleEl = document.createElement('div');
  bubbleEl.setAttribute('class', 'bubble');
  bubbleElContent = document.createTextNode('');
  bubbleEl.appendChild(bubbleElContent);
  
  moveEl.appendChild(bubbleEl)
  bubbleField.appendChild(moveEl);
}

//++++++++++++++++++++++++++++ POISSONS ++++++++++++++++++++++++++++//
document.addEventListener('DOMContentLoaded', function() {
  var fishes = document.querySelectorAll('.fish');
  fishes.forEach(function(fish) {
      var randomDuration = (Math.floor(Math.random() * 23) + 4) * 5; // Random duration between 20s and 130s, multiples of 5
      var randomLeft = Math.floor(Math.random() * 17) * 5; // Random left between 0vw and 80vw, multiples of 5
      var randomBottom = (Math.floor(Math.random() * 13) + 4) * 5; // Random bottom between 20vh and 80vh, multiples of 5

      //console.log(randomDuration, randomBottom, randomLeft);
      fish.style.left = randomLeft + 'vw';
      fish.style.bottom = randomBottom + 'vh';
      fish.style.animation = `fish ${randomDuration}s cubic-bezier(0.9, 1, 0.3, 0.75) 0s infinite normal`;
  });
});


