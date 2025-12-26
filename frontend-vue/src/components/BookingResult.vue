<template>
  <!-- ❌ No result -->
  <div v-if="!result"></div>

  <!-- 🚫 Cancelled UI (HIGHEST PRIORITY) -->
  <div
    v-else-if="cancelled"
    class="booking-result cancelled"
  >
    <h3>Booking Cancelled ❌</h3>
    <p>Your appointment has been cancelled.</p>
  </div>

  <!-- ❌ Booking failed -->
  <div
    v-else-if="result.status !== 'success'"
    class="booking-result error"
  >
    <h3 style="color:#dc2626">Booking Failed ❌</h3>

    <p style="margin-top:8px;color:#374151">
      {{ errorMessage }}
    </p>

    <p
      v-if="errorCode"
      style="font-size:12px;color:#6b7280;margin-top:6px"
    >
      Error code: <strong>{{ errorCode }}</strong>
    </p>

    <p
      style="font-size:12px;color:#9ca3af;margin-top:12px"
    >
      Please select a different date or try again later.
    </p>
  </div>

  <!-- ✅ Success UI -->
  <div
    v-else
    class="booking-result success"
  >
    <h3>Booking Confirmed ✔</h3>

    <p style="font-size:12px;color:#888">
      Booking UID: {{ bookingUid }}
    </p>

    <p><strong>Patient:</strong> {{ name }}</p>
    <p><strong>Email:</strong> {{ email }}</p>
    <p><strong>Date:</strong> {{ date }}</p>
    <p><strong>Time:</strong> {{ start }}</p>
    <p><strong>Ends:</strong> {{ end }}</p>

    <!-- 🔁 RESCHEDULE COMPONENT -->
    <RescheduleBooking
      :bookingUid="bookingUid"
      @success="onRescheduleSuccess"
    />

    <!-- ❌ Cancel button with countdown -->
    <button
      v-if="secondsLeft > 0"
      @click="handleCancel"
      :disabled="loading"
      style="
        margin-top:14px;
        padding:10px;
        width:100%;
        background:#ef4444;
        color:#fff;
        border:none;
        border-radius:8px;
        cursor:pointer;
      "
    >
      {{ loading
        ? 'Cancelling...'
        : `Cancel Booking (${secondsLeft}s)`
      }}
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from "vue";
import { cancelBookingAPI } from "../api/api";
import RescheduleBooking from "./RescheduleBooking.vue";

const props = defineProps({
  result: {
    type: Object,
    required: true
  }
});

/* -------- Error handling -------- */

const errorMessage = computed(() =>
  props.result?.message ||
  props.result?.cal_response?.error?.message ||
  "Unable to complete booking. Please try again."
);

const errorCode = computed(() =>
  props.result?.cal_response?.error?.code || null
);

/* -------- Booking data -------- */

const bookingUid = computed(() => props.result.booking_uid);
const name = computed(() => props.result.name || "N/A");
const email = computed(() => props.result.email || "N/A");
const date = computed(() => props.result.start?.slice(0, 10) || "N/A");
const start = computed(() => props.result.start?.slice(11, 16) || "N/A");
const end = computed(() => props.result.end?.slice(11, 16) || "N/A");

/* -------- State -------- */

const secondsLeft = ref(30);
const cancelled = ref(false);
const loading = ref(false);

let timer = null;

/* ⏱ Countdown timer */
const startTimer = () => {
  clearInterval(timer);
  secondsLeft.value = 30;

  timer = setInterval(() => {
    if (secondsLeft.value > 0) {
      secondsLeft.value--;
    }
  }, 1000);
};

onMounted(startTimer);

onBeforeUnmount(() => {
  clearInterval(timer);
});

/* 🔄 Reset when new booking result arrives */
watch(
  () => props.result,
  () => {
    cancelled.value = false;
    loading.value = false;
    startTimer();
  }
);

/* ❌ Cancel booking */
const handleCancel = async () => {
  if (!bookingUid.value) return;

  loading.value = true;
  try {
    await cancelBookingAPI(bookingUid.value);
    cancelled.value = true;
    clearInterval(timer); // ✅ stop timer
  } catch (err) {
    alert("Failed to cancel booking");
  } finally {
    loading.value = false;
  }
};

/* 🔁 Reschedule success */
const onRescheduleSuccess = (data) => {
  alert("Booking rescheduled successfully");
  console.log("Rescheduled:", data);
};
</script>
