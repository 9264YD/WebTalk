/* Add a click event listener to a reply button and toggles the display state of a reply form when clicked. */

document.getElementById('reply-btn-{{ loop.index }}').addEventListener('click', function () {
    var replyForm = document.getElementById('reply-form-{{ loop.index }}');
    if (replyForm.style.display === 'none') {
        replyForm.style.display = 'block';
    } else {
        replyForm.style.display = 'none';
    }
});