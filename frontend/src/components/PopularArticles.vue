<template>
  <div class="card my-2">
    <div class="card-body">
      <h5 class="card-title">ЧИТАЮТ СЕЙЧАС</h5>
      <ol>
        <li v-for="article in articles" :key="article.slug" class="mb-2">
          <div>
            <small class="text-muted">
              {{ new Date(article.createdAt).toDateString() }}
              <ion-icon name="heart"></ion-icon>
              {{ article.favoritesCount }}
            </small>
            <AppLink
              class="block hover:text-gray-300"
              name="article"
              :params="{ slug: article.slug }"
            >
              <p>{{ article.title }}</p>
            </AppLink>
          </div>
        </li>
      </ol>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import type { Article } from "src/services/api";
import { api } from "src/services";

const articles = ref<Article[]>([]);
const res = await api.articles
  .articlesList({ limit: 5, ordering: ["-favoritesCount"] })
  .then((res) => res.data);

articles.value = res.articles;
</script>
