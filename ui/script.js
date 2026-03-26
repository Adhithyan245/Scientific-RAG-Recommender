const API_BASE_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
    checkHealth();
    const form = document.getElementById("recommendation-form");
    form.addEventListener("submit", handleFormSubmit);
});

async function checkHealth() {
    const dot = document.getElementById("api-status-dot");
    const text = document.getElementById("api-status-text");

    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            dot.className = "dot online";
            text.textContent = "API Online";
        } else {
            throw new Error("API not OK");
        }
    } catch (error) {
        dot.className = "dot offline";
        text.textContent = "API Offline";
        console.error("Health check failed:", error);
    }
}

async function handleFormSubmit(event) {
    event.preventDefault();

    const form = event.target;
    const submitBtn = document.getElementById("submit-btn");
    const loading = document.getElementById("loading");
    const resultContainer = document.getElementById("result-container");
    const errorCard = document.getElementById("error-message");

    resultContainer.classList.add("hidden");
    errorCard.classList.add("hidden");
    
    const formData = new FormData(form);
    const payload = {
        research_objective: formData.get("research_objective").trim(),
        sample_type: formData.get("sample_type").trim(),
        domain: formData.get("domain").trim(),
        debug: formData.get("debug") === "on"
    };

    const sensitivity = formData.get("sensitivity").trim();
    if (sensitivity) payload.sensitivity = sensitivity;

    const resolution = formData.get("resolution").trim();
    if (resolution) payload.resolution = resolution;

    const constraints = formData.get("constraints").trim();
    if (constraints) payload.constraints = constraints;

    submitBtn.disabled = true;
    loading.classList.remove("hidden");

    try {
        const response = await fetch(`${API_BASE_URL}/recommend`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`API returned ${response.status}`);
        }

        const data = await response.json();
        renderResults(data);
    } catch (error) {
        console.error("Failed to fetch recommendation:", error);
        errorCard.textContent = "API Request Failed. Ensure the backend server is running and CORS is enabled.";
        errorCard.classList.remove("hidden");
    } finally {
        submitBtn.disabled = false;
        loading.classList.add("hidden");
    }
}

function renderResults(data) {
    const resultContainer = document.getElementById("result-container");
    resultContainer.classList.remove("hidden");

    const topRec = data.recommendations && data.recommendations.length > 0 
        ? data.recommendations[0] 
        : null;

    if (!topRec) {
        document.getElementById("res-instrument").textContent = "None Found";
        return;
    }

    // Top Result
    document.getElementById("res-instrument").textContent = topRec.instrument;
    document.getElementById("res-score").textContent = topRec.score.toFixed(2);
    document.getElementById("res-reasoning").textContent = topRec.reasoning;
    document.getElementById("res-limitations").textContent = topRec.limitations || "None specified.";
    document.getElementById("res-confidence-explanation").textContent = data.confidence_explanation || "";

    const altsContainer = document.getElementById("res-alternatives");
    altsContainer.innerHTML = "";
    if (topRec.alternatives && topRec.alternatives.length > 0) {
        topRec.alternatives.forEach(alt => {
            const span = document.createElement("span");
            span.className = "tag";
            span.textContent = alt;
            altsContainer.appendChild(span);
        });
    } else {
        altsContainer.textContent = "None typically recommended.";
        altsContainer.style.background = "transparent";
        altsContainer.style.padding = "0";
    }

    // Secondary Results
    const secondaryList = document.getElementById("secondary-recs-list");
    secondaryList.innerHTML = "";
    if (data.recommendations.length > 1) {
        for (let i = 1; i < data.recommendations.length; i++) {
            const rec = data.recommendations[i];
            const div = document.createElement("div");
            div.className = "secondary-item card";
            div.innerHTML = `
                <div class="secondary-header">
                    <h4>${rec.instrument}</h4>
                    <span class="score-badge secondary-score">Score: ${rec.score.toFixed(2)}</span>
                </div>
                <p class="secondary-reasoning">${rec.reasoning}</p>
            `;
            secondaryList.appendChild(div);
        }
    } else {
        secondaryList.innerHTML = "<p>No significant secondary alternatives found.</p>";
    }

    // Confidence
    const confidencePct = Math.round(data.confidence * 100);
    document.getElementById("res-confidence-text").textContent = `${confidencePct}%`;
    
    const fill = document.getElementById("res-confidence-fill");
    fill.style.width = "0%";
    setTimeout(() => {
        fill.style.width = `${confidencePct}%`;
        if (confidencePct >= 80) fill.style.backgroundColor = "var(--success)";
        else if (confidencePct >= 50) fill.style.backgroundColor = "var(--warning)";
        else fill.style.backgroundColor = "var(--error)";
    }, 100);

    // Warnings
    const warningsCard = document.getElementById("warnings-card");
    const warningsList = document.getElementById("res-warnings");
    warningsList.innerHTML = "";
    
    if (data.warnings && data.warnings.length > 0) {
        data.warnings.forEach(warning => {
            const li = document.createElement("li");
            li.textContent = warning;
            warningsList.appendChild(li);
        });
        warningsCard.classList.remove("hidden");
    } else {
        warningsCard.classList.add("hidden");
    }

    // Debug
    const debugCard = document.getElementById("debug-card");
    const debugContent = document.getElementById("debug-content");
    debugContent.innerHTML = "";
    if (data.debug_info) {
        debugContent.innerHTML = `
            <h4>Similarity Scores</h4>
            <pre>${JSON.stringify(data.debug_info.scores, null, 2)}</pre>
            <h4>Retrieved Chunks</h4>
            <pre>${JSON.stringify(data.debug_info.retrieved_chunks, null, 2)}</pre>
        `;
        debugCard.classList.remove("hidden");
    } else {
        debugCard.classList.add("hidden");
    }
}
