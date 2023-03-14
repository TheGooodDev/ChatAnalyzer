import { Message } from "./message.js";

// Create an instance of XMLHttpRequest object
let p = document.querySelector("#chat-log");
let searchInput = document.querySelector("#search");

// Define the callback function to be executed when the response is received

let lastlength = 0

function getApi() {
    fetch("http://127.0.0.1:8000")
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


function display(res){
    cleanChat()
    for (let i = 0; i < res.length;i++){
        let span_message = document.createElement("span");
        span_message.classList.toggle(res[i].type);

        let span_time = document.createElement("span")
        span_time.classList.toggle("time");
        span_time.innerHTML =`[${res[i].time}] `
        span_message.appendChild(span_time)

        let span_user = document.createElement("span")
        span_user.classList.toggle("user");
        span_user.addEventListener("click",()=>{
            navigator.clipboard.writeText(`/w ${res[i].user}`)
        })
        span_user.innerHTML =`${res[i].user} `
        span_message.appendChild(span_user)

        if(res[i].content.toLowerCase().includes(searchInput.value.toLowerCase()) && searchInput.value){
            let span_content1 = document.createElement("span")
            span_content1.classList.toggle("content");
            let searchWord = document.createElement("span")
            searchWord.classList.toggle("searchWord");
            let span_content2 = document.createElement("span")
            span_content2.classList.toggle("content");
        }else{
            let span_content = document.createElement("span")
            span_content.classList.toggle("content");
            span_content.innerHTML =`${res[i].content}`
            span_message.appendChild(span_content)
        }

        p.insertBefore(span_message, p.firstChild);
    }
    lastlength = res.length
}

function cleanChat(){
    while (p.firstChild) {
        p.removeChild(p.lastChild);
    }
}
