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
      {{ formattedPercentage }}
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
        :style="{ width: (percentage * 100) + '%', backgroundColor: backgroundColor }"
      ></div>
    </div>
  </div>
</template>

<script>
const metricColorMap = {
  accuracy: 'oklch(63.7% 0.237 25.331)', // Green
  precision: 'oklch(76.9% 0.188 70.08)', // Blue
  recall: 'oklch(72.3% 0.219 149.579)', // Amber
  f1_score: 'oklch(70.4% 0.14 182.503)', // Pink
  micro_f1_score: 'oklch(68.5% 0.169 237.323)', // Orange
  macro_f1_score: 'oklch(58.5% 0.233 277.117)', // Cyan
  weighted_f1_score: 'oklch(62.7% 0.265 303.9)', // Light Green
  auc_roc: 'oklch(74% 0.238 322.16)' // Purple
};

export default {
  name: 'AccuracyCard',
  props: {
    percentage: {
      type: Number,
      required: true,
      default: 0
    }
  },
  computed: {
    formattedPercentage() {
      return this.percentage.toFixed(2);
    },
    metricName() {
      if (this.$slots.default && this.$slots.default()) {
        const vnode = this.$slots.default()[0];
        if (vnode && vnode.children && typeof vnode.children === 'string') {
          return vnode.children.trim().toLowerCase();
        }
      }
      return '';
    },
    backgroundColor() {
      return metricColorMap[this.metricName] || '#3b82f6';
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
  color: #94a3b8; /* Muted text color */
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.trend-icon {
  width: 18px;
  height: 18px;
  color: #94a3b8; /* Matches label color */
}

.card-value {
  color: #ffffff;
  font-size: 2.5rem; /* Large text size */
  font-weight: 700;
  margin-bottom: 16px;
  line-height: 1.1;
}

/* Progress Bar Container (Track) */
.progress-track {
  width: 100%;
  height: 8px;
  background-color: #2b3648; /* Darker track color */
  border-radius: 99px; /* Pill shape */
  overflow: hidden; /* Ensures the fill doesn't bleed out */
}

/* Progress Bar Indicator (Fill) */
.progress-fill {
  height: 100%;
  background-color: #3b82f6; /* Bright Blue */
  border-radius: 99px;
  /* Smooth transition if the number updates */
  transition: width 0.5s ease-out;
}
</style>
