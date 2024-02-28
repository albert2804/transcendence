<template>
	<div>
    <div class="offcanvas offcanvas-end" tabindex="-1" id="chatCanvas" aria-labelledby="chatCanvasLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="chatCanvasLabel">
          <i type="button" class="bi bi-question-circle clickable" style="font-size: 1.2em; margin-left: 5px;" @click="openHelpModal"></i>
          Chat
        </h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <!--  BODY -->
          <ul class="contacts-list nes-container">
            <div class="accordion" id="contactListAccordion">
            <div class="accordion-item clickable">
              <h2 class="accordion-header">
              <button class="accordion-button nes-container" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOnline" aria-expanded="true" aria-controls="collapseOnline">
                <span class="online-dot"/>&nbsp;Online
              </button>
              </h2>
              <div id="collapseOnline" class="accordion-collapse collapse show">
              <ul v-for="(user, index) in onlineUsers" :key="index" class="list-group">
                <li class="list-group-item" :class="{ 'active': this.chatid === user.id }" style="cursor: pointer;" 
                @click="selectUser(user)"
                >
                <ChatContact :user="user" :unreadMessageCountMap="unreadMessageCountMap" />
                </li>
              </ul>
              </div>
            </div>
            <div class="accordion-item clickable">
              <h2 class="accordion-header">
              <button class="accordion-button nes-container" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOffline" aria-expanded="true" aria-controls="collapseOffline">
                <span class="offline-dot"/>&nbsp;Offline
              </button>
              </h2>
              <div id="collapseOffline" class="accordion-collapse collapse show">
              <ul class="contacts-list">
                <ul v-for="(user, index) in offlineUsers" :key="index" class="list-group">
                <li class="list-group-item nes-container" :class="{ 'active': this.chatid === user.id }" style="cursor: pointer;" @click="selectUser(user)">
                  <ChatContact :user="user" :unreadMessageCountMap="unreadMessageCountMap" />
                </li>
                </ul>
              </ul>
              </div>
            </div>
            </div>
          </ul>
          <!-- CHATBOX -->
          <div v-show="chatid !== null" style="margin-top: 5px;">
          <div class="chat-container">
            <div class="header-bar clickable" @click="openProfile(active_chat_user.username)">
              <div class="row align-items-center">
                <div class="col-1">
                  <i class="bi bi-person-circle" style="font-size: 1.3em;"></i>
                </div>
                <div class="col-2">
                  {{ active_chat_user ? active_chat_user.username : '' }}
                </div>
              </div>
              <button type="button" class="btn-close" @click="this.chatid = null" aria-label="Close"></button>
            </div>
            <ul class="chat-messages">
              <li v-for="(message, index) in filteredMessages" :key="index" :class="getMessageType(message)">
                <span class="message" style="white-space: pre-line;">
                {{ JSON.parse(message).message }}
                <span class="date" style="font-size: 0.8em; text-align: right; display: block;">
                  {{ JSON.parse(message).date }}
                </span>
                </span>
      
              </li>
            </ul>
            <div class="chat-input-container">
              <input v-model="newMessage" type="text" placeholder="Type your message..." class="form-control chat-input" @keyup.enter="sendMessage" />
			        <button type="button" class="nes-btn is-primary send-button clickable" @click="sendMessage" style="font-size: 0.6em;">
              Send
              </button>
            </div>
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
      active_chat_user: null,
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
    // add event listener for offcanvas collapse
    const offcanvasElement = document.getElementById('chatCanvas');
    offcanvasElement.addEventListener('hidden.bs.offcanvas', this.handleOffcanvasCollapse);
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
  beforeUnmount() {
    // remove event listener for offcanvas collapse
    const offcanvasElement = document.getElementById('chatCanvas');
    offcanvasElement.removeEventListener('hidden.bs.offcanvas', this.handleOffcanvasCollapse);
  },
  methods: {
    openProfile(username) {
      this.$router.push({ path: '/userinfopage', query: { username: username } }).then(() => {
        this.$router.go();
      });
    },
    handleOffcanvasCollapse() {
      this.chatid = null;
    },
    openHelpModal() {
      this.$nextTick(() => {
        new bootstrap.Modal(document.getElementById('helpmodal')).show();
      });	
    },
    getMessageType (message) {
      const parsedMessage = JSON.parse(message)
      if (parsedMessage.subtype === 'info') {
        return 'message-item-info'
      } else if (parsedMessage.sender_id === this.own_id) {
        return 'message-item-sent'
      } else {
        return 'message-item-received'
      }
    },
    scrollDown () {
      this.$nextTick(() => {
        const container = this.$el.querySelector('.chat-messages')
        container.scrollTop = container.scrollHeight
      })
      // remove unread message count for selected chat
      if (this.unreadMessageCountMap.has(String(this.chatid))) {
        this.unreadMessageCountMap.delete(String(this.chatid));
      }
      // send read message info to server
      this.socket.send(JSON.stringify({ type: "read_info", chat_id: this.chatid }))
    },
    selectUser (user) {
      this.chatid = user.id
      this.active_chat_user = user
      this.scrollDown()
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
        if (this.newMessage.charAt(0) === '/') {
          this.socket.send(JSON.stringify({ type: "command", command: this.newMessage, receiver_id: this.chatid }))
        } else {
        this.socket.send(JSON.stringify({ type: "message", message: this.newMessage, receiver_id: this.chatid }))
        }
        this.newMessage = ''
      }
    }
  }
}
</script>

<style>
/* CONTACTS-CARD */

.contacts-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.accordion-header{
  padding: 0px;
}

.accordion-button {
  background-color: #ffffff;
  text-align: left;
  width: 100%;
  padding: 10px;
  margin: 0px;
  border-width: 4px;
  border-radius: 5px;
}

.accordion-button:focus {
  border-color: #000000;
  border-width: 4px;
  border-radius: 5px;
}

.list-group-item {
  padding: 0px;
  margin: 0;
  border-color: #000000;
  border-width: 3px;
}

.list-group-item.active {
  background-color: #ecedee;
  border-color: #000000;
  border-width: 3px;
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
  border: 1px solid #000000;
  border-width: 4px;
  border-radius: 0px;
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

.message-item-info {
  margin-bottom: 2px;
  margin-top: 2px;
  margin-left: 4px;
  margin-right: 4px;
  display: flex;
  justify-content: center;
  color: #007bff;
}

.message {
  background-color: #eeeeee;
  border-bottom: 1px solid #c8c8c8;
  border-width: 3px;
  padding: 8px;
  border-radius: 8px;
  display: inline-block;
  word-wrap: break-word;
  max-width: 80%;
  align-self: flex-end;
  font-size: 0.8em;
}

.date {
  color: #808080;
}

.chat-input-container {
  background-color: #d7d7d7;
  display: flex;
  align-items: center;
  padding: 8px;
}

.chat-input {
  flex-grow: 1;
  margin-right: 8px;
  font-size: 0.8em;
}

.send-button {
  width: 70px;
  font-size: 0.8em;
  margin-right: 8px;
  margin-top: 8px;
}


/* GENERAL */

.header-bar {
  background-color: #d7d7d7;
  color: #000000;
  padding: 10px;
  display: flex;
  justify-content: space-between;
}

</style>