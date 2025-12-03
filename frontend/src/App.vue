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
        trainingComplete: null,
        socket: null
      }
    },
    async mounted() {
      // Initialise Websocket Connection
      this.socket = io('http://127.0.0.1:5500')

      // Fetch data from /training-status to get initial status
      fetch("/api/training-status")
        .then(res => res.json())
        .then(data => {
          this.trainingComplete = data["Training status"] === "ongoing" ? false : true
        })

      // Initialise Listener for trainingComplete event
      this.socket.on("trainingComplete", (data) => {
        console.log("Training Complete!")
        console.log(`Data: ${data.key}`)
        this.trainingComplete = (data.key === 'completed')
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
