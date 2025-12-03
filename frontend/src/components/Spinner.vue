<template>
  <div class="spinner"></div>
</template>

<script>
  export default {

  }
</script>

<style scoped>
.spinner {
  border: 20px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-left-color: hsl(153, 60%, 39%);
  animation: spin 1s ease infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
