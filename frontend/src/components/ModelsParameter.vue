<template>
  <pre v-if="highlightedCode"><code class="language-json" v-html="highlightedCode"></code></pre>
</template>

<script>
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css';
import 'prismjs/components/prism-json';

export default {
  props: {
    jsonContent: {
      type: String,
      required: true,
      default: '{}'
    }
  },
  computed: {
    formattedJson() {
      const parsed = JSON.parse(this.jsonContent);
      return JSON.stringify(parsed, null, 2);
    },
    highlightedCode() {
      if (!this.jsonContent || this.jsonContent === 'Loading...') {
        return null;
      }
      return Prism.highlight(this.formattedJson, Prism.languages.json, 'json');
    }
  }
}
</script>

<style scoped>
pre {
  border-radius: 12px;
  padding: 24px;
  background-color: hsla(196, 87%, 15%, 0.178);
  border: 1px solid #2b3648;
  width: 60%;
  margin-inline: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
