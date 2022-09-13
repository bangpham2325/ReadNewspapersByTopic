<template>
  <div class="chat">
    <div class="chat__body" id="container">
      <el-scrollbar ref="scrollbarRef" height="500px">
        <div ref="scrollbarInnerRef">
          <div v-for="chat in this.chats" :key="chat.key">
            <div :class='`chat__message ${isMe(chat) && "chat__receiver"}`' v-if="chat.username">
              <p style="color: #6D7C90">{{ chat.username }}</p>
              <p style="word-break: break-word">{{ chat.message }}</p>
            </div>
          </div>
        </div>
      </el-scrollbar>

      <div class="chat__footer">
        <textarea
          rows="1"
          autosize
          v-model="message"
          class="textarea mb-4 mt-6"
          placeholder="Press enter to reply"
          @keydown.enter.shift.exact.prevent=""
          @keydown.enter.exact.prevent="onSubmit"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';
import {onMounted, ref} from 'vue';
import {useRoute} from 'vue-router';
import {database, ref as dbRef, onValue, push} from '@/firebase'
import {equalTo, query, orderByChild, get} from '@firebase/database';
import {mapGetters} from "vuex";

@Options({
  computed: {
    ...mapGetters("user", ["userInfo"]),
  },
  props: {
    chatRoomId: ""
  },
  data() {
    return {
      chats: [''],
      firebase_room_id: null,
      avatar: null,
      friend: {},
      route: useRoute(),
      email: null,
      message: "",
    }
  },
  watch: {
    chats: {
      deep: true,
      handler() {
        setTimeout(() => {
          let maxScrollHeight = this.$refs.scrollbarInnerRef.clientHeight-380
          this.$refs.scrollbarRef.setScrollTop(maxScrollHeight)
        }, 500)
      },
    }
  },
  methods: {
    onSubmit() {
      push(dbRef(database, 'chatrooms/' + this.firebase_room_id + '/chats'), {
        username: this.userInfo.full_name,
        email: this.userInfo.email,
        message: this.message
      });
      this.message = "";
    },
    isMe(chat: any) {
      return chat.email == this.email;
    },
    getPreviousChats(roomId: string) {
      onValue(dbRef(database, 'chatrooms/' + roomId + '/chats'), (snapshot) => {
        this.chats = []
        snapshot.forEach((doc) => {
          let item = doc.val();
          this.chats.push(item);
        })
      })
    },
    async getRoomName(room_id: string) {
      const que = await query(dbRef(database, 'chatrooms/'), orderByChild('room_id'), equalTo(room_id))
      get(que).then((snapshot: any) => {
        this.firebase_room_id = Object.keys(snapshot.val())[0]
        this.getPreviousChats(this.firebase_room_id)
        return Object.keys(snapshot.val())[0]
      })
    },
  },
  mounted() {
    this.getRoomName(this.chatRoomId)
    this.email = this.userInfo.email
  },
})

export default class ChatSection extends Vue {
}

</script>


<style scoped>
.chat {
  flex: 0.70;
  display: flex;
  flex-direction: column;
}

.chat__header {
  padding: 20px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid lightgray;
}

.chat__headerInfo {
  flex: 1;
  padding-left: 20px;
}

.chat__headerInfo > h3 {
  margin-bottom: 3px;
  font-weight: 500;
}

.chat__headerInfo > p {
  color: gray;
}

.chat__headerRight {
  display: flex;
  justify-content: space-between;
  min-width: 100px;
}

.chat__body {
  flex: 1;
  background: url("https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png") repeat center;
  padding: 30px;
  overflow-y: auto;
  border-radius: 0 0 15px 15px;
}

.chat__message {
  position: relative;
  font-size: 16px;
  padding: 10px;
  background-color: white;
  border-radius: 10px;
  width: fit-content;
  margin-bottom: 30px;
}

.chat__name {
  position: absolute;
  top: -15px;
  font-weight: 800;
  font-size: xx-small;
}

.chat__timestamp {
  margin-left: 10px;
  font-size: xx-small;
}

.chat__receiver {
  margin-left: auto;
  background-color: #b0ffb0;
}

.chat__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100px;
  border-top: 1px solid lightgray;
}

.chat__footer > form {
  flex: 1;
  display: flex;
}

.chat__footer > form > input {
  flex: 1;
  border-radius: 30px;
  padding: 10px;
  border: none;
}

.chat__footer > form > button {
  display: none;
}

.chat__footer > md-icon {
  padding: 10px;
  color: gray;
}
</style>