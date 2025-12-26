<script setup>
import { ref } from "vue";
import { bookSlotAPI } from "../api/api";

const props = defineProps(["selectedSlot", "eventTypeId"]);
const emit = defineEmits(["result"]);

const name = ref("");
const email = ref("");
const loading = ref(false);

const book = async () => {
  loading.value = true;
  const res = await bookSlotAPI({
    event_type_id: props.eventTypeId,
    start: props.selectedSlot.start,
    end: props.selectedSlot.end,
    name: name.value,
    email: email.value,
  });
  emit("result", res.data);
  loading.value = false;
};
</script>

<template>
  <input v-model="name" placeholder="Name" />
  <input v-model="email" placeholder="Email" />
  <button @click="book" :disabled="loading">
    {{ loading ? "Booking..." : "Book Appointment" }}
  </button>
</template>
