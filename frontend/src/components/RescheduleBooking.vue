<script setup>
import { ref, watch } from "vue";
import { getSlots, rescheduleBookingAPI } from "../api/api";

const props = defineProps({
  bookingUid: { type: String, required: true },
  eventTypeId: { type: Number, required: true }
});

const emit = defineEmits(["success"]);

const open = ref(false);
const date = ref("");
const slots = ref([]);
const selectedSlot = ref(null);
const loading = ref(false);
const error = ref("");

watch(date, async (d) => {
  if (!d) return;

  loading.value = true;
  error.value = "";
  selectedSlot.value = null;

  try {
    const res = await getSlots({
      eventTypeId: props.eventTypeId,
      date: d,
      bookingUidToReschedule: props.bookingUid,
    });

    slots.value = res.data.slots;
  } catch {
    error.value = "Failed to load slots";
  } finally {
    loading.value = false;
  }
});

const confirmReschedule = async () => {
  if (!selectedSlot.value) {
    error.value = "Select a time slot";
    return;
  }

  loading.value = true;

  try {
    const res = await rescheduleBookingAPI(props.bookingUid, {
      start: selectedSlot.value.start,
      reschedulingReason: "User requested reschedule",
    });

    emit("success", res.data);
    open.value = false;
  } catch (e) {
    error.value = e.response?.data?.detail || "Reschedule failed";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div style="margin-top:12px">
    <button
      @click="open = !open"
      class="book-btn"
      style="background:#f59e0b"
    >
      🔁 Reschedule Booking
    </button>

    <div v-if="open" style="margin-top:10px">
      <input type="date" v-model="date" />

      <div class="slot-grid" v-if="slots.length">
        <button
          v-for="slot in slots"
          :key="slot.start"
          class="slot-btn"
          :class="{ selected: selectedSlot?.start === slot.start }"
          @click="selectedSlot = slot"
        >
          {{ slot.start.slice(11,16) }} → {{ slot.end.slice(11,16) }}
        </button>
      </div>

      <p v-if="error" style="color:red">{{ error }}</p>

      <button
        @click="confirmReschedule"
        :disabled="loading || !selectedSlot"
        class="book-btn"
      >
        {{ loading ? "Rescheduling..." : "Confirm Reschedule" }}
      </button>
    </div>
  </div>
</template>
