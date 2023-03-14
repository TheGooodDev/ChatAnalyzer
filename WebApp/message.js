export class Message {
    constructor(user, time, type, content) {
      this.user = user;
      this.time = time;
      this.type = type;
      this.content = content;
    }
  
    toString() {
      return `${this.time} ${this.user} ${this.content}`;
    }
  }