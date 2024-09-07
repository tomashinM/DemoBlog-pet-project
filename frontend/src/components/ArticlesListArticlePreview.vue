<template>
  <article class="post p-3 mb-3">
    <div class="d-flex align-items-center mb-2">
      <AppLink
        name="profile"
        v-if="article.author.image"
        :params="{ username: props.article.author.username }"
      >
        <img
          class="avatar me-2"
          :src="article.author.image"
          :alt="props.article.author.username"
        />
      </AppLink>
      <div>
        <AppLink
          name="profile"
          :params="{ username: props.article.author.username }"
        >
          <h5 class="mb-0">{{ article.author.username }}</h5>
        </AppLink>
        <small class="text-muted">{{
          new Date(article.createdAt).toDateString()
        }}</small>
      </div>
      <button
        :aria-label="
          article.favorited ? 'Unfavorite article' : 'Favorite article'
        "
        class="btn btn-sm ms-auto"
        :class="[article.favorited ? 'btn-primary' : 'btn-outline-primary']"
        :disabled="favoriteProcessGoing"
        @click="() => favoriteArticle()"
      >
        <ion-icon name="heart"></ion-icon> {{ article.favoritesCount }}
      </button>
    </div>
    <AppLink name="article" :params="{ slug: props.article.slug }">
      <h3>{{ article.title }}</h3>
    </AppLink>

    <p>{{ article.description }}</p>

    <AppLink
      name="article"
      :params="{ slug: props.article.slug }"
      class="btn btn-outline-secondary btn-sm"
    >
      Читать дальше...
    </AppLink>
    <ul class="d-flex flex-wrap m-0 p-0">
      <li
        v-for="tag in article.tagList"
        :key="tag"
        class="badge m-1 p-2 rounded-pill text-bg-secondary"
      >
        {{ tag }}
      </li>
    </ul>
  </article>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useFavoriteArticle } from "src/composable/useFavoriteArticle";
import type { Article } from "src/services/api";

interface Props {
  article: Article;
}
interface Emits {
  (e: "update", article: Article): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const { favoriteProcessGoing, favoriteArticle } = useFavoriteArticle({
  isFavorited: computed(() => props.article.favorited),
  articleSlug: computed(() => props.article.slug),
  onUpdate: (newArticle: Article): void => emit("update", newArticle),
});
</script>
