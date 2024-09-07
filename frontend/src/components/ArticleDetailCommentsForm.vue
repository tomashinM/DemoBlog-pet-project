<template>
  <p v-if="!profile">
    <AppLink name="login"> Войти </AppLink> или
    <AppLink name="register"> Зарегестрироваться </AppLink> чтобы оставлять
    комментарии.
  </p>
  <form v-else class="card comment-form" @submit.prevent="submitComment">
    <div class="card-block">
      <textarea
        v-model="comment"
        aria-label="Write comment"
        class="form-control"
        placeholder="Ваш комментарий..."
        :rows="3"
      />
    </div>
    <div class="card-footer">
      <img
        v-if="profile.image"
        :src="profile.image"
        class="avatar"
        :alt="profile.username"
      />
      <button
        aria-label="Submit"
        type="submit"
        :disabled="comment === ''"
        class="btn btn-sm btn-primary"
      >
        Отправить
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { storeToRefs } from "pinia";
import { useProfile } from "src/composable/useProfile";
import { api } from "src/services";
import type { Comment } from "src/services/api";
import { useUserStore } from "src/store/user";

interface Props {
  articleSlug: string;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: "addComment", comment: Comment): void;
}>();

const { user } = storeToRefs(useUserStore());

const username = computed(() => user.value?.username ?? "");
const { profile } = useProfile({ username });

const comment = ref("");

async function submitComment() {
  const newComment = await api.articles
    .articlesCommentsCreate(props.articleSlug, {
      comment: { body: comment.value },
    })
    .then((res) => res.data.comment);
  emit("addComment", newComment);
  comment.value = "";
}
</script>
