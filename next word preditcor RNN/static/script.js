const inpText = document.getElementById("inpText");
const charCount = document.getElementById("charCount");
const wordCount = document.getElementById("wordCount");
const predictedWord = document.getElementById("predictedWord");
const suggestionArea = document.getElementById("suggestions");

// Function to update character and word count
function updateCount() {
charCount.innerText = inpText.value.trim().length;
wordCount.innerText = inpText.value.replace(/\s+/g, ' ').trim().split(" ").length;
}

// Function to make AJAX request to Flask server for predictions
function makePrediction() {
    fetch('/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'text=' + encodeURIComponent(inpText.value),
    })
    .then(response => response.json())
    .then(data => {
      predictedWord.innerText = ' Predicted word: ' + data.predicted_word;
      predictedWord.style.fontSize = '20px'; 
    })
    .catch(error => console.error('Error:', error));
  }
// Event listeners
inpText.addEventListener("input", () => {
updateCount();
makePrediction();
});

uppercase.addEventListener("click", () => {
inpText.value = inpText.value.toUpperCase();
updateCount();
});

lowercase.addEventListener("click", () => {
inpText.value = inpText.value.toLowerCase();
updateCount();
});

extSpaces.addEventListener("click", () => {
inpText.value = inpText.value.replace(/\s+/g, ' ').trim();
updateCount();
});

extNewline.addEventListener("click", () => {
inpText.value = inpText.value.replace(/\s+/g, '\n').trim();
updateCount();
});

// Event listener for predicted word click
predictedWord.addEventListener("click", () => {
    const predictedWordText = predictedWord.innerText.split(":")[1].trim();
    if (predictedWordText) {
      inpText.value += predictedWordText + " ";
      updateCount();
      makePrediction();
    }
  });
  
  // Hover effect for predicted word
  predictedWord.addEventListener("mouseover", () => {
    predictedWord.classList.add("predicted-word-hover");
  });
  
  predictedWord.addEventListener("mouseout", () => {
    predictedWord.classList.remove("predicted-word-hover");
  });
  
  