<template>
    <div class="board">
        <div class="board__column" v-for="(_, column) in columns" :key="column" :style="{'width': 100 / this.columns + '%'}" @click="makeTurn(column)">
            <div class="board__row" v-for="(_, row) in rows" :key="row">
                <div class="board__chip" v-if="this.board[column] && this.board[column].length > rows - row - 1" :class="{'my-chip': this.board[column][rows - row - 1] == 0}"></div>
            </div>
        </div>
    </div>
</template>


<style>
    .board {
        display: flex;
        width: 90%;
    }
    .board__row {
        width: 100%;
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .board, .board__row {
        border: 1px solid var(--tg-theme-hint-color);
        border-collapse: collapse;
    }
    .board__chip {
        margin: 2px;
        width: 100%;
        aspect-ratio: 1 / 1;
        border-radius: 50%;
        background-color: rgb(233, 73, 73);
        /* background-color: var(--decline-color); */
    }
    .my-chip {
        background-color: rgb(87, 218, 87);
        /* background-color: var(--accept-color); */
    }
</style>

<script>
    export default {
        data() {
            return {
                board: []
            }
        },
        created() {
            for (let i = 0; i < this.columns; i++) {
                this.board.push([])
            }
        },
        methods: {
            makeTurn(column) {
                if (this.board[column].length < this.rows) {
                    this.$emit('makeTurn', column)
                }
            },
            pushToBoard(user_id, column) {
                if (this.board[column].length < this.rows) {
                    this.board[column].push(user_id)
                }
            },
            clearBoard() {
                for (let i = 0; i < this.columns; i++) {
                    this.board[i] = []
                }
            }
        },
        inject: ['columns', 'rows']
    }

</script>