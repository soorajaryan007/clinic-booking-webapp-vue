<script setup>
import { ref, onMounted } from "vue";
import { getEventTypes } from "../api/api";

const emit = defineEmits(["select"]);

const types = ref([]);
const loading = ref(false);
const error = ref("");

onMounted(async () => {
  loading.value = true;
  error.value = "";

  try {
    const res = await getEventTypes();
    types.value = res.data.events || [];
  } catch (err) {
    console.error(err);
    error.value = "Failed to load event types";
  } finally {
    loading.value = false;
  }
});

const onChange = (e) => {
  const value = e.target.value;
  emit("select", value ? Number(value) : null);
};
</script>

<template>
  <div class="section-block">
    <label class="label">Event Type</label>

    <div v-if="loading">Loading event types...</div>

    <div v-else-if="error" style="color:red">
      {{ error }}
    </div>

    <select v-else @change="onChange">
      <option value="">Select Event Type</option>
      <option
        v-for="t in types"
        :key="t.id"
        :value="t.id"
      >
        {{ t.title }} ({{ t.length }} min)
      </option>
    </select>
  </div>
</template>
