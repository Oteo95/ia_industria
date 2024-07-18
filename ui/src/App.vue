<template>
  <v-app>
    <v-main>
      <v-navigation-drawer
        v-model="drawer"
        :rail="rail"
        permanent
        @click="rail = false"
        style="background-color: rgba(119, 181, 118, 0.1);"
      >
        <v-list dense>
          <v-list-item link>
            <!-- Horizontal centering for icons -->
            <v-list-item-icon class="d-flex justify-center" v-if="rail==false">
              <v-avatar :size="rail ? 20 : 30" color="red">
                <span class="white--text">{{ user_letter }}</span>
              </v-avatar>
            </v-list-item-icon>

            <!-- Horizontal centering for text content -->
            <v-list-item-content class="d-flex justify-center" v-if="rail==false">
              <v-list-item-title class="text-center">AI</v-list-item-title>
            </v-list-item-content>

            <!-- Horizontal centering for append slot (button/avatar) -->
            <template v-slot:append>
              <div class="d-flex justify-center">
                <v-avatar color="red" size="20" @click.stop="rail = !rail" v-if="rail">
                  <span class="white--text">{{ user_letter }}</span>
                </v-avatar>
                <v-btn
                  flat
                  icon="mdi-chevron-left"
                  @click.stop="rail = !rail"
                  v-if="!rail"
                  color="rgba(119, 181, 118, 0.1)"
                ></v-btn>
              </div>
            </template>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list density="compact" nav>
          <v-list-item prepend-icon="mdi-newspaper-variant-multiple-outline" title="Assistant" value="newspaper-variant-multiple-outline" @click="ActivateView('chat')"></v-list-item>
        </v-list>
      </v-navigation-drawer>
      <Chat v-if="whichView=='chat'"/>
      <MyImpact v-if="whichView=='myimpactchat'"/>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref, onMounted} from "vue";

import Chat from "./components/Chat.vue";


const user_letter = ref("")
const drawer =  ref(true);
const rail =  ref(true);
const whichView = ref("chat");  // New property to control chat visibility

function ActivateView(view: string) {
  whichView.value = view;
}

async function fetchData() {
  console.log('Component has been mounted');
}

onMounted(() => {
  console.log('Component has been mounted');
});
</script>

<style>
</style>