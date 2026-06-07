<template>
  <user-center :is-light-mode="globalLightMode" />
</template>

<script>
import UserCenter from '../pages/user/UserCenter.vue'

export default {
  name: 'UserCenterView',
  components: { UserCenter },
  props: {
    globalLightMode: {
      type: Boolean,
      default: false
    }
  }
}
</script>