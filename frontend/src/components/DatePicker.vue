<script setup>
const emit = defineEmits(["select"]);
</script>

<template>
  <input type="date" @change="emit('select', $event.target.value)" />
</template>
