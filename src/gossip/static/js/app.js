document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("query-form");
    const resultsContainer = document.getElementById("results");

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        const query = document.getElementById("query").value;

        fetch("/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query: query })
        })
        .then(response => response.json())
        .then(data => {
            resultsContainer.innerHTML = "";
            data.results.forEach(result => {
                const resultElement = document.createElement("div");
                resultElement.innerHTML = `
                    <h3>${result.title}</h3>
                    <p>${result.summary}</p>
                    <a href="${result.link}" target="_blank">Read more</a>
                    <p>Similarity: ${result.similarity}</p>
                `;
                resultsContainer.appendChild(resultElement);
            });
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});