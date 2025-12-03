<template>
  <TrainingInProgress v-if="!trainingComplete"/>
  <ModelInfo v-if="trainingComplete"/>
</template>

<script>
import { io } from 'socket.io-client'
import ModelInfo from './components/ModelInfo.vue';
import TrainingInProgress from './components/TrainingInProgress.vue';

  export default {
    components: { ModelInfo, TrainingInProgress },
    data() {
      return {
        trainingComplete: false,
        socket: null
      }
    },
    mounted() {
      // Initialise Websocket Connection
      this.socket = io('http://127.0.0.1:5500')

      // Initialise Listener
      this.socket.on("trainingComplete", (key) => {
        console.log("Training Complete!")
        console.log(`Key: ${key}`)
        this.trainingComplete = key
      })

      this.socket.on('connectionTest', (msg) => {
        alert('JS function triggered by Flask: ' + msg.message);
      })
    },
    beforeUnmount() {
      // Clean up the listeners when the component is destroyed
      this.socket.off('trainingComplete')
      this.socket.off("connectionTest")
    }
  }
</script>

<style scoped>

</style>
