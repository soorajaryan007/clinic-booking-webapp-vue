<script setup>
import { ref, watch } from "vue";
import { getSlots } from "../api/api";

const props = defineProps({
  eventTypeId: Number,
  date: String,
});

const emit = defineEmits(["select"]);

const slots = ref([]);
const loading = ref(false);
const error = ref("");

watch(
  () => [props.eventTypeId, props.date],
  async ([eventTypeId, date]) => {
    if (!eventTypeId || !date) return;

    loading.value = true;
    error.value = "";
    slots.value = [];

    try {
      const res = await getSlots({
        eventTypeId,
        date,
      });

      slots.value = res.data.slots || [];
    } catch (err) {
      console.error(err);
      error.value = "Failed to load slots";
    } finally {
      loading.value = false;
    }
  },
  { immediate: true }
);
</script>

<template>
  <div class="section-block">
    <div v-if="loading">Loading slots...</div>

    <div v-else-if="error" style="color: red">
      {{ error }}
    </div>

    <div v-else-if="slots.length === 0">
      No slots available
    </div>

    <div class="slot-grid">
      <button
        v-for="slot in slots"
        :key="slot.start"
        @click="emit('select', slot)"
        class="slot-btn"
      >
        {{ slot.start.slice(11, 16) }} → {{ slot.end.slice(11, 16) }}
      </button>
    </div>
  </div>
</template>
