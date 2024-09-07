<template>
  <div>
    <Suspense>
      <ArticleDetail />
      <template #fallback>
        <div class="container page">Статья загружается ...</div>
      </template>
    </Suspense>

    <Suspense>
      <div class="col-xs-12 col-md-8 offset-md-2">
        <ArticleDetailComments />
      </div>

      <template #fallback>
        <div class="container page">Комментарии загружаются ...</div>
      </template>
    </Suspense>
  </div>
</template>

<script setup lang="ts">
import ArticleDetail from "src/components/ArticleDetail.vue";
import ArticleDetailComments from "src/components/ArticleDetailComments.vue";
</script>
