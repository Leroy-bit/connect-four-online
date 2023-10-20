<template>
    <div class="popup">
        <div class="popup__inner">
        <div class="popup__title">
            <slot name="title"></slot>
        </div>
        <div class="popup__buttons">
            <slot name="buttons"></slot>
        </div>
        </div>
    </div>
</template>

<style>

.popup {
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    top: 0;
    left: 0;
    z-index: 100;
    width: 100%;
    backdrop-filter: blur(1px);
    max-width:  var(--max-width);
    height: var(--tg-viewport-stable-height);
    background-color: rgba(0, 0, 0, 0.25);
}

.popup__inner {
    width: 85%;
    height: fit-content;
    background-color: var(--tg-theme-bg-color);
    opacity: 0.9;
    border-radius: 10px;
    padding: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    box-sizing: border-box;
}

.popup__title {
    margin-right: auto;
    padding: 15px;
    color: var(--tg-theme-text-color);
}

.popup__title *{
    display: inline-block;
    height: fit-content;
    color: var(--tg-theme-text-color);
    font-size: 20px;
    margin: 15px;
    margin-bottom: 25px;
}

.popup__buttons {
    display: flex;
    justify-content: space-between;
    margin-left: auto;
}

.popup__buttons *{
    display: flex;
    justify-content: center;
    padding: 15px;
    border-radius: 5px;
    color: var(--tg-theme-button-color);
}

.popup__buttons *:hover {
    background-color: rgba(85, 85, 85, 0.2);
    cursor: pointer;
}

.popup__buttons .decline {
    color: var(--decline-color);
}
</style>