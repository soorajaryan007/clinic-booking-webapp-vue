<script setup>
import { ref } from "vue";
import { bookSlotAPI } from "../api/api";
import EmailVerification from "../components/EmailVerification.vue";

const props = defineProps(["selectedSlot", "eventTypeId"]);
const emit = defineEmits(["result"]);

const name = ref("");
const email = ref("");
const emailVerified = ref(false);
const loading = ref(false);

const book = async () => {
  console.log("BOOK FUNCTION CALLED"); // 👈 debug proof

  if (!props.selectedSlot) {
    alert("Please select a time slot");
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
  <!-- ✅ FORM with submit handler -->
  <form @submit.prevent="book">
    <input v-model="name" placeholder="Name" />

    <EmailVerification
      v-model="email"
      @verified="emailVerified = true"
    />

    <button
      type="submit"
      class="book-btn"
      :disabled="!emailVerified || loading"
    >
      {{ loading ? "Booking..." : "Book Appointment" }}
    </button>
  </form>
</template>
