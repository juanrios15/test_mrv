function toggleBold(checkbox) {
    var label = checkbox.parentNode;
    if (checkbox.checked) {
        label.classList.add("fw-bold");
    } else {
        label.classList.remove("fw-bold");
    }
}

function handleConfigClick(event) {
    event.preventDefault();
    var anonymousUser = localStorage.getItem('AnonymousUser');
    if (anonymousUser === 'true') {
        window.location.href = "/register";
    } else {
        window.location.href = event.target.href;
    }
}

function toggleKnowledgeBox() {
    var knowledgeBox = document.getElementById("knowledge_box");
    var button = document.getElementById("knowledge_btn");
    knowledgeBox.style.display = knowledgeBox.style.display === "none" ? "block" : "none";
    button.textContent = knowledgeBox.style.display === "none" ? "Knowledge" : "Hide Knowledge";
    button.classList.toggle("btn-success");
    button.classList.toggle("btn-secondary");
}