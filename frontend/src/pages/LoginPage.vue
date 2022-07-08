<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex bg-image flex-center">
        <q-card
          v-bind:style="$q.screen.lt.sm ? { width: '80%' } : { width: '30%' }"
          style="border-radius: 1vh"
        >
          <q-card-section>
            <q-avatar size="103px" class="absolute-center shadow-7">
              <img src="profile.svg" />
            </q-avatar>
          </q-card-section>
          <q-card-section>
            <div class="text-center q-pt-lg">
              <div class="col text-h6 ellipsis q-mt-sm">Zaloguj</div>
            </div>
          </q-card-section>
          <q-card-section>
            <q-form class="q-gutter-md">
              <q-input
                for="login"
                v-model="username"
                label="Nazwa uzytkownika"
                lazy-rules
                outlined
              />

              <q-input
                for="password"
                type="password"
                v-model="password"
                label="Hasło"
                outlined
              />
              <span class="text-negative">{{ errorMsg }}</span>

              <div class="row justify-end q-mt-lg q-mb-sm">
                <q-btn
                  id="log_in"
                  label="Zaloguj"
                  type="button"
                  color="grey-6"
                  no-caps
                  class="justify-center items-center"
                  @click="sendLogin"
                  style="height: 5vh"
                />
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import router from 'src/router';
import { ref } from 'vue';
import { useUserStore } from '../stores/userStore';

const userStore = useUserStore();
const username = ref<string>('');
const password = ref<string>('');

const isLoading = ref(false);
const errorMsg = ref('');

const sendLogin = () => {
  isLoading.value = true;
  userStore
    .login(username.value, password.value)
    .then(() => {
      console.log('LOGGED ID');
      router.replace('/main');
    })
    .catch(() => {
      errorMsg.value =
        'This email and password combination didnt work, try again.';
    })
    .finally(() => {
      isLoading.value = false;
    });
};
</script>

<style>
.bg-image {
  background-image: linear-gradient(135deg, #005041 0%, #00baae 150%);
}
body .q-input {
  border-radius: 1vh;
}
</style>
