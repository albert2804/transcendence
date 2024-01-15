<template>
	<div>
    <!-- CONTAINER WITH CONTACTS... -->
    <div class="contacts-container">
      <div class="header-bar">
        <p class="m-0">
        Contacts
        </p>
        <button type="button" class="btn-close" @click="this.$emit('closeChat'); chatid = null;" aria-label="Close"></button>
      </div>
      <ul class="contacts-list">
        <div class="accordion" id="contactListAccordion">
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOnline" aria-expanded="true" aria-controls="collapseOnline">
                <span class="online-dot"/>&nbsp;Online
              </button>
            </h2>
            <div id="collapseOnline" class="accordion-collapse collapse show">
              <ul v-for="(user, index) in onlineUsers" :key="index" class="list-group">
                <li class="list-group-item" :class="{ 'active': this.chatid === user.id }" style="cursor: pointer;" @click="selectUser(user)">
                  <span class="badge rounded-pill bg-danger" v-if="unreadMessageCountMap.get(String(user.id)) != 0">
                    {{ unreadMessageCountMap.get(String(user.id)) }}
                  </span>
                  {{ user.username }}
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
                <ul v-for="(user, index) in offlineUsers" :key="index" class="list-group">
                  <li class="list-group-item" :class="{ 'active': this.chatid === user.id }" style="cursor: pointer;" @click="selectUser(user)">
                    <span class="badge rounded-pill bg-danger" v-if="unreadMessageCountMap.get(String(user.id)) != 0">
                      {{ unreadMessageCountMap.get(String(user.id)) }}
                    </span>
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
            </p>
            <button type="button" class="btn-close" @click="this.chatid = null" aria-label="Close"></button>
          </div>
          <ul class="chat-messages">
            <li v-for="(message, index) in filteredMessages" :key="index" :class="getMessageType(message)">
                <span class="message">
                  {{ JSON.parse(message).message }}
                  <span class="date" style="font-size: 0.8em; text-align: right; display: block;">
                    {{ JSON.parse(message).date }}
                  </span>
                </span>

            </li>
          </ul>
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
      unreadMessageCountMap: new Map(),
      newMessage: '',
      chatid: null,
      own_id: null
    }
  },
  computed: {
    filteredMessages() {
      return this.messages.filter(message => JSON.parse(message).chat_id == this.chatid);
    },
    onlineUsers() {
      return this.userlist.filter(user => user.chat_online);
    },
    offlineUsers() {
      return this.userlist.filter(user => !user.chat_online);
    },
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
    // watch for unread messages (in unreadMessageCountMap)
    watchEffect(() => {
      let totalUnreadMessages = 0;
      for (const count of this.unreadMessageCountMap.values()) {
        totalUnreadMessages += count;
      }
      this.$emit('unreadMessages', totalUnreadMessages);
    });
  },
  methods: {
    getMessageType (message) {
      const parsedMessage = JSON.parse(message)
      return parsedMessage.sender_id === this.own_id ? 'message-item-sent' : 'message-item-received'
    },
    scrollDown () {
      this.$nextTick(() => {
        const container = this.$el.querySelector('.chat-messages')
        container.scrollTop = container.scrollHeight
      })
    },
    selectUser (user) {
      this.chatid = user.id
      this.scrollDown()
      // remove unread message count for selected chat
      if (this.unreadMessageCountMap.has(String(user.id))) {
        this.unreadMessageCountMap.delete(String(user.id));
      }
      // send read message info to server
      this.socket.send(JSON.stringify({ type: "read_info", chat_id: user.id }))
    },
    createWebSocket () {
      const currentDomain = window.location.hostname;
      const sockurl = 'wss://' + currentDomain + '/endpoint/chat/';
      this.socket = new WebSocket(sockurl)

      this.socket.onopen = () => {
        this.$emit('loading')
      }

      this.socket.onclose = () => {
        this.$emit('disconnected')
        this.unreadMessageCountMap.clear()
      }

      this.socket.onerror = (error) => {
        console.error(`WebSocket-Error: ${error}`)
        this.$emit('disconnected')
        this.unreadMessageCountMap.clear()
      }

      this.socket.onmessage = (event) => {
        var data = JSON.parse(event.data);
        if (data.type === 'user_list') {
          this.own_id = data.own_id
          this.userlist = data.users.filter(user => user.id != this.own_id)
          this.$emit('connected')
        } else if (data.type === 'chat_message') {
          // add message to messages array
          this.messages.push(event.data)
          //
          const chatId = data.chat_id;
          const unread = data.unread;
          // scroll down if message is from current chat window
          if (this.chatid == chatId) {
            this.scrollDown()
          }
          // increase unread messages count if message is from other chat window
          else if (unread && chatId) {
            if (this.unreadMessageCountMap.has(chatId)) {
              this.unreadMessageCountMap.set(chatId, this.unreadMessageCountMap.get(chatId) + 1);
            } else {
              this.unreadMessageCountMap.set(chatId, 1);
            }
          }
        } else {
          console.log('unknown message type received')
        }
      }
    },
    closeWebSocket () {
      if (this.socket) {
        this.socket.close()
      }
      this.messages = []
      this.userlist = []
      this.chatid = null
      this.own_id = null
    },
    sendMessage () {
      if (this.newMessage.trim() !== '') {
        this.socket.send(JSON.stringify({ type: "message", message: this.newMessage, receiver_id: this.chatid }))
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

.date {
  color: #808080;
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