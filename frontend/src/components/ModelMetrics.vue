<template>
  <div class="model-metrics">
    <h1 class="model-name">Random Forest</h1>
    <p v-for="line in metrics" :key="line">{{ line }}</p>
    <MetricsContainer v-for="n in 5" :key="n" class="metrics-container" :percentage="n*10">Accuracy</MetricsContainer>
  </div>
</template>

<script>
import MetricsContainer from './MetricsContainer.vue';

  export default {
    components: { MetricsContainer },
    props: [ "model" ],
    computed: {
      auc_roc() {
        return this.$props.model["auc_roc.png"]
      },

      cmatrix() {
        return this.$props.model["cmatrix.png"]
      },

      feature_importance() {
        return this.$props.model["feature_importance.png"]
      },

      parameters() {
        return this.$props.model["parameters.json"]
      },

      metrics() {
        return JSON.stringify(this.$props.model["test_error.json"].content.split()[0])
      }
    }
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
