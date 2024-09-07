<template>
  <ul v-if="errors" class="error-messages">
    <li v-for="(error, field) in errors" :key="field">
      {{ field }}: {{ error ? error : "" }}
    </li>
  </ul>
</template>

<script setup lang="ts">
interface ErrorsProps {
  errors: Record<string, string> | undefined | null;
}

defineProps<ErrorsProps>();
</script>
