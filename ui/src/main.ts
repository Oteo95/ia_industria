/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'
import Markdown from 'vue3-markdown-it';
import 'highlight.js/styles/monokai.css';

// Components
import App from './App.vue'
import Vue3EasyDataTable from 'vue3-easy-data-table';
import 'vue3-easy-data-table/dist/style.css';

// Composables
import { createApp } from 'vue'

const app = createApp(App)
app.component('EasyDataTable', Vue3EasyDataTable);


app.use(Markdown);

registerPlugins(app)

app.mount('#app')
