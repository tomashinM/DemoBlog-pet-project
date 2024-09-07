<template>
  <div class="container page">
    <div class="row">
      <div class="col-md-6 offset-md-3 col-xs-12">
        <h1 class="text-xs-center">Войти</h1>
        <p class="text-xs-center">
          <AppLink name="register">Регистрация</AppLink>
        </p>

        <Errors :errors="errors" />

        <form ref="formRef" aria-label="Login form" @submit.prevent="login">
          <div class="mb-3" aria-required="true">
            <input
              v-model="form.email"
              aria-label="Email"
              class="form-control form-control-lg"
              type="email"
              required
              placeholder="Email"
            />
          </div>
          <div class="mb-3">
            <input
              v-model="form.password"
              aria-label="Password"
              class="form-control form-control-lg"
              type="password"
              required
              placeholder="Пароль"
            />
          </div>
          <button
            class="btn btn-lg btn-primary pull-xs-right"
            :disabled="!form.email || !form.password"
            type="submit"
          >
            Войти
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { routerPush } from "src/router";
import { api, isFetchError } from "src/services";
import type { LoginRequest } from "src/services/api";
import { useUserStore } from "src/store/user";
import Errors from "src/components/Errors.vue";

const formRef = ref<HTMLFormElement | null>(null);
const form: LoginRequest = reactive({
  email: "",
  password: "",
});

const { updateUser } = useUserStore();

const errors = ref();

async function login() {
  errors.value = {};

  if (!formRef.value?.checkValidity()) return;

  try {
    const result = await api.users.usersLoginCreate({ user: form });
    updateUser(result.data.user);
    await routerPush("global-feed");
  } catch (error) {
    if (isFetchError(error)) {
      errors.value = error.error?.errors;
      return;
    }
    console.error(error);
  }
}
</script>
