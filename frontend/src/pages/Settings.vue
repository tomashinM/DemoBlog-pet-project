<template>
  <div class="container page">
    <div class="row">
      <div class="col-md-6 offset-md-3 col-xs-12">
        <h1 class="text-xs-center">Настройки</h1>

        <Errors :errors="errors" />

        <form @submit.prevent="onSubmit">
          <div class="mb-3">
            <input
              v-model="form.image"
              aria-label="Avatar picture url"
              type="text"
              class="form-control"
              placeholder="URL аватарки"
            />
          </div>
          <div class="mb-3">
            <input
              v-model="form.username"
              aria-label="Username"
              type="text"
              class="form-control form-control-lg"
              placeholder="Имя"
            />
          </div>
          <div class="mb-3">
            <textarea
              v-model="form.bio"
              aria-label="Bio"
              class="form-control form-control-lg"
              :rows="8"
              placeholder="Кратко о себе"
            />
          </div>
          <div class="mb-3">
            <input
              v-model="form.email"
              aria-label="Email"
              type="email"
              class="form-control form-control-lg"
              placeholder="Email"
            />
          </div>
          <div class="mb-3">
            <input
              v-model="form.password"
              aria-label="New password"
              type="password"
              class="form-control form-control-lg"
              placeholder="Новый пароль"
            />
          </div>
          <div class="mb-3 form-check">
            <input
              v-model="form.notifications"
              type="checkbox"
              class="form-check-input"
              id="notificationsCheck"
            />
            <label class="form-check-label" for="notificationsCheck">
              Получать уведомления
            </label>
          </div>
          <button
            class="btn btn-lg btn-primary pull-xs-right"
            :disabled="isButtonDisabled"
            type="submit"
          >
            Обновить
          </button>
        </form>

        <hr />

        <button
          class="btn btn-outline-danger"
          aria-label="Logout"
          @click="onLogout"
        >
          Выйти из аккаунта
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { routerPush } from "src/router";
import { api, isFetchError } from "src/services";
import type { PatchedUserRequest } from "src/services/api";
import { useUserStore } from "src/store/user";
import Errors from "src/components/Errors.vue";

const form: PatchedUserRequest = reactive({});

const userStore = useUserStore();
const errors = ref();

async function onSubmit() {
  errors.value = {};

  try {
    const filteredForm = Object.entries(form).reduce(
      (form, [k, v]) => (v === null ? form : Object.assign(form, { [k]: v })),
      {}
    );
    const userData = await api.user
      .userUpdate({ user: filteredForm })
      .then((res) => res.data.user);
    userStore.updateUser(userData);
    await routerPush("profile", { username: userData.username });
  } catch (error) {
    if (isFetchError(error)) errors.value = error.error?.errors;
  }
}

async function onLogout() {
  userStore.updateUser(null);
  await routerPush("global-feed");
}

onMounted(async () => {
  if (!userStore.isAuthorized) return await routerPush("login");

  form.image = userStore.user?.image;
  form.username = userStore.user?.username;
  form.bio = userStore.user?.bio;
  form.email = userStore.user?.email;
  form.notifications = userStore.user?.notifications;
});

const isButtonDisabled = computed(
  () =>
    form.image === userStore.user?.image &&
    form.username === userStore.user?.username &&
    form.bio === userStore.user?.bio &&
    form.email === userStore.user?.email &&
    form.notifications === userStore.user?.notifications &&
    !form.password
);
</script>
