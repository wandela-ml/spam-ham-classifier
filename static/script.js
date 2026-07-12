console.log("Javascript loaded successfully!");

const clearButton = document.getElementById("clear-btn");
const button = document.getElementById("predict-btn");

button.addEventListener("click", async () => {

    const message = document.getElementById("message").value;

    if (message.trim() === "") {
        alert("Please enter a message.");
        return;
    }

    const result = document.getElementById("result");

    result.innerHTML = "Predicting...";

    const response = await fetch("/predict", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message
        })
    });

    const data = await response.json();

    if (data.prediction === 1) {
        result.innerHTML = "🚨 SPAM";
        result.style.color = "red";
    } else {
        result.innerHTML = "✅ HAM";
        result.style.color = "green";
    }
    const textarea = document.getElementById("message");
    textarea.focus();
    textarea.select();

});
// Clear Button Event Listener
    clearButton.addEventListener('click', () => {
        message.value = "";
        result.innerHTML = "Your prediction results will appear Here.";
    });