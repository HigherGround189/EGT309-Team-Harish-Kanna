<template>
  <div v-for="(files, model) in models" :key="model">
    <h2>{{ model }}</h2>
    <div v-for="(file, filename) in files" :key="filename">
      <p>Api Route: {{ file.url }}</p>
      <img v-if="file.isImage" :src="file.url" :alt="filename" />
      <pre v-else>{{ file.content }}</pre>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        models: {},
        image_file_extensions: ["png", "jpeg", "jpg"]
      }
    },
    mounted() {
      fetch("/api/models")
        .then(res => res.json())
        .then(data => {

          //After fetching model data, we want to create metadata for each file, for convenience.
          // This is our goal:
          // file: {
          //   url: "/api/<model>/<filepath>"
          //   isImage: false,
          //   content: xxx
          // }
          // Acutal text content should be stored in .content.
          // However, if the file is an image, it can't have text content, so we leaeve it as null

          // Iterate through all model folders
          const processedModels = {}
          for (const modelName in data) {
            // console.log(`Model name: ${modelName}`)
            const files = data[modelName]

            // Iterate through all files inside model folder
            const processedFiles = {}
            for (const filename in files) {
              // console.log(`${modelName}'s file: ${filename}}`)

              // Get route to query backend with (eg: /api/RandomForestClassifier/parameters.json)
              const api_route = files[filename];

              // Check if file extension is inside this.image_file_extensions list.
              const file_extension = filename.split('.').pop().toLowerCase()
              const isImage = this.image_file_extensions.includes(file_extension)

              // Create hashmap containing metadata for each file
              processedFiles[filename] = {
                url: api_route,
                isImage: isImage,
                content: isImage ? null : 'Loading...' // Notice that this is empty
              };
            }

            // Add file metadata to model, eg:
            // RandomForestClassifier: {
            //   filename1: {url: xxx, isImage: false, content: null},
            //   filename12 {url: xxx, isImage: false, content: "Loading..."}
            // }
            processedModels[modelName] = processedFiles;
          }

          // Overall hashmap that will contain the hashmap of all existing models, eg:
          // processedModels: {
          //   RandomForestClassifier: {xxx},
          //   XGBoostClassifier: {xxx},
          // }
          this.models = processedModels;

          // Our goal is to populate the .content field of each file with the actual textdata
          // However, we can only update it through Vue data attributes, else the UI won't update
          // Thus we have to loop through each model to access their files
          for (const modelName in this.models) {
            // So we can loop through each file
            for (const filename in this.models[modelName]) {
              const file = this.models[modelName][filename];
              if (!file.isImage) {
                // This way, we can change each file's .content field appropriately, using fetch() to retrieve the actual data
                fetch(file.url)
                  .then(res => res.text())
                  .then(text => {
                    file.content = text;
                  })
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
