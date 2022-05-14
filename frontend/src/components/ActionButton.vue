<template>
  <div class="rounded-full bg-primary text-white p-4 shadow-md m-2 cursor-pointer duration-300 transition-transform scale-100 active:scale-90" :class="pressed ? 'scale-90' : ''" @touchstart="pressed = true" @touchend="pressed = false"><slot></slot></div>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  setup() {
    const pressed = ref(false);
    return {
      pressed
    }
  },
})
</script>
