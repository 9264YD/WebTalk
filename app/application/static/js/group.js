/* Send and receive message on the group chat page */

const chatbox = document.querySelector('#chatbox');
const inputBox = document.querySelector('#input-box');
const sendButton = document.querySelector('#send-button');
function pushcontent() {
    $.ajax({
        url: "/meet",
        type: "POST",
        data: $("#my-form").serialize(),
        success: function (response) {
            message = response.result
            const input = inputBox.value;
            if (!input.trim()) return;
            inputBox.value = '';
            { #chatbox.innerHTML += `<p class="user-message">${input}</p>`;# }
            chatbox.innerHTML += `<p class="ai-message">${message}</p>`;

            chatbox.scrollTop = chatbox.scrollHeight;
            console.log(response);
        },
        error: function (error) {
            console.log(error);
        }
    });
}