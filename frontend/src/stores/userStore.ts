import { defineStore } from 'pinia'
import { loginEmailTokenPost, loginPost } from '../api/shop';

export type UserData = {
  user_id: number
  email: string
  first_name: string
  last_name: string
}
export type UserStoreState = {
  authorization: null | string
};

export const useUserStore = defineStore('userStore', {
  state: (): UserStoreState => {

    if (!!localStorage.userStoreState) {
      const parsedState = JSON.parse(localStorage.userStoreState) as Record<string, unknown>
      if (parsedState.authorization !== undefined) {  // do checks on localStorage object here
        return parsedState as UserStoreState
      }
    }
    return {
      authorization: null,
    }
  },
  getters: {
    isLoggedIn: (state) => (state.authorization !== null)
  },
  actions: {
    async login (email: string, password: string) {
      const response = await loginPost(email, password)
      this.authorization = response.authorization
      this.saveToLocalStorage()
    },
    async loginEmailToken (token: string) {
      const response = await loginEmailTokenPost(token)
      this.authorization = response.authorization
      this.saveToLocalStorage()
    },
    logout () {
      this.authorization = null;
      localStorage.clear()
    },
    saveToLocalStorage () {
      localStorage.userStoreState = JSON.stringify(this.$state)
    }
  }

})
