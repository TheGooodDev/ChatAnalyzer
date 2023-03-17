import { Message } from "./message.js";

// Create an instance of XMLHttpRequest object
let p = document.querySelector("#chat-log");
let searchInput = document.querySelector("#search");

// Define the callback function to be executed when the response is received

let lastlength = 0

function getApi() {
    fetch("http://localhost:8000")
        .then((response) => {
            // Check if the response was successful
            if (response.ok) {
                // Convert the response to text
                return response.text();
            } else {
                // Handle error
                throw new Error("Error: " + response.status);
            }
        })
        .then((data) => {
            // Update the HTML element with the file contents
            let json_string = data;
            let res = JSON.parse(json_string);
            display(res)
        })
        .catch((error) => {
            // Handle error
            console.log(error.message);
        });
}

setInterval(getApi, 100)


function display(res) {
    cleanChat()
    let count = 0
    for (let i = 0; i < res.length; i++) {
        let span_message = document.createElement("span");
        span_message.classList.toggle(res[i].type);

        let span_time = document.createElement("span")
        span_time.classList.toggle("time");
        span_time.innerHTML = `[${res[i].time}] (${res[i].type})`
        span_message.appendChild(span_time)

        let span_user = document.createElement("span")
        span_user.classList.toggle("user");
        span_user.addEventListener("click", () => {
            navigator.clipboard.writeText(`/w ${res[i].user}`)
        })
        span_user.innerHTML = `${res[i].user} `
        span_message.appendChild(span_user)

        if (res[i].content.toLowerCase().includes(searchInput.value.toLowerCase()) && searchInput.value) {
            const re = new RegExp(`${searchInput.value}`,"gi")
            let tab = res[i].content.split(re)
            tab.forEach(function (sentence, idx) {
                span_message.appendChild(createMessageSpan(sentence))
                if (idx != tab.length - 1) {
                    count++
                    displayCount(count)
                    let searchWord = document.createElement("span")
                    searchWord.classList.toggle("searchWord");
                    searchWord.innerHTML = searchInput.value
                    span_message.appendChild(searchWord)
                }
            })
        } else {
            displayCount(count)
            span_message.appendChild(createMessageSpan(res[i].content))
        }

        p.insertBefore(span_message, p.firstChild);
    }
    lastlength = res.length
}

function createMessageSpan(content){
    let span_content = document.createElement("span")
    span_content.classList.toggle("content");
    span_content.innerHTML = content
    return span_content

}

function displayCount(count){
    document.querySelector("#count").innerHTML = count
}

function cleanChat() {
    while (p.firstChild) {
        p.removeChild(p.lastChild);
    }
}
