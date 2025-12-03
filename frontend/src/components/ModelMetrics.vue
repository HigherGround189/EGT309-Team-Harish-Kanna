<template>
  <div class="model-metrics">
    <h1 class="model-name">{{ model.name }}</h1>
    <MetricsContainer
      v-for="(value, metricName) in model.results"
      :key="metricName"
      class="metrics-container"
      :percentage="value"
      :colour="getMetricColor(metricName)"
    >
      <template v-slot:label>{{ metricName.toUpperCase() }}</template>
    </MetricsContainer>
  </div>
</template>

<script>
import MetricsContainer from './MetricsContainer.vue';

  export default {
    components: { MetricsContainer },
    props: {
      model: {
        type: Object,
        required: true
      }
    },
    methods: {
      getMetricColor(metricName) {
        const colors = {
          'accuracy': '#3b82f6', // Blue
          'precision': '#10b981', // Green
          'recall': '#f59e0b', // Amber
          'f1_score': '#ef4444' // Red
        };
        return colors[metricName.toLowerCase()] || '#6b7280'; // Default gray
      }
    }
  }
</script>

<style scoped>
  .model-metrics {
    display: flex;
    flex-direction: column;
    align-items: center;
    row-gap: 2.5rem;

    padding-block: 3rem;
  }

  .model-name {
    color: white;
    width: 60%;

    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 3rem;
  }
</style>
