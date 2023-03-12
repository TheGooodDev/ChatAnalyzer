import { Message } from "./message.js";

// Create an instance of XMLHttpRequest object
let p = document.querySelector("#chat-log");

// Define the callback function to be executed when the response is received

fetch("chatLog.txt")
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
    res.reverse().forEach((message) => {
      let span_message = document.createElement("span");
      span_message.classList.toggle(message.type);
      span_message.innerHTML = `[${message.time}] ${message.user} ${message.content}`;
      p.appendChild(span_message);
    });
  })
  .catch((error) => {
    // Handle error
    console.log(error.message);
  });
