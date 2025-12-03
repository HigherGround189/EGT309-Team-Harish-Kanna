<template>
  <div class="model-metrics">
    <h1 class="model-name">Random Forest</h1>
    <MetricsContainer v-for="n in 5" :key="n" class="metrics-container" :percentage="n*10">Accuracy</MetricsContainer>
  </div>
</template>

<script>
import MetricsContainer from './MetricsContainer.vue';

  export default {
    components: { MetricsContainer }
  }
</script>

<style scoped>
  .model-metrics {
    display: flex;
    flex-direction: column;
    align-items: center;
    row-gap: 2rem;

    padding-block: 3rem;
  }

  .model-name {
    color: white;
    width: 60%;

    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 3rem;
  }
</style>
