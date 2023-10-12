<template>
    <div class="screen">
        <div class="screen__content">
            <!-- <img class="screen__sticker" src="../assets/waiting-sticker.gif" alt="sticker"> -->
            <slot name="sticker"></slot>
            <div class="screen__title">
                <slot name="text"></slot>
            </div>
        </div>
    </div>
</template>

<style>
    .screen {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: var(--tg-theme-secondary-bg-color);
        width: 100%;
        height: var(--tg-viewport-stable-height);
    }
    .screen__content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 90%;
        height: 90%;
        background-color: var(--tg-theme-bg-color);
        border-radius: 15px;
    }
    .screen__title {
        font-size: 26px;
        color: var(--tg-theme-text-color);
        padding: 10px;
        max-width: 90%;
        text-align: center;
    }
    .screen__sticker {
        width: 50%;
        padding: 10px;
        -webkit-transform: rotateX(0);
        transform: rotateX(0);
    }
</style>