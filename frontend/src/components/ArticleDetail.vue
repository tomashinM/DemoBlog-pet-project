<template>
  <div class="banner">
    <div class="container">
      <h1 class="display-4">{{ article.title }}</h1>

      <ArticleDetailMeta
        v-if="article"
        :article="article"
        @update="updateArticle"
      />
    </div>
  </div>

  <div class="container my-4">
    <div id="article-content" v-html="articleHandledBody" />

    <ul class="d-flex m-0 p-0">
      <li
        v-for="tag in article.tagList"
        :key="tag"
        class="badge m-1 p-2 rounded-pill text-bg-secondary"
      >
        {{ tag }}
      </li>
    </ul>

    <hr />
    <ArticleDetailMeta
      v-if="article"
      :article="article"
      @update="updateArticle"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, reactive } from "vue";
import { useRoute } from "vue-router";
import marked from "src/plugins/marked";
import { api } from "src/services";
import type { Article } from "src/services/api";
import ArticleDetailMeta from "./ArticleDetailMeta.vue";

const route = useRoute();
const slug = route.params.slug as string;
const article: Article = reactive(
  await api.articles.articlesRetrieve(slug).then((res) => res.data.article)
);

const articleHandledBody = computed(() => marked(article.body));

function updateArticle(newArticle: Article) {
  Object.assign(article, newArticle);
}
</script>
