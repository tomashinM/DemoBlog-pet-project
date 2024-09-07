<template>
  <div>
    <div class="container banner">
      <div class="row">
        <div class="col-xs-12 col-md-10 offset-md-1">
          <div v-if="!profile">Загрузка профиля...</div>
          <template v-else>
            <img
              v-if="profile.image"
              :src="profile.image"
              class="avatar"
              :alt="profile.username"
            />

            <h4>{{ profile.username }}</h4>

            <p v-if="profile.bio">
              {{ profile.bio }}
            </p>

            <AppLink
              v-if="showEdit"
              class="btn btn-sm btn-outline-secondary action-btn"
              name="settings"
              aria-label="Edit profile settings"
            >
              <ion-icon name="settings"></ion-icon>
              Изменить профиль
            </AppLink>

            <button
              v-if="showEdit"
              class="btn btn-sm btn-outline-danger ms-2"
              aria-label="Logout"
              @click="onLogout"
            >
              <ion-icon name="exit"></ion-icon>
              Выйти из аккаунта
            </button>

            <button
              v-if="showFollow"
              class="btn btn-sm btn-outline-secondary action-btn"
              :disabled="followProcessGoing"
              @click="toggleFollow"
            >
              <ion-icon name="add"></ion-icon>
              {{ profile.following ? "Отписаться от" : "Подписаться на" }}
              {{ profile.username }}
            </button>
          </template>
        </div>
      </div>
    </div>

    <div class="container">
      <div class="row">
        <div class="col-xs-12 col-md-10 offset-md-1">
          <Suspense>
            <ArticlesList use-user-feed use-user-favorited />
            <template #fallback> Загрузка... </template>
          </Suspense>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { storeToRefs } from "pinia";
import { routerPush } from "src/router";
import ArticlesList from "src/components/ArticlesList.vue";
import { useFollow } from "src/composable/useFollowProfile";
import { useProfile } from "src/composable/useProfile";
import type { Profile } from "src/services/api";
import { useUserStore } from "src/store/user";

const route = useRoute();
const username = computed<string>(() => route.params.username as string);

const { profile, updateProfile } = useProfile({ username });

const { followProcessGoing, toggleFollow } = useFollow({
  following: computed<boolean>(() => profile.value?.following ?? false),
  username,
  onUpdate: (newProfileData: Profile) => updateProfile(newProfileData),
});

const userStore = useUserStore();

const { user, isAuthorized } = storeToRefs(userStore);

const showEdit = computed<boolean>(
  () => isAuthorized && user.value?.username === username.value
);
const showFollow = computed<boolean>(
  () => user.value?.username !== username.value
);

async function onLogout() {
  userStore.updateUser(null);
  await routerPush("global-feed");
}
</script>
