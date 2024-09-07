<template>
  <div class="comment p-4 mb-3">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <div class="d-flex align-items-center">
        <AppLink
          v-if="comment.author.image"
          name="profile"
          :params="{ username: comment.author.username }"
        >
          <img
            :src="comment.author.image"
            class="avatar me-2"
            :alt="comment.author.username"
          />
        </AppLink>
        <div>
          <AppLink
            name="profile"
            :params="{ username: comment.author.username }"
          >
            <h6 class="mb-0">{{ comment.author.username }}</h6>
          </AppLink>

          <small class="text-muted">{{
            new Date(comment.createdAt).toLocaleDateString("en-US")
          }}</small>
        </div>
      </div>
      <span>
        <ion-icon
          v-if="showRemove"
          name="trash"
          tabindex="0"
          role="button"
          aria-label="Delete comment"
          @click="emit('remove-comment')"
          @keypress.enter="emit('remove-comment')"
        ></ion-icon>
      </span>
    </div>
    <p>{{ comment.body }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { Comment } from "src/services/api";

interface Props {
  comment: Comment;
  username?: string;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: "remove-comment"): boolean;
}>();

const showRemove = computed(
  () =>
    props.username !== undefined &&
    props.username === props.comment.author.username
);
</script>
