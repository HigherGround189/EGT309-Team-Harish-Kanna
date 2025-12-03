<template>
  <div class="card-container">
    <div class="card-header">
      <span class="card-label">
        <slot></slot>
      </span>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
        class="trend-icon"
      >
        <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
        <polyline points="17 6 23 6 23 12"></polyline>
      </svg>
    </div>

    <div class="card-value">
      {{ formattedPercentage }}%
    </div>

    <div
      class="progress-track"
      role="progressbar"
      :aria-valuenow="percentage"
      aria-valuemin="0"
      aria-valuemax="100"
    >
      <div
        class="progress-fill"
        :style="{ width: percentage + '%', backgroundColor: colour }"
      ></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AccuracyCard',
  props: {
    percentage: {
      type: Number,
      required: true,
      default: 0
    },
    colour: {
      type: String,
      default: '#3b82f6'
    }
  },
  computed: {
    formattedPercentage() {
      return this.percentage.toFixed(2);
    }
  }
}
</script>

<style scoped>
.card-container {
  background-color: hsla(196, 87%, 15%, 0.178);
  border: 1px solid #2b3648;
  border-radius: 12px;
  padding: 24px;
  width: 60%;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.card-label {
  color: #94a3b8;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.trend-icon {
  width: 18px;
  height: 18px;
  color: #94a3b8;
}

.card-value {
  color: #ffffff;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 16px;
  line-height: 1.1;
}

/* Progress Bar Container (Track) */
.progress-track {
  width: 100%;
  height: 8px;
  background-color: #2b3648;
  border-radius: 99px;
  overflow: hidden;
}

/* Progress Bar Indicator (Fill) */
.progress-fill {
  height: 100%;
  background-color: #3b82f6;
  border-radius: 99px;
  transition: width 0.5s ease-out;
}
</style>
