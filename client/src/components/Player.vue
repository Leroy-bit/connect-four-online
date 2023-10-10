<template>
    <span class="player-name" :class="{upbar: bar_type, downbar: !bar_type, current: isCurrentPlayer}">
        <slot></slot>
    </span>
</template>

<style scoped>
    .player-name {
        color: var(--tg-theme-text-color);
        position: relative;
        display: flex;
        justify-content: center;
        font-size: 26px;
        width: 65%;
        white-space: nowrap;
    }
    .upbar::before, .downbar::after {
        content: '';
        position: absolute;
        bottom: 140%;
        display: inline-block;
        height: 7px;
        width: 85%;
        background-color: var(--tg-theme-hint-color);
        border-radius: 10px;
        transition: all 0.5s ease-out;
    }
    .downbar::after {
        top: 140%;
    }
    .current::before, .current::after {
        background-color: var(--tg-theme-link-color);
        width: 100%;
    }

</style>



<script>
    export default {
        data() {
            return {
            }
        },
        props: {
            id: Number,
            bar_type: Boolean,
            isCurrentPlayer: Boolean
        }
    }
</script>