<template>
  <div v-for="(files, model) in models" :key="model">
    <h2>{{ model }}</h2>
    <div v-for="(file, filename) in files" :key="filename">
      <img v-if="file.isImage" :src="file.url" :alt="filename" />
      <pre v-else>{{ file.content }}</pre>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        models: {}
      }
    },
    mounted() {
      fetch("/api/models")
        .then(res => res.json())
        .then(data => {
          const processedModels = {};
          for (const modelName in data) {
            const files = data[modelName];
            const processedFiles = {};
            for (const filename in files) {
              const url = files[filename];
              const isImage = filename.toLowerCase().endsWith('.png') || filename.toLowerCase().endsWith('.jpeg');
              processedFiles[filename] = {
                url: url,
                isImage: isImage,
                content: isImage ? null : 'Loading...'
              };
            }
            processedModels[modelName] = processedFiles;
          }
          this.models = processedModels;

          // Now fetch the content for non-image files
          for (const modelName in this.models) {
            for (const filename in this.models[modelName]) {
              const file = this.models[modelName][filename];
              if (!file.isImage) {
                fetch(file.url)
                  .then(res => res.text())
                  .then(text => {
                    file.content = text;
                  })
                  .catch(err => {
                    file.content = 'Error loading content.';
                    console.error(err);
                  });
              }
            }
          }
        });
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
</style>

