<template>
    <Screen v-if="isShowScreen">
        <template v-slot:text>
            {{ this.screenText }}
        </template>
        <template v-slot:sticker>
            <img v-if="stickerType=='waiting'" class="screen__sticker" src="../assets/waiting-sticker.gif">
            <img v-else-if="stickerType=='error'" class="screen__sticker" src="../assets/error-sticker.gif">
        </template>
    </Screen>

</template>

<script>
    import Screen from './Screen.vue'
    export default {
        data() {
            return {
                isShowScreen: false,
                screenText: '',
                stickerType: ''
            }
        },
        components: {
            'Screen': Screen
        },
        methods: {
            showScreen(text, stickerType) {
                console.log('[SHOW SCREEN]('+ text +')')
                this.screenText = text
                this.stickerType = stickerType
                this.isShowScreen = true
            },
            hideScreen() {
                console.log('[HIDE SCREEN]')
                this.isShowScreen = false
            }
        }
    }
</script>