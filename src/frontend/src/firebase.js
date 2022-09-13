import { initializeApp } from "firebase/app";
import { getDatabase, ref, push, onValue, query, orderByChild, get } from "firebase/database";

const firebaseConfig = {
  apiKey: "AIzaSyA4KhiEuU8AOrNek53Nt85ootJP_pJqPKk",
  authDomain: "real-time-chat-a939d.firebaseapp.com",
  projectId: "real-time-chat-a939d",
  storageBucket: "real-time-chat-a939d.appspot.com",
  messagingSenderId: "422976543869",
  appId: "1:422976543869:web:af3fde5bb8bdf98d4b2514",
  measurementId: "G-XXD94CRE3F"
};
// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);
export { database, ref, push, onValue, query, orderByChild, get};
