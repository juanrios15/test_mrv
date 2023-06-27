function toggleBold(checkbox) {
    var label = checkbox.parentNode;
    if (checkbox.checked) {
        label.classList.add("fw-bold");
    } else {
        label.classList.remove("fw-bold");
    }
}