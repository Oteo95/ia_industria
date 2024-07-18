<template>
    <v-speed-dial
      v-model="fab"
      bottom
      right
      :direction="'top'"
      :transition="'slide-y-reverse-transition'"
      open-on-hover
      class="fixed-bottom-right"
    >
      <v-btn
        fab
        small
        flat
        color="white"
        @click="dialog = true"
      >
        ref
        <v-icon>mdi-book-open-variant</v-icon>
      </v-btn>
    </v-speed-dial>
  
    <v-bottom-sheet v-model="dialog">
      <v-card>
        <v-card-title>
          <span class="headline">References</span>
        </v-card-title>
        <v-card-text>
          <v-data-iterator :items="references" :items-per-page="3">
            <template v-slot:default="{ items }">
                <template
                    v-for="(item, i) in items"
                    :key="item.raw.source"
                >
                    <v-list-item :href="item.raw.link" target="_blank" class="mb-2">
                            <template v-slot:title>
                            <strong class="text-h6 mb-2">{{ item.raw.source }}</strong>
                            </template>
                    </v-list-item>
                    <br>
                </template>
            </template>

            <template v-slot:footer="{ page, pageCount, prevPage, nextPage }">
                <div class="d-flex align-center justify-center pa-4">
                <v-btn
                    :disabled="page === 1"
                    density="comfortable"
                    icon="mdi-arrow-left"
                    variant="tonal"
                    rounded
                    @click="prevPage"
                ></v-btn>

                <div class="mx-2 text-caption">
                    Page {{ page }} of {{ pageCount }}
                </div>

                <v-btn
                    :disabled="page >= pageCount"
                    density="comfortable"
                    icon="mdi-arrow-right"
                    variant="tonal"
                    rounded
                    @click="nextPage"
                ></v-btn>
                </div>
            </template>
          </v-data-iterator>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-bottom-sheet>


    <v-speed-dial
        v-model="fab"
        bottom
        right
        :direction="'top'"
        :transition="'slide-y-reverse-transition'"
        open-on-hover
        class="fixed-bottom-right2"
        >
        <v-btn
            fab
            small
            flat
            color="white"
            @click="dialog2 = true"
        >
            feedback
            <v-icon>mdi-comment-quote-outline</v-icon>
        </v-btn>
      </v-speed-dial>
  
      <!-- Dialog Component -->
      <v-dialog persistent v-model="dialog2" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">Feedback</v-card-title>
        <v-card-text>
          Help us to improve the tool! Send us your comments related to our conversation.
          <!-- Feedback Buttons -->
          <div class="my-2">
            <v-btn-toggle
              v-model="toggle"
              variant="outlined"
              divided
            >
              <v-btn variant="text" icon @click="sendFeedback('positive')">
                <v-icon>mdi-thumb-up</v-icon>
              </v-btn>
              <v-btn variant="text" icon @click="sendFeedback('negative')">
                <v-icon>mdi-thumb-down</v-icon>
              </v-btn>
            </v-btn-toggle>
          </div>
          <!-- Comment Box -->
          <v-textarea
            v-model="comment"
            outlined
            label="Your comments"
            rows="1"
            auto-grow
          ></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="submitFeedback">Submit</v-btn>
          <v-btn color="red darken-1" text @click="closeFeedback">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  // Data models for dialogs and page navigation
  const dialog = ref(false);
  const dialog2 = ref(false);
  const fab = ref(false);
  const page = ref(1);
  const pageCount = ref(1); // Assuming some initial value or calculated based on `content` length
  const comment = ref("");
  const feedback = ref("");
  const toggle = ref(null);
  
  // Props definition to validate and use 'content'
  const props = defineProps({
    references: {
      type: Array,
      required: true,
      validator: (value) => {
        return value.every(item => typeof item === 'object' && !Array.isArray(item));
      }
    },
    chat_history: {
      type: Array,
      required: true,
    }
  });
  
  
  // Feedback submission methods
  function sendFeedback(type) {
      console.log("AAAAA")
      feedback.value = type; // Store feedback type ('positive' or 'negative')
      // Potentially trigger an API call here to send the feedback
  }
  
  async function submitFeedback() {
      console.log('Feedback:', feedback.value);
      console.log('Comment:', comment.value);
      console.log('chat_history:', props.chat_history);
      const payload = JSON.stringify({
        feedback: feedback.value,
        comment: comment.value,
        chat_history: props.chat_history
      });
      try {
        fetch(`https://XXXXXX/submit_feedback/`, {
          method: "POST",
          headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
          },
          body: payload
        });
      } catch (error) {
        console.error("Error fetching response:", error);
      } finally {
      }
      // Here, you would typically handle the feedback submission, e.g., sending it to a server
      dialog2.value = false; // Close the feedback dialog after submission
      feedback.value = ""
      comment.value = ""
      toggle.value = null
  }

  function closeFeedback() {
      console.log('Feedback:', feedback.value);
      console.log('Comment:', comment.value);
      // Here, you would typically handle the feedback submission, e.g., sending it to a server
      dialog2.value = false; // Close the feedback dialog after submission
      feedback.value = ""
      comment.value = ""
      toggle.value = null
  }
  </script>
  
  
  <style scoped>
  .fixed-bottom-right {
    position: sticky;
    bottom: 10px;
    left: 90vw;
    z-index: 1000;
  }

  .fixed-bottom-right2 {
    position: sticky;
    bottom: 10px;
    right: 90vw;
    z-index: 1000;
  }
  </style>
  