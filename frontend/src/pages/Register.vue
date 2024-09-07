<template>
  <div class="container page">
    <div class="row">
      <div class="col-md-6 offset-md-3 col-xs-12">
        <h1 class="text-xs-center" v-if="success">
          Активируйте аккаунт по email
        </h1>
        <h1 class="text-xs-center">Зарегестрироваться</h1>
        <p class="text-xs-center">
          <AppLink name="login"> Войти </AppLink>
        </p>

        <Errors :errors="errors" />

        <form
          ref="formRef"
          aria-label="Registration form"
          @submit.prevent="register"
        >
          <div class="mb-3">
            <input
              v-model="form.username"
              aria-label="Username"
              class="form-control form-control-lg"
              type="text"
              required
              placeholder="Имя"
            />
          </div>
          <div class="mb-3">
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
              :minLength="8"
              required
              placeholder="Пароль"
            />
          </div>
          <button
            type="submit"
            class="btn btn-lg btn-primary pull-xs-right"
            :disabled="!(form.email && form.username && form.password)"
          >
            Зарегестрироваться
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { api, isFetchError } from "src/services";
import type { UserRequest } from "src/services/api";
import Errors from "src/components/Errors.vue";

const formRef = ref<HTMLFormElement | null>(null);
const form: UserRequest = reactive({
  username: "",
  email: "",
  password: "",
});
const success = ref();

const errors = ref();

async function register() {
  success.value = false;
  errors.value = {};

  if (!formRef.value?.checkValidity()) return;

  try {
    await api.users.usersCreate({ user: form });
    success.value = true;
    form.username = "";
    form.email = "";
    form.password = "";
  } catch (error) {
    if (isFetchError(error)) errors.value = error.error?.errors;
  }
}
</script>
