<template>
  <div class="card my-2">
    <div class="card-body">
      <h5 class="card-title">Популярные тэги</h5>
      <div class="d-flex justify-content-around flex-wrap">
        <AppLink
          v-for="tag in tags"
          :key="tag"
          name="tag"
          :params="{ tag }"
          :aria-label="tag"
          class="badge m-1 rounded-pill text-bg-secondary flex-fill"
        >
          {{ tag }}
        </AppLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useTags } from "src/composable/useTags";

const { tags, fetchTags } = useTags();

await fetchTags();
</script>
