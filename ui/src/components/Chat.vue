<template>

  <v-container
    style="height: auto; min-height: 80vh"
  >
    <v-row v-if="messages.length > 0" style="width: 70vw" class="fixed-bottom-chat">
      <v-col cols="8">
        <div ref="messagesContainer" id="messages-container">
          <div v-for="(msg, index) in messages" :key="index" class="d-flex">
            <div v-if="msg.role === 'user'" class="user-icon">
              {{ user_letter }}
            </div>
            <img v-else :src="msg.role === 'system' ? robotImage : userImage" alt="Profile Image" class="mr-4 message-icon">
            <v-card :key="index" class="mb-4" :variant="msg.role === 'system' ? 'outlined' : 'flat'">
              <v-card-text class="custom-card-text">
                <Markdown :source="msg.content" />
                <div v-if="index === messages.length - 1 && asyncState.isLoading" class="text-center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                </div>
              </v-card-text>
              <ExpandableComponent 
               v-if="msg.role === 'system' && index === messages.length - 1 && asyncState.isLoading===false && conversationHistory && expandableBoxContent.length > 0"
               :references="expandableBoxContent"
               :chat_history="conversationHistory"
              />
            </v-card>
          </div>
        </div>
      </v-col>
    </v-row>


    <v-row
      v-if="messages.length === 0"
      class="fixed-bottom-exam"
    >
      <v-spacer></v-spacer>
      <v-card
        :key="index"
        class="ma-4"
        variant="tonal"
        color="primary"
        @click="handleSubmitTemplatePrompt('Build a python game')"
      >
        <v-card-text>Build a python game</v-card-text>
      </v-card>
      <v-card
        :key="index"
        class="ma-4"
        variant="tonal"
        color="primary"
        @click="handleSubmitTemplatePrompt('What is fire?')"
      >
        <v-card-text>What is fire?</v-card-text>
      </v-card>
      <v-card
        :key="index"
        class="ma-4"
        variant="tonal"
        color="primary"
        @click="handleSubmitTemplatePrompt('Which is the most clever AI?')"
      >
        <v-card-text>Which is the most clever AI?</v-card-text>
      </v-card>
      <v-spacer></v-spacer>
    </v-row>

    <v-row class="fixed-bottom">
      <v-col cols="12">
        <v-textarea
          v-model="message"
          label="Enter your message"
          variant="outlined"
          @click:append="sendMessage"
          @keydown.enter.prevent="sendMessage"
          single-line
          rows="2"
          no-resize
        >
          <template v-slot:append>
            <v-btn
              @click="sendMessage"
              :disabled="asyncState.isLoading"
              icon="mdi-send"
              variant="plain"
            ></v-btn>
          </template>
        </v-textarea>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>

import { ref, watch, nextTick, reactive, onMounted} from "vue";
import Markdown from 'vue3-markdown-it';
import robotImage from '@/assets/logo.png';  // Adjust the path according to your project structure
import userImage from '@/assets/logo.png';
import ExpandableComponent from "./ExpandableComponent.vue";


const messagesContainer = ref(null);
const message = ref("");
const messages = ref([]);
const conversationHistory = ref([]); // Store conversation history
const asyncState = reactive({ isLoading: false, error: null });
const user_letter = ref("X");
const expandableBoxContent = ref([{"source":"", "link":""}]);

const openAIKey = import.meta.env.VITE_APP_OPENAI_KEY;

async function fetchOpenAIResponse(userMessage) {
  const copyOfUserMessage = userMessage;
  asyncState.isLoading = true;
  const currentMessageIndex = messages.value.length;
  messages.value.push({ role: "system", content: "" });
  
  const last_interactions = messages.value.slice(0, -2);
  console.log("INTERACTIONS",last_interactions)
  // Store user message in history
  conversationHistory.value.push({ role: "user", message: copyOfUserMessage });

  // Create the payload for the POST request
  const payload = JSON.stringify({
    user_message: userMessage,
    chat_history: last_interactions.map(msg => ({ role: msg.role, content: msg.content }))
  });
  console.log("PAYLOAD", payload)
  try {
    const response = await fetch(`xxxxxxxx`, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: payload
    });

    const data = await response.json();
    if (data && data.response) {
      console.log("Response received: ", data.response)
      console.log("MESSAGES 2:", messages.value[currentMessageIndex])
      messages.value[currentMessageIndex].content += data.response;
      // Store system response in history
      conversationHistory.value.push({ role: "system", message: data.response });
      expandableBoxContent.value = data.reference;
    }
  } catch (error) {
    messages.value[currentMessageIndex].content = "Error: " + error.message;
    conversationHistory.value.push({ role: "system", message: "Error: " + error.message });
    expandableBoxContent.value = [{"source":"", "link":""}];
    console.error("Error fetching OpenAI response:", error);
    return "Sorry, I couldn't process that.";
  } finally {
    asyncState.isLoading = false;
  }
}

async function sendMessage() {
  if (asyncState.isLoading) return;
  if (message.value.trim()) {
    messages.value.push({ role: "user", content: message.value });
    const userInput = message.value;
    message.value = ""; // Clear the input field

    const LlmResponse = await fetchOpenAIResponse(userInput);
    // Ensures the DOM updates with the new message before scrolling
    nextTick(() => {
      scrollToBottom();  // Ensures scrolling happens after the DOM updates
    });
  }
}

// Function to scroll to the bottom of the messages container
function scrollToBottom() {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: 'smooth'  // Optional: Adds an animation effect to the scroll
  });
}

const handleSubmitTemplatePrompt = (template) => {
  message.value = template;
  sendMessage();
};

watch(messages, () => {
  nextTick(() => {
    scrollToBottom();  // Scroll after Vue has updated the DOM following changes to messages
  });
}, { deep: true });


onMounted(() => {
  console.log('Component has been mounted');
});
</script>

<style>
#messages-container {
  overflow-y: auto; /* Allows for scrolling within the container itself */
  margin-bottom: 100px; /* Adjust this value to the height of your input area */
  margin-top: 10vh; /* Adjust this value to the height of your input area */
}


.text-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Adding left padding to the message text inside the card */
#messages-container .v-card-text {
  padding-left: 1.2rem; /* Adjust the padding as needed */
}

.message-card .custom-card-text {
  padding-left: 1.2rem;
}

.message-icon {
  width: 30px;
  height: 32px;
}

/* Adjust size on smaller screens */
@media (max-width: 600px) {
  .message-icon {
    width: 20px;
    height: 22px;
  }
}

.user-icon {
  width: 30px;    /* Set the width to match the images */
  height: 32px;   /* Set the height to match the images */
  background-color: red; /* Set background color to red */
  color: white; /* Set text color to white */
  display: flex;
  justify-content: center; /* Center content horizontally */
  align-items: center; /* Center content vertically */
  font-size: 16px; /* Set a suitable font size */
  font-weight: bold; /* Make the letter bold */
}

.fixed-bottom {
  position: fixed;
  width: 60%;
  bottom: 0;
  left: 50%;            /* Center the element relative to the container */
  transform: translateX(-50%); /* Move it left by half its own width */
  z-index: 1000;        /* Higher than other content */
  background-color: white; /* Ensure it's visible against any background */
  border-top: 1px solid #e0e0e0; /* Optional: adds a subtle line at the top of the row */
}

.fixed-bottom-chat {
  position: sticky;
  top: 50%;             /* Position the top edge of the element at the middle of the screen vertically */
  left: 50%; 
  z-index: 600;        /* Higher than other content */
  background-color: white; /* Ensure it's visible against any background */
}

.fixed-bottom-exam {
  position: fixed;
  bottom: 0;
  padding-bottom: 15vh;
  left: 31vw;            /* Center the element relative to the container */
  z-index: 600;        /* Higher than other content */
  background-color: white; /* Ensure it's visible against any background */
}

body, html {
  height: 100%; /* Full height to manage overflow properly */
  margin: 0;
  padding: 0;
}

.content-area {
  padding-bottom: 70px; /* Adjust this value based on the actual height of your fixed row */
}
.drawer-style .v-navigation-drawer {
  padding: 0;
}

.drawer-style .v-list-item {
  width: 100%;
}

.drawer-style .v-list-item-icon, .drawer-style .v-list-item-content, .drawer-style [v-slot="append"] {
  flex-grow: 1;
}
.fixed-bottom-right {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}
</style>
