<template>
    <div class="row items-center justify-center q-my-sm">
        <q-btn dense round @click="() => { year--; $emit('input', year) }" icon="chevron_left" />
        <div color="primary" class="q-mx-md text-center">{{year}}</div>
        <q-btn dense round @click="() => { year++; $emit('input', year) }" icon="chevron_right" />
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
    props: {
        'value': {'type':Number, 'required': true},
        'show': Boolean
    },
    setup(props) {
        const year = ref<number>(props.value)
        return { year }
    },
})
</script>
