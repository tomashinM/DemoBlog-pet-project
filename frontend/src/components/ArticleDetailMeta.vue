<template>
  <div class="d-flex align-items-center mt-4">
    <AppLink
      v-if="article.author.image"
      name="profile"
      :params="{ username: article.author.username }"
    >
      <img
        :src="article.author.image"
        :alt="article.author.username"
        class="avatar me-2"
      />
    </AppLink>

    <div>
      <AppLink name="profile" :params="{ username: article.author.username }">
        <h5 class="mb-0">
          {{ article.author.username }}
        </h5>
      </AppLink>

      <small class="text-muted">{{
        new Date(article.createdAt).toLocaleDateString()
      }}</small>
    </div>

    <button
      v-if="displayFollowButton"
      :aria-label="article.author.following ? 'Unfollow' : 'Follow'"
      class="btn btn-sm btn-outline-secondary ms-3 me-1"
      :disabled="followProcessGoing"
      @click="toggleFollow"
    >
      <ion-icon name="add"></ion-icon>
      {{ article.author.following ? "Отписаться" : "Подписаться" }}
      {{ article.author.username }}
    </button>

    <button
      :aria-label="
        article.favorited ? 'Unfavorite article' : 'Favorite article'
      "
      class="btn btn-sm mx-1"
      :class="[article.favorited ? 'btn-primary' : 'btn-outline-primary']"
      :disabled="favoriteProcessGoing"
      @click="favoriteArticle"
    >
      <ion-icon name="heart"></ion-icon>
      <span class="counter">{{ article.favoritesCount }}</span>
    </button>

    <AppLink
      v-if="displayEditButton"
      aria-label="Edit article"
      class="btn btn-outline-secondary btn-sm mx-1"
      name="edit-article"
      :params="{ slug: article.slug }"
    >
      <ion-icon name="create"></ion-icon>
      Редактировать статью
    </AppLink>

    <button
      v-if="displayEditButton"
      aria-label="Delete article"
      class="btn btn-outline-danger btn-sm mx-1"
      @click="onDelete"
    >
      <ion-icon name="trash"></ion-icon>
      Удалить статью
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed, toRefs } from "vue";
import { storeToRefs } from "pinia";
import { useFavoriteArticle } from "src/composable/useFavoriteArticle";
import { useFollow } from "src/composable/useFollowProfile";
import { routerPush } from "src/router";
import { api } from "src/services";
import type { Article, Profile } from "src/services/api";
import { useUserStore } from "src/store/user";

interface Props {
  article: Article;
}
interface Emits {
  (e: "update", article: Article): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const { article } = toRefs(props);
const { user, isAuthorized } = storeToRefs(useUserStore());
const displayEditButton = computed(
  () =>
    isAuthorized.value && user.value?.username === article.value.author.username
);
const displayFollowButton = computed(
  () =>
    isAuthorized.value && user.value?.username !== article.value.author.username
);

const { favoriteProcessGoing, favoriteArticle } = useFavoriteArticle({
  isFavorited: computed(() => article.value.favorited),
  articleSlug: computed(() => article.value.slug),
  onUpdate: (newArticle) => emit("update", newArticle),
});

async function onDelete() {
  await api.articles.articlesDestroy(article.value.slug);
  await routerPush("global-feed");
}

const { followProcessGoing, toggleFollow } = useFollow({
  following: computed(() => article.value.author.following),
  username: computed(() => article.value.author.username),
  onUpdate: (author: Profile) => {
    const newArticle = { ...article.value, author };
    emit("update", newArticle);
  },
});
</script>
