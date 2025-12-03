<template>
  <div class="model-info-wrapper">
    <CongratulationsText/>
    <div v-for="(model, modelName) in models" :key="modelName">
      <ModelMetrics :model="model" />
    </div>
  </div>
</template>

<script>
import CongratulationsText from './CongratulationsText.vue';
import ModelMetrics from './ModelMetrics.vue';

  export default {
    components: { CongratulationsText, ModelMetrics },
    data() {
      return {
        models: {},
        image_file_extensions: ["png", "jpeg", "jpg"]
      }
    },
    async mounted() { // Added async
      try {
        const res = await fetch("/api/models");
        const data = await res.json();

        const finalModels = {};

        for (const modelName in data) {
          const files = data[modelName];
          let results = {};
          let parameters = {};
          const fileContentsPromises = [];

          for (const filename in files) {
            const api_route = files[filename];
            const file_extension = filename.split('.').pop().toLowerCase();
            const isImage = this.image_file_extensions.includes(file_extension);

            if (!isImage) {
              fileContentsPromises.push(
                fetch(api_route)
                  .then(res => res.text())
                  .then(text => {
                    if (filename === 'results.json') {
                      results = JSON.parse(text);
                    } else if (filename === 'parameters.json') {
                      parameters = JSON.parse(text);
                    }
                  })
                  .catch(error => {
                    console.error(`Error fetching content for ${api_route}:`, error);
                  })
              );
            }
          }
          await Promise.all(fileContentsPromises); // Wait for all file contents of the current model

          finalModels[modelName] = {
            name: modelName,
            results: results,
            parameters: parameters
          };
        }
        this.models = finalModels;
      } catch (error) {
        console.error("Error fetching models data:", error);
      }
    }
  }
</script>

<style scoped>
  pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    background-color: #f4f4f4;
    padding: 1em;
    border-radius: 5px;
  }
  img {
    max-width: 100%;
    height: auto;
  }

  .model-info-wrapper {
    padding-block: 3rem;
    min-height: 90vh;
  }
</style>
