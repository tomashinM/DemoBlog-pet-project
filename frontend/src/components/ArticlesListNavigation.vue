<template>
  <div class="mb-3">
    <ul class="nav nav-pills outline-active">
      <li v-for="link in links" :key="link.name" class="nav-item">
        <AppLink
          class="nav-link"
          active-class="active"
          :name="link.routeName"
          :params="link.routeParams"
        >
          <ion-icon v-if="link.icon" :name="link.icon"></ion-icon>
          {{ link.title }}
        </AppLink>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { RouteParams } from "vue-router";
import { storeToRefs } from "pinia";
import type { ArticlesType } from "src/composable/useArticles";
import type { AppRouteNames } from "src/router";
import { useUserStore } from "../store/user";

interface ArticlesListNavLink {
  name: ArticlesType;
  routeName: AppRouteNames;
  routeParams?: Partial<RouteParams>;
  title: string;
  icon?: string;
}

interface Props {
  useGlobalFeed?: boolean;
  useMyFeed?: boolean;
  useTagFeed?: boolean;
  useSearchFeed?: boolean;
  useUserFeed?: boolean;
  useUserFavorited?: boolean;
  tag: string;
  searchQuery: string;
  username: string;
}

const props = withDefaults(defineProps<Props>(), {
  useGlobalFeed: false,
  useMyFeed: false,
  useTagFeed: false,
  useSearchFeed: false,
  useUserFavorited: false,
  useUserFeed: false,
});

const allLinks = computed<ArticlesListNavLink[]>(() => [
  {
    name: "global-feed",
    routeName: "global-feed",
    title: "Последние статьи",
  },
  {
    name: "my-feed",
    routeName: "my-feed",
    title: "Подписки",
  },
  {
    name: "tag-feed",
    routeName: "tag",
    routeParams: { tag: props.tag },
    title: props.tag,
    icon: "pricetag",
  },
  {
    name: "search-feed",
    routeName: "search",
    routeParams: { searchQuery: props.searchQuery },
    title: "Поиск",
    icon: "search",
  },
  {
    name: "user-feed",
    routeName: "profile",
    routeParams: { username: props.username },
    title: "Мои статьи",
  },
  {
    name: "user-favorites-feed",
    routeName: "profile-favorites",
    routeParams: { username: props.username },
    title: "Понравившиеся",
    icon: "heart",
  },
]);

const { isAuthorized } = storeToRefs(useUserStore());

const show = computed<Record<ArticlesType, boolean>>(() => ({
  "global-feed": props.useGlobalFeed,
  "my-feed": props.useMyFeed && isAuthorized.value,
  "tag-feed": props.useTagFeed && props.tag !== "",
  "search-feed": props.useSearchFeed && props.searchQuery !== "",
  "user-feed": props.useUserFeed && props.username !== "",
  "user-favorites-feed": props.useUserFavorited && props.username !== "",
}));

const links = computed<ArticlesListNavLink[]>(() =>
  allLinks.value.filter((link) => show.value[link.name])
);
</script>
