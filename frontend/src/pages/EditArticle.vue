<template>
  <div class="container page">
    <div class="row">
      <div class="col-md-10 offset-md-1 col-xs-12">
        <form @submit.prevent="onSubmit">
          <div class="mb-3">
            <input
              v-model="form.title"
              aria-label="Title"
              type="text"
              class="form-control form-control-lg"
              placeholder="Название"
            />
          </div>
          <div class="mb-3">
            <input
              v-model="form.description"
              aria-label="Description"
              type="text"
              class="form-control form-control-lg"
              placeholder="Описание"
            />
          </div>
          <div class="mb-3">
            <textarea
              v-model="form.body"
              aria-label="Body"
              :rows="8"
              class="form-control"
              placeholder="Ваша статья (можно использовать markdown)"
            />
          </div>
          <div class="mb-3">
            <input
              v-model="newTag"
              aria-label="Tags"
              type="text"
              class="form-control"
              placeholder="Тэги"
              @change="addTag"
              @keypress.enter.prevent="addTag"
            />
            <div class="d-flex">
              <span
                v-for="tag in form.tagList"
                :key="tag"
                class="badge m-1 p-2 rounded-pill text-bg-secondary"
              >
                <ion-icon
                  name="close-circle"
                  role="button"
                  tabindex="0"
                  :aria-label="`Delete tag: ${tag}`"
                  @click="removeTag(tag)"
                  @keypress.enter="removeTag(tag)"
                ></ion-icon>
                {{ tag }}
              </span>
            </div>
          </div>
          <button
            class="btn btn-lg pull-xs-right btn-primary"
            type="submit"
            :disabled="!(form.title && form.description && form.body)"
          >
            Опубликовать
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { api } from "src/services";
import type { Article } from "src/services/api";

interface FormState {
  title: string;
  description: string;
  body: string;
  tagList: string[];
}

const route = useRoute();
const router = useRouter();
const slug = computed<string>(() => route.params.slug as string);

const form: FormState = reactive({
  title: "",
  description: "",
  body: "",
  tagList: [],
});

const newTag = ref<string>("");
function addTag() {
  form.tagList.push(newTag.value.trim());
  newTag.value = "";
}
function removeTag(tag: string) {
  form.tagList = form.tagList.filter((t) => t !== tag);
}

async function fetchArticle(slug: string) {
  const article = await api.articles
    .articlesRetrieve(slug)
    .then((res) => res.data.article);

  form.title = article.title;
  form.description = article.description;
  form.body = article.body;
  form.tagList = article.tagList;
}

onMounted(async () => {
  if (slug.value) await fetchArticle(slug.value);
});

async function onSubmit() {
  let article: Article;
  if (slug.value)
    article = await api.articles
      .articlesUpdate(slug.value, { article: form })
      .then((res) => res.data.article);
  else
    article = await api.articles
      .articlesCreate({ article: form })
      .then((res) => res.data.article);

  return router.push({ name: "article", params: { slug: article.slug } });
}
</script>
