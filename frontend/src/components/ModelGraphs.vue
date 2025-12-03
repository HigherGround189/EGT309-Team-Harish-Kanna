<template>
  <div>
    <img :src="image_url.url" alt=""/>
  </div>
</template>

<script>
  export default {
    props: [ "image_url" ]
  }
</script>

<style scoped>

</style>
