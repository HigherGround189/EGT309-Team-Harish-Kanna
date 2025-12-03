<template>
  <h1 class="title-text">EGT309 Team Harish Kanna</h1>

  <div class="content-wrapper">
    <TrainingInProgress v-if="!trainingComplete" />
    <ModelInfo v-if="trainingComplete" />
  </div>
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
.title-text {
  color: white;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 5.5rem;
  text-align: center;
  margin-bottom: 4vh;
  text-shadow: 0 0 5px #aaaaaa;
  user-select: none;
}

.content-wrapper {
  border: 3px hsl(0, 0%, 40%) solid;
  border-radius: 14px;
  background-color: hsl(24, 10%, 10%);
  filter: drop-shadow(0 0 0.75rem hsl(0, 0%, 35%));

  min-height: 75vh;
}
</style>
