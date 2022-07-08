<template>
  <q-page class="column items-center justify-start">
    <q-btn :ripple="{ center: true }" color="primary" class="q-my-lg" label="Pop-up" @click="showDialog = true"/>
    <q-table title="Articles" :rows="rows" :columns="columns" row-key="id">
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn class="q-mr-sm" dense round color="blue" @click="editArticle(props)" icon="edit"></q-btn>
          <q-btn dense round color="red" @click="() => {showDeleteDialog = true; articleToDelete = props.row.article_id}" icon="delete"></q-btn>
        </q-td>          
      </template>
    </q-table>
    <q-dialog v-model="showDialog">
      <q-card>
        <q-card-section>
          <div class="text-h5">Choose operation to perform.</div>
        </q-card-section>
        <q-card-section>
          <div class="text-h6 text-center items-center">Filter articles by years
            <q-toggle v-model="showFilter" color="blue" />
          </div>
          <year-picker :value="filterYear" @input="e =>filterYear = e" v-show="showFilter"/>
        </q-card-section>
        <q-card-actions class="row items-center justify-evenly">
          <q-btn label="Create acrticle" @click="showCreateDialog = true" color="primary" v-close-popup />
          <q-btn label="Refresh table" @click="getArticles(true)" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="showCreateDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Create new article</div>
        </q-card-section>
        <q-card-section>
          <q-input v-model="newArticle.title" label="Title" />
          <q-input v-model="newArticle.content" label="Content" />
          <q-date v-model="newArticle.created_at" label="Release Date" />
        </q-card-section>
        <q-card-actions class="row item-center justify-center">
          <q-btn label="Create" color="primary" @click="createArticle" v-close-popup/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="showAlert">
      <q-card>
        <q-card-section>
          <div class="text-h6">Alert</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          {{ alertMsg }}
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="OK" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="showEditDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Edit Article</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input v-model="articleToEdit.title" label="Title" />
          <q-input v-model="articleToEdit.content" label="Content" />
          <q-date v-model="articleToEdit.created_at" label="Release Date" />
        </q-card-section>

        <q-card-actions align="center">
          <q-btn label="Update" color="primary" @click="updateArticle" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <q-dialog v-model="showDeleteDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Delete Article {{articleToDelete}}</div>
        </q-card-section>

        <q-card-actions align="center">
          <q-btn label="Delete" color="red" @click="deleteArticle" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script lang="ts">
import axios from 'axios';
import { defineComponent, onMounted, ref } from 'vue';
import { date } from 'quasar';
import YearPicker from '../components/YearPicker.vue';

export interface Article {
  'article_id': number;
  'title': string;
  'content': string;
  'created_at': string;
}

export interface NewArticle {
  'title': string;
  'content': string;
  'created_at': string;
}

export interface RowProps {
  'row': Article;
  'key': number;
}

type GetArticleResponse = {
  articles: Article[];
}

axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'
axios.defaults.headers.common['Authorization'] = JSON.parse(localStorage.getItem('userStoreState')).authorization
axios.defaults.headers.post['Content-Type'] = 'application/json'
axios.defaults.headers.put['Content-Type'] = 'application/json'
axios.defaults.headers.delete['Content-Type'] = 'application/json'

export default defineComponent({
  name: 'IndexPage',
  components: { YearPicker },
  setup() {
    const APIUrl = 'http://127.0.0.1:5000/api/'
    const newArticle = ref<NewArticle>({
      title: '',
      content: '',
      created_at: date.formatDate(new Date(), 'YYYY/MM/DD')
    })
    const articleToEdit = ref<Article>({
      article_id: 0,
      title: '',
      content: '',
      created_at: ''
    })
    const articleToDelete = ref<number>(0)
    const showAlert = ref(false)
    const showEditDialog = ref(false)
    const alertMsg = ref<string>('')
    const showFilter = ref(false)
    const filterYear = ref<number>(new Date().getFullYear())
    const rows = ref<Article[]>([])
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
        field: 'created_at',
        sortable: true,
        format: (val: string, row: Article) => date.formatDate(Date.parse(val), 'YYYY/MM/DD')
      },
      {
        name: 'actions',
        required: true,
        label: 'Actions',
        align: 'center',
        field: '',
        sortable: false,
      }
    ]

    async function getArticles(alert?: boolean): Promise<string | Article[]> {
      try {
        const {data, status} = await axios.get<Article[]>(`${APIUrl}articles`, showFilter.value ? { params: { year: filterYear.value } } : {})
        console.log(data)
        console.log('resposne status is: ', status)
        rows.value = data
        if (alert){
          alertMsg.value = 'Successfully refreshed table'
          showAlert.value = true
        }
        return data.articles
      } catch (error) {
        if (axios.isAxiosError(error)) {
          console.log('error message: ', error.message);
          if (alert){
          alertMsg.value = JSON.parse(error.request.response).info
          showAlert.value = true
        }
          return error.message;
        } else {
          console.log('unexpected error: ', error);
          return 'An unexpected error occurred';
        }
      }
    }

    async function createArticle(): Promise<string| Article> {
      const article = {
        title: newArticle.value.title,
        content: newArticle.value.content,
        created_at: new Date(newArticle.value.created_at).toUTCString()
      }
      try {
        const {data, status} = await axios.post<Article>(`${APIUrl}articles`, article)
        console.log(data)
        console.log('resposne status is: ', status)
        alertMsg.value = 'Successfully created new article'
        showAlert.value = true
        newArticle.value = {title: '', content: '', created_at: date.formatDate(new Date(), 'YYYY/MM/DD')}
        return data
      } catch (error) {
        if (axios.isAxiosError(error)) {
          console.log('error message: ', error.request);
          alertMsg.value = JSON.parse(error.request.response).info
          showAlert.value = true
          return error.message;
        } else {
          console.log('unexpected error: ', error);
          return 'An unexpected error occurred';
        }
      }
    }

    function editArticle(props: RowProps) {
      const formatedDate = date.formatDate(Date.parse(props.row.created_at), 'YYYY/MM/DD')
      articleToEdit.value = {
        article_id: props.row.article_id,
        title: props.row.title,
        content: props.row.content,
        created_at: formatedDate
      }
      showEditDialog.value = true
    }

    async function updateArticle() {
      const article = {
        title: articleToEdit.value.title,
        content: articleToEdit.value.content,
        created_at: new Date(articleToEdit.value.created_at).toUTCString()
      }
      console.log(article)
      try {
        const {data, status} = await axios.put<Article>(`${APIUrl}articles/${articleToEdit.value.article_id}`, article)
        console.log(data)
        console.log('response status is: ', status)
        alertMsg.value = 'Successfully updated article'
        showAlert.value = true
        return data
      } catch (error) {
        if (axios.isAxiosError(error)) {
          console.log('error message: ', error.request);
          alertMsg.value = JSON.parse(error.request.response).info
          showAlert.value = true
          return error.message;
        } else {
          console.log('unexpected error: ', error);
          return 'An unexpected error occurred';
        }
      }
    }

    async function deleteArticle() {
      try {
        const {data, status} = await axios.delete<string>(`${APIUrl}articles/${articleToDelete.value}`)
        console.log(data)
        console.log('response status is: ', status)
        alertMsg.value = 'Successfully deleted article'
        showAlert.value = true
        return data
      } catch (error) {
        if (axios.isAxiosError(error)) {
          console.log('error message: ', error.request);
          alertMsg.value = JSON.parse(error.request.response).info
          showAlert.value = true
          return error.message;
        } else {
          console.log('unexpected error: ', error);
          return 'An unexpected error occurred';
        }
      }
    }
    onMounted(() => {
      getArticles()
    })

    return { rows, columns, showDialog: ref(false), showFilter, filterYear, showCreateDialog: ref(false), showEditDialog, showAlert, alertMsg, getArticles, newArticle, createArticle, editArticle, articleToEdit, updateArticle, showDeleteDialog: ref(false), articleToDelete, deleteArticle };
  }
});
</script>
