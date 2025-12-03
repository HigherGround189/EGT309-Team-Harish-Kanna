<template>
  <div class="training-in-progress">
    <div class="spinner-wrapper">
      <Spinner class="loading-spinner"/>
    </div>
    <h1 class="come-back-later-text">The Kedro Pipeline has not finished executing yet. <br>Come back later!</h1>
  </div>
</template>

<script>
import Spinner from './Spinner.vue';

export default {
  components: { Spinner }
};
</script>

<style scoped>
.training-in-progress{
  height: 75vh;
  width: 100%;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.spinner-wrapper {
  padding: 3rem;

  height: 80%;
}

.loading-spinner {
  aspect-ratio: 1 / 1;
  height: 100%;
}

.come-back-later-text {
  color: white;
  font-family: Arial, Helvetica, sans-serif;

  height: 20%;
  width: 100%;
  border-top: 2px hsl(0, 0%, 20%) solid;

  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}
</style>
