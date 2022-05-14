<template>
  <div class="relative" aria-labelledby="modal-title" role="dialog" aria-modal="true" :class="show ? 'z-30' : 'z-10 pointer-events-none'">
    <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity duration-300" :class="show ? 'opacity-100' : 'opacity-0'" @click="hide"></div>

    <div class="fixed z-30 inset-0 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-4 text-center sm:block sm:p-0">
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
        <div class="relative inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle max-w-sm w-full sm:p-6 sm:pb-4" :class="show ? 'opacity-100 translate-y-0 sm:scale-100' : 'opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95'">
          <div>
            <div class="mt-0 text-center">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">Wprowadź tagi dla tego punktu:</h3>
              <div class="mt-4">
                <input v-model="tags" type="text" name="last-name" id="last-name" autocomplete="family-name" class="max-w-lg block w-full shadow-sm focus:ring-primary focus:border-primary sm:text-sm border-gray-300 rounded-md">
              </div>
            </div>
          </div>
          <div class="mt-5 sm:mt-6">
            <button type="button" @click="save" class="inline-flex justify-center w-full rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary text-base font-medium text-white focus:outline-none">Dodaj punkt</button>
            <button type="button" @click="hide" class="inline-flex justify-center w-full px-4 pt-3 pb-2 text-base font-medium text-gray-500">Anuluj</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['show'],
  data: () => ({
    tags: ''
  }),
  methods: {
    save() {
      this.$emit('save', this.tags)
    },
    hide() {
      this.$emit('hide')
    }
  }
}
</script>
