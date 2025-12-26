<template>
  <div style="margin-top:12px">
    <!-- Toggle button -->
    <button
      @click="open = !open"
      style="
        width:100%;
        padding:10px;
        background:#f59e0b;
        color:#fff;
        border:none;
        border-radius:8px;
      "
    >
      🔁 Reschedule Booking
    </button>

    <!-- Reschedule form -->
    <div v-if="open" style="margin-top:10px">
      <input
        type="date"
        v-model="date"
      />

      <input
        type="time"
        v-model="time"
        style="margin-top:6px"
      />

      <p
        v-if="error"
        style="color:red;margin-top:6px"
      >
        {{ error }}
      </p>

      <button
        @click="handleReschedule"
        :disabled="loading"
        style="
          margin-top:8px;
          width:100%;
          padding:10px;
          background:#2563eb;
          color:#fff;
          border:none;
          border-radius:8px;
        "
      >
        {{ loading ? "Rescheduling..." : "Confirm Reschedule" }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

/* -------- Props & Emits -------- */

const props = defineProps({
  bookingUid: {
    type: String,
    required: true
  }
});

const emit = defineEmits(["success"]);

/* -------- State -------- */

const open = ref(false);
const date = ref("");
const time = ref("");
const loading = ref(false);
const error = ref("");

/* -------- Logic -------- */

const handleReschedule = async () => {
  if (!date.value || !time.value) {
    error.value = "Select date and time";
    return;
  }

  loading.value = true;
  error.value = "";

  try {
    const start = new Date(`${date.value}T${time.value}`).toISOString();

    const res = await fetch(
      `http://localhost:8000/reschedule-booking/${props.bookingUid}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          start,
          reschedulingReason: "User requested reschedule"
        })
      }
    );

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Failed");
    }

    const data = await res.json();

    emit("success", data);
    open.value = false;
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
};
</script>
