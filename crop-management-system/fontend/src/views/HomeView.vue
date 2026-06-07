<template>
  <home-page :username="username" :is-light-mode="globalLightMode" @logout="goLogin" />
</template>

<script>
import HomePage from '../features/home/HomePage.vue'

export default {
  name: 'HomeView',
  components: { HomePage },
  props: {
    globalLightMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      username: ''
    }
  },
  created() {
    this.username = localStorage.getItem('username') || ''
  },
  methods: {
    goLogin() {
      this.$router.push('/login')
    }
  }
}
</script>
