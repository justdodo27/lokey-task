import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '', component: () => import('src/pages/LoginPage.vue'),
  },
  {
    path: '/', component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: 'main', component: () => import('pages/MainPage.vue') },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
