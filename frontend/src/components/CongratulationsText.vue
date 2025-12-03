<template>
    <div class="congratulations-text">
      <img src="@/assets/checkmark.png" class="checkmark" alt=""/>
      <h2>Training Completed!</h2>
      <p>Kedro has completed its pipelines. Here are your models' results:</p>
    </div>
</template>

<script>
  export default {

  }
</script>

<style scoped>
  .congratulations-text {
    font-family: ui-sans-serif, system-ui, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol, Noto Color Emoji;
    color: white;

    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;

    width: 100%;
    padding-bottom: 2rem;
    border-bottom: 2px hsl(0, 0%, 20%) solid;
  }

  .checkmark {
    height: 10vh;
    animation: bounce 1s infinite;
    margin-bottom: 1rem;
  }

  @keyframes bounce {
    0%, 100% {
      transform: translateY(-25%);
      animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
    }
    50% {
      transform: translateY(0);
      animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
    }
  }

  .congratulations-text > h2{
    font-size: 4rem;
    margin-bottom: 0.5rem;
  }

  .congratulations-text > p {
    font-size: 1.2rem;
  }
</style>
