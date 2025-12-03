<template>
  <div class="model-metrics">
    <h1 class="model-name">{{ modelName }}</h1>
    <MetricsContainer v-for="key in metricKeys" :key="key" class="metrics-container" :percentage="metrics[key] * 100">{{ key }}</MetricsContainer>
    <ModelGraphs :image_url="auc_roc"/>
    <ModelGraphs :image_url="cmatrix"/>
    <ModelsParameter :json-content="parameters"/>
  </div>
</template>

<script>
import MetricsContainer from './MetricsContainer.vue';
import ModelGraphs from './ModelGraphs.vue';
import ModelsParameter from './ModelsParameter.vue';

export default {
  components: { MetricsContainer, ModelGraphs, ModelsParameter },
  props: {
    model: {
      type: Object,
      required: true
    },
    modelName: {
      type: String,
      required: true
    }
  },
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
      return this.$props.model["parameters.json"].content
    },

    metrics() {
      try {
        return JSON.parse(this.$props.model["test_error.json"].content);
      } catch (e) {
        console.error("Error parsing metrics JSON:", e);
        return {};
      }
    },

    metricKeys() {
      return Object.keys(this.metrics);
    },

    metricName() {
      if (this.$slots.default && this.$slots.default()) {
        const vnode = this.$slots.default()[0];
        if (vnode && vnode.children && typeof vnode.children === 'string') {
          return vnode.children.trim().toLowerCase();
        }
      }
      return '';
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
