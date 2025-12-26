<template>
  <div class="booking-wrapper">
    <div class="booking-layout">

      <!-- LEFT -->
      <div class="booking-card">
        <h2 class="section-title">Clinic Appointment Scheduler</h2>
        <p class="section-subtitle">
          Book a consultation with ease.
        </p>

        <EventTypeSelector @select="eventTypeId = $event" />

        <DatePicker
          v-if="eventTypeId"
          @select="date = $event"
        />

        <SlotGrid
          v-if="eventTypeId && date"
          :eventTypeId="eventTypeId"
          :date="date"
          @select="selectedSlot = $event"
        />

        <BookingForm
          v-if="selectedSlot"
          :selectedSlot="selectedSlot"
          :eventTypeId="eventTypeId"
          @result="result = $event"
        />
      </div>

      <!-- RIGHT -->
      <div class="booking-result-wrapper">
        <BookingResult
          v-if="result"
          :result="result"
        />
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import EventTypeSelector from "../components/EventTypeSelector.vue";
import DatePicker from "../components/DatePicker.vue";
import SlotGrid from "../components/SlotGrid.vue";
import BookingForm from "../components/BookingForm.vue";
import BookingResult from "../components/BookingResult.vue";

const eventTypeId = ref("");
const date = ref("");
const selectedSlot = ref(null);
const result = ref(null);
</script>
