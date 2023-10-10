<template>
    <div class="waiting-screen">
        <div class="waiting-screen__content">
            <img class="waiting-screen__sticker" src="../assets/waiting-sticker.gif" alt="sticker">
            <div class="waiting-screen__title">Waiting for opponent</div>
        </div>
    </div>
</template>

<style scoped>
    .waiting-screen {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: var(--tg-theme-secondary-bg-color);
        width: 100%;
        height: var(--tg-viewport-stable-height);
    }
    .waiting-screen__content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 90%;
        height: 90%;
        background-color: var(--tg-theme-bg-color);
        border-radius: 15px;
    }
    .waiting-screen__title {
        font-size: 26px;
        color: var(--tg-theme-text-color);
        padding: 10px;
    }
    .waiting-screen__sticker {
        width: 50%;
        padding: 10px;
        -webkit-transform: rotateX(0);
        transform: rotateX(0);
    }
</style>