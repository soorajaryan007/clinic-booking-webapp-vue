<script setup>
import { ref } from "vue";
import { bookSlotAPI } from "../api/api";
import EmailVerification from "../components/EmailVerification.vue";

const props = defineProps({
  selectedSlot: Object,
  eventTypeId: Number,
});

const emit = defineEmits(["result"]);

const name = ref("");
const email = ref("");
const emailVerified = ref(false);
const loading = ref(false);

const book = async () => {
  console.log("BOOK FUNCTION CALLED");

  if (!props.eventTypeId) {
    alert("Please select an event type");
    return;
  }

  if (!props.selectedSlot) {
    alert("Please select a time slot");
    return;
  }

  if (!name.value.trim()) {
    alert("Please enter your name");
    return;
  }

  if (!emailVerified.value) {
    alert("Please verify your email");
    return;
  }

  loading.value = true;

  try {
    const res = await bookSlotAPI({
      event_type_id: props.eventTypeId,
      start: props.selectedSlot.start,
      end: props.selectedSlot.end,
      name: name.value,
      email: email.value,
    });

    emit("result", res.data);
  } catch (err) {
    console.error(err);
    alert("Booking failed");
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <form @submit.prevent="book" class="section-block">
    <label class="label">Name</label>
    <input v-model="name" placeholder="Your name" />

    <label class="label">Email</label>
    <EmailVerification
      v-model="email"
      @verified="emailVerified = true"
    />

    <button
      type="submit"
      class="book-btn"
      :disabled="loading || !emailVerified"
    >
      {{ loading ? "Booking..." : "Book Appointment" }}
    </button>
  </form>
</template>
