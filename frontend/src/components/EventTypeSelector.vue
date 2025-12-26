<script setup>
import { ref, onMounted } from "vue";
import { getEventTypes } from "../api/api";

const emit = defineEmits(["select"]);
const types = ref([]);

onMounted(async () => {
  const res = await getEventTypes();
  types.value = res.data.events || [];
});
</script>

<template>
  <select @change="emit('select', $event.target.value)">
    <option value="">Select Event Type</option>
    <option v-for="t in types" :key="t.id" :value="t.id">
      {{ t.title }} ({{ t.length }} min)
    </option>
  </select>
</template>
