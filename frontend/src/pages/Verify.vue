<template>
  <div class="container page">
    <Errors :errors="errors" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { routerPush } from "src/router";
import { api, isFetchError } from "src/services";
import Errors from "src/components/Errors.vue";

const route = useRoute();
const uuid = route.params.uuid as string;
const errors = ref();

onMounted(async () => {
  await verifyAccount();
});

async function verifyAccount() {
  errors.value = {};
  try {
    await api.users.usersVerifyRetrieve(uuid);
    await routerPush("login");
  } catch (error) {
    if (isFetchError(error)) errors.value = error.error?.errors;
  }
}
</script>
