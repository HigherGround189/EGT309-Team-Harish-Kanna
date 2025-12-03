<template>
  <div class="training-in-progress">
    <div class="spinner-wrapper">
      <Spinner class="loading-spinner"/>
    </div>
    <h1 class="come-back-later-text">The Kedro Pipeline has not completed yet. Come back later!</h1>
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
  height: 100%;
  width: 100%;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  border: 3px red solid;
}

.spinner-wrapper {
  background-color: orange;
  padding: 3rem;

  height: 80%;
}

.loading-spinner {
  aspect-ratio: 1 / 1;
  width: 25vw;
}

.come-back-later-text {
  color: white;
  font-family: Arial, Helvetica, sans-serif;

  height: 20%;
}
</style>
