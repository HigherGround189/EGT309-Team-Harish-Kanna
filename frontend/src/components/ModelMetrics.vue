<template>


  <div class="model-metrics">
    <MetricsContainer v-for="n in 5" :key="n" class="metrics-container" :percentage="n*10"/>
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
  }
</style>
