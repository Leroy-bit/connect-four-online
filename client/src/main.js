
import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import {messages} from './i18n'
import './style.css'
import App from './App.vue'

const i18n = createI18n({
    legacy: false,
    locale: window.Telegram.WebApp.initDataUnsafe.user.language_code,
    fallbackLocale: 'en',
    messages: messages
})

const app = createApp(App)
app.use(i18n)
app.mount('#app')

window.Telegram.WebApp.ready()



