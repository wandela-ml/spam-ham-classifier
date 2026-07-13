//DOM elements

const messageInput = document.getElementById("message");
const predictButton = document.getElementById("predict-btn");
const clearButton = document.getElementById("clear-btn");
const resultArea = document.getElementById("result");

//predict button event listener
predictButton.addEventListener("click", async () =>{
    const text = messageInput.value.trim();
    if (!text){
        resultArea.innerHTML = "Please type or paste your message....";
        return;
    }
    resultArea.innerHTML = "Analyzing...";
    
    

    try {
            predictButton.disabled = true;
            predictButton.textContent = "Analyzing...";

            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: text })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            
            if (data.prediction === 1) {
                resultArea.className = "result-box result-spam";
                resultArea.innerHTML = `
                <div>
                    <h2>🚨 SPAM</h2>
                    <p>This message appears to be spam.</p>
                </div>
            `;
            } else {
                resultArea.className = "result-box result-ham";
                resultArea.innerHTML = `
                <div>
                    <h2>✅ HAM</h2>
                    <p>This message appears to be legitimate.</p>
                </div>
             `;
                }
            
        } catch (error) {
            console.error('Error:', error);
            resultArea.innerHTML = "Error fetching prediction. Please try again.";
        }
        finally{
            predictButton.disabled = false;
            predictButton.textContent = "predict"
        }
    });
    messageInput.addEventListener("keydown", (event) =>{
        if(event.key==="Enter" && !event.shiftKey){
            event.preventDefault(); //prevent a new line
            predictButton.click(); //Trigger the same prediction
        }

    })

    // Clear Button Event Listener
    clearButton.addEventListener('click', () => {
        messageInput.value = "";
        resultArea.innerHTML = "Your prediction results will appear Here.";
    });

