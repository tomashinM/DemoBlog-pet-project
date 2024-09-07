<template>
  <div class="container mt-4">
    <div class="row">
      <main class="col-md-8">
        <Suspense>
          <ArticlesList
            use-global-feed
            use-my-feed
            use-tag-feed
            use-search-feed
          />
          <template #fallback> Загрузка... </template>
        </Suspense>
      </main>

      <aside class="col-md-4">
        <div class="input-group mb-3">
          <input
            type="text"
            class="form-control"
            placeholder="Поиск"
            aria-label="SearchField"
            v-model="searchQuery"
            @keyup.enter="search"
          />
          <button
            class="btn btn-outline-secondary"
            type="submit"
            @click="search"
          >
            <ion-icon name="search"></ion-icon>
          </button>
        </div>
        <Suspense>
          <PopularTags />
          <template #fallback> Загрузка тэгов... </template>
        </Suspense>
        <Suspense>
          <PopularArticles />
          <template #fallback> Загрузка топа... </template>
        </Suspense>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
import ArticlesList from "src/components/ArticlesList.vue";
import PopularTags from "src/components/PopularTags.vue";
import PopularArticles from "src/components/PopularArticles.vue";
import { ref } from "vue";
import { routerPush } from "src/router";

const searchQuery = ref<string>("");
async function search() {
  const query = searchQuery.value.trim();
  if (query) {
    await routerPush("search", { searchQuery: query });
  }
}
</script>
