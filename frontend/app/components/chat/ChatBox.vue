<template>
	<div>
    <!-- CONTAINER WITH CONTACTS... -->
    <div class="contacts-container">
      <div class="header-bar">
        <p class="m-0">
        Contacts
        </p>
        <button type="button" class="btn-close" @click="this.$emit('closeChat')" aria-label="Close"></button>
      </div>
      <ul class="contacts-list">
        <div class="accordion" id="contactListAccordion" v-if="userlist && userlist.length > 0">
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOnline" aria-expanded="true" aria-controls="collapseOnline">
                <span class="online-dot"/>&nbsp;Online
              </button>
            </h2>
            <div id="collapseOnline" class="accordion-collapse collapse show">
                  <ul v-for="(user, index) in userlist" :key="index" class="list-group">
                    <li class="list-group-item" :class="{ 'active': this.chatid === user.id }" v-if="user.chat_online" style="cursor: pointer;" @click="this.chatid = user.id">
                      {{ user.username }}
                      <!-- <span class="badge bg-primary rounded-pill">23</span> -->
                    </li>
                </ul>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOffline" aria-expanded="true" aria-controls="collapseOffline">
                <span class="offline-dot"/>&nbsp;Offline
              </button>
            </h2>
            <div id="collapseOffline" class="accordion-collapse collapse show">
                <ul class="contacts-list">
                  <ul v-for="(user, index) in userlist" :key="index" class="list-group">
                    <li class="list-group-item" :class="{ 'active': this.chatid === user.id }" v-if="!user.chat_online" style="cursor: pointer;" @click="this.chatid = user.id">
                      {{ user.username }}
                    </li>
                  </ul>
                </ul>
            </div>
          </div>
        </div>
      </ul>
      <!-- CHATBOX -->
      <div v-show="chatid !== null" style="padding: 5px;">
        <div class="chat-container">
          <div class="header-bar">
            <p class="m-0">
            <!-- {{ userlist.find(user => user.id === chatid).username }} -->
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
      userlist: [],
      messages: [],
      unseen: 0,
      showScrollButton: false,
      scrollEventListenerAdded: false,
      newMessage: '',
      chatid: null,
      own_id: null
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
      return parsedMessage.sender_id === this.own_id ? 'message-item-sent' : 'message-item-received'
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
        // check if type is user_list
        var data = JSON.parse(event.data);
        if (data.type === 'user_list') {
          // console.log('user list received');
          // get own_id from user_list and put rest of user_list in userlist
          this.own_id = data.own_id
          this.userlist = data.users.filter(user => user.id != this.own_id)
          // this.userlist = data.users
          // console.log(data.users)
          console.log('user list received');
        } else if (data.type === 'chat_message') {
          let sender_id = data.sender_id
          // console.log(sender_id)
          if (sender_id !== this.own_id) {
            let sender_username = this.userlist.find(user => user.id == sender_id).username
            console.log('message received from ' + sender_username)
          }
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

.online-dot {
  height: 10px;
  width: 10px;
  background-color: #02ce02;
  border-radius: 50%;
  display: inline-block;
}

.offline-dot {
  height: 10px;
  width: 10px;
  background-color: #FF0000;
  border-radius: 50%;
  display: inline-block;
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