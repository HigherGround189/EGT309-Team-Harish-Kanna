<template>
  <div v-for="(file_paths, model) in models" :key="model">
    <h1>{{ model }}</h1>
    <div v-for="file in file_paths" :key="file">
      <p>{{ file }}</p>
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
    // Fetch model data from flask
      fetch("/api/models")
      .then(res => res.json())
      .then(data => {
        this.models = data;
      });
    }
  }
</script>

<style scoped>

</style>
