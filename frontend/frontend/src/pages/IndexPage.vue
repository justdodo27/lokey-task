<template>
  <q-page class="column items-center justify-start">
    <q-btn :ripple="{ center: true }" color="primary" class="q-my-lg" label="Pop-up" @click="showDialog = true"/>
    <q-table title="Articles" :rows="rows" :columns="columns" row-key="title" />
    <q-dialog v-model="showDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Choose operation to perform.</div>
        </q-card-section>
        <q-card-actions class="row items-center justify-evenly">
          <q-btn label="Create acrticle" color="primary" v-close-popup />
          <q-btn label="Refresh table" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';


export default defineComponent({
  name: 'IndexPage',
  components: {  },
  setup() {
    const rows = [
      {
        title: 'Test article 1',
        content: 'It\'s a test article!',
        release_date: new Date().toDateString()
      },
      {
        title: 'Test article 2',
        content: 'It\'s a test article but second!',
        release_date: new Date().toDateString()
      },
    ]
    const columns = [
      {
        name: 'title',
        required: true,
        label: 'Article',
        align: 'left',
        field: 'title',
        sortable: true
      },
      {
        name: 'content',
        required: true,
        label: 'Content',
        align: 'left',
        field: 'content',
        sortable: true
      },
      {
        name: 'release_date',
        required: true,
        label: 'Release Date',
        align: 'left',
        field: 'release_date',
        sortable: true
      },
    ]
    return { rows, columns, showDialog: ref(false) };
  }
});
</script>
