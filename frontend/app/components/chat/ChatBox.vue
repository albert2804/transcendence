<template>
	<div>
    <!-- CONTAINER WITH CONTACTS... -->
    <div class="contacts-container">
      <div class="header-bar">
        <p class="m-0">
        Chat
        </p>
        <button type="button" class="btn-close" @click="this.$emit('closeChat')" aria-label="Close"></button>
      </div>
      <ul class="contacts-list">
        <p class="text-center">Online:</p>
        <button class="btn" @click="this.chatid = 4">test</button>
        <p class="text-center">Offline:</p>
      </ul>
      <!-- CHATBOX -->
      <div v-show="chatid !== null" style="padding: 5px;">
        <div class="chat-container">
          <div class="header-bar">
            <p class="m-0">
            Online
            </p>
            <button type="button" class="btn-close" @click="this.chatid = null" aria-label="Close"></button>
          </div>
          <ul class="chat-messages">
            <li v-for="(message, index) in messages" :key="index" :class="getMessageType(message)">
            <span class="message">
              {{ JSON.parse(message).message }}
            </span>
            </li>
          </ul>
          <div v-show="showScrollButton === true" class="scroll-button" style="cursor: pointer;" @click="scrollDown">
            ⬇️{{ unseen }}
          </div>
          <div class="chat-input-container">
            <input v-model="newMessage" type="text" placeholder="Type your message..." class="form-control chat-input" @keyup.enter="sendMessage" />
            <button class="btn btn-primary send-button" @click="sendMessage">
            Send
            </button>
          </div>
        </div>
      </div>
    </div>
	</div>
</template>
  
<script>
import { isLoggedIn } from '~/store';
export default {
  name: 'ChatBox',

  data () {
    return {
      socket: null,
      messages: [],
      unseen: 0,
      showScrollButton: false,
      scrollEventListenerAdded: false,
      newMessage: '',
      chatid: null,
    }
  },
  mounted () {
    // watch for changes in isLoggedIn from store/index.js
    watchEffect(() => {
      if (isLoggedIn.value === 1) {
        this.createWebSocket();
      } else if (isLoggedIn.value === 0) {
        this.closeWebSocket();
      }
    });
  },
  methods: {
    getMessageType (message) {
      const parsedMessage = JSON.parse(message)
      // console.log(parsedMessage.sender_id)
      return parsedMessage.sender_id === '0' ? 'message-item-sent' : 'message-item-received'
    },
    checkScroll (event) {
      const container = event.target
      if (container.scrollTop + container.clientHeight >= container.scrollHeight) {
        this.showScrollButton = false
        this.unseen = 0
      }
    },
    scrollDown () {
      this.$nextTick(() => {
        const container = this.$el.querySelector('.chat-messages')
        container.scrollTop = container.scrollHeight
      })
      this.unseen = 0
      this.showScrollButton = false
    },
    createWebSocket () {
      const currentDomain = window.location.hostname;
      const sockurl = 'wss://' + currentDomain + '/endpoint/chat/';
      this.socket = new WebSocket(sockurl)

      this.socket.onopen = () => {
        console.log('opened chat websocket')
        this.$emit('connected')
      }

      this.socket.onclose = () => {
        console.log('closed chat websocket')
      }

      this.socket.onerror = (error) => {
        console.error(`WebSocket-Error: ${error}`)
      }

      this.socket.onmessage = (event) => {
        const container = this.$el.querySelector('.chat-messages')
        const isScrolledToBottom = container.scrollHeight - container.clientHeight <= container.scrollTop + 1
        this.messages.push(event.data)
        // console.log(event.data)
        if (isScrolledToBottom) {
          this.scrollDown()
        } else {
          this.showScrollButton = true
          this.unseen += 1
          if (!this.scrollEventListenerAdded) {
            this.$el.querySelector('.chat-messages').addEventListener('scroll', this.checkScroll)
            this.scrollEventListenerAdded = true
            console.log('added scroll event listener')
          }
        }
      }
    },
    closeWebSocket () {
      if (this.socket) {
        this.socket.close()
      }
      this.messages = []
      if (this.$el.querySelector('.chat-messages')) {
        this.$el.querySelector('.chat-messages').removeEventListener('scroll', this.checkScroll)
      }
    },
    sendMessage () {
      if (this.newMessage.trim() !== '') {
        this.socket.send(JSON.stringify({ message: this.newMessage }))
        this.newMessage = ''
      }
    }
  }
}
</script>

<style>
/* CONTACTS-CARD */

.contacts-container {
  background-color: #fff;
  display: flex;
  min-width: 250px;
  width: 350px;
  height: 90vh;
  border: 1px solid #ced4da;
  border-radius: 5px;
  overflow: hidden;
  margin-bottom: 10px;
  flex-direction: column;
}

.contacts-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}


/* CHAT-CARD */

.chat-container {
  background-color: #fff;
  position: relative;
  min-width: 250px;
  height: 50vh;
  flex-shrink: 1;
  border: 1px solid #ced4da;
  border-radius: 5px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.chat-messages {
  list-style-type: none;
  padding: 0;
  margin: 0;
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

/* used around message, to add margin */
.message-item-received {
  margin-bottom: 2px;
  margin-top: 2px;
  margin-left: 4px;
  margin-right: 4px;
  display: flex;
  justify-content: flex-start;
}

.message-item-sent {
  margin-bottom: 2px;
  margin-top: 2px;
  margin-left: 4px;
  margin-right: 4px;
  display: flex;
  justify-content: flex-end;
}

.message {
  background-color: #d7d7d7;
  border-bottom: 1px solid #ced4da;
  padding: 8px;
  border-radius: 8px;
  display: inline-block;
  word-wrap: break-word;
  max-width: 80%;
  align-self: flex-end;
}

/* The scroll down button that appears if you have unseen messages */
.scroll-button {
  position: absolute;
  left: 3%;
  top: 80%;
  z-index: 1;
}

.chat-input-container {
  background-color: #ebeaea;
  display: flex;
  align-items: center;
  padding: 8px;
}

.chat-input {
  flex-grow: 1;
  margin-right: 8px;
}

.send-button {
  width: 70px;
}


/* GENERAL */

.header-bar {
  background-color: #007bff;
  color: #fff;
  padding: 10px;
  display: flex;
  justify-content: space-between;
}

</style>