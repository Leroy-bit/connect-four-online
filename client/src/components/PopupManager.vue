<template>
    <Popup v-if="showPopup">
        <template v-slot:title>
            {{ popupTitle }}
        </template>
        <template v-slot:buttons>
            <div :class="{decline: !button.type}" v-for="button in popupButtons" :key="button.id" @click="onButtonClick(button.id)">{{ button.text }}</div>
        </template>
    </Popup>

</template>

<script>
    import Popup from './Popup.vue'
    export default {
        data() {
            return {
                showPopup: false,
                popupTitle: '',
                popupButtons: [],
            }
        },
        components: {
            'Popup': Popup
        },
        methods: {
            openPopup(title, buttons) {
                console.log('[OPEN POPUP]('+ title +')' + JSON.stringify(buttons))
                this.popupTitle = title
                this.popupButtons = buttons
                this.showPopup = true
            },
            closePopup() {
                console.log('[CLOSE POPUP]')
                this.showPopup = false
            },
            onButtonClick(id) {
                this.$emit('popupButtonClicked', id)
            }
        }
    }
</script>