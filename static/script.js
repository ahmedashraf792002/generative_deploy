document.getElementById('textForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const inputText = document.getElementById('inputText').value;
    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sequence: inputText })
    });
    
    const result = await response.json();
    document.getElementById('generatedText').textContent = result.generated_text;
});
