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