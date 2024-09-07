<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
    <div class="container">
      <AppLink class="navbar-brand logo" name="global-feed">
        Demo Blog
      </AppLink>
      <button
        class="navbar-toggler"
        type="button"
        @click="toggleNavbar"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        :class="[
          'collapse',
          'navbar-collapse',
          'justify-content-end',
          { show: isNavbarOpen },
        ]"
        id="navbarNav"
      >
        <ul class="navbar-nav">
          <li v-for="link in navLinks" :key="link.name" class="nav-item">
            <AppLink
              class="nav-link"
              active-class="active"
              :name="link.name"
              :params="link.params"
              :aria-label="link.title"
              @click="closeNavbar"
            >
              <ion-icon v-if="link.icon" :name="link.icon"></ion-icon>
              {{ link.title }}
            </AppLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import type { RouteParams } from "vue-router";
import { storeToRefs } from "pinia";
import type { AppRouteNames } from "src/router";
import { useUserStore } from "src/store/user";

interface NavLink {
  name: AppRouteNames;
  params?: Partial<RouteParams>;
  title: string;
  icon?: string;
  display: "all" | "anonym" | "authorized";
}

const { user } = storeToRefs(useUserStore());

const username = computed(() => user.value?.username);
const displayStatus = computed(() =>
  username.value ? "authorized" : "anonym"
);

const isNavbarOpen = ref(false);

const toggleNavbar = () => {
  isNavbarOpen.value = !isNavbarOpen.value;
};

const closeNavbar = () => {
  isNavbarOpen.value = false;
};

const allNavLinks = computed<NavLink[]>(() => [
  {
    name: "global-feed",
    title: "Главная",
    display: "all",
  },
  {
    name: "login",
    title: "Войти",
    display: "anonym",
    icon: "person",
  },
  {
    name: "register",
    title: "Регистрация",
    display: "anonym",
    icon: "person-add",
  },
  {
    name: "create-article",
    title: "Новая статья",
    display: "authorized",
    icon: "create",
  },
  {
    name: "settings",
    title: "Настройки",
    display: "authorized",
    icon: "settings",
  },
  {
    name: "profile",
    params: { username: username.value },
    title: username.value || "",
    display: "authorized",
    icon: "person",
  },
]);

const navLinks = computed(() =>
  allNavLinks.value.filter(
    (l) => l.display === displayStatus.value || l.display === "all"
  )
);
</script>
