<script setup>
import { ref, watch } from "vue";
import { getAvailability } from "../api/api";

const props = defineProps(["eventTypeId", "date"]);
const emit = defineEmits(["select"]);

const slots = ref([]);
const loading = ref(false);
const error = ref("");

watch(
  () => [props.eventTypeId, props.date],
  async () => {
    if (!props.eventTypeId || !props.date) return;
    loading.value = true;
    try {
      const res = await getAvailability({
        event_type_id: props.eventTypeId,
        date: props.date,
      });
      slots.value = res.data.slots || [];
    } catch {
      error.value = "Failed to load slots";
    } finally {
      loading.value = false;
    }
  },
  { immediate: true }
);
</script>

<template>
  <div>
    <div v-if="loading">Loading slots...</div>
    <div v-else-if="slots.length === 0">No slots available</div>

    <button
      v-for="slot in slots"
      :key="slot.start"
      @click="emit('select', slot)"
      class="slot-btn"
    >
      {{ slot.start.slice(11,16) }} → {{ slot.end.slice(11,16) }}
    </button>
  </div>
</template>
