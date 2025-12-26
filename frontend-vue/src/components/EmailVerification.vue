<template>
  <div>
    <!-- Email input -->
    <input
      type="email"
      v-model="email"
      :disabled="verified"
      placeholder="Enter email"
    />

    <!-- Verify button -->
    <button
      v-if="!verified && !codeSent"
      @click="sendCode"
      :disabled="loading || !email"
      class="verify-btn"
    >
      {{ loading ? "Sending..." : "Verify Email" }}
    </button>

    <!-- OTP input -->
    <div v-if="codeSent && !verified" style="margin-top:8px">
      <input
        type="text"
        v-model="code"
        placeholder="Enter OTP"
      />

      <button
        @click="confirmCode"
        :disabled="loading"
        class="confirm-btn"
      >
        {{ loading ? "Verifying..." : "Confirm OTP" }}
      </button>
    </div>

    <!-- Verified badge -->
    <p v-if="verified" style="color:#16a34a;margin-top:6px">
      ✅ Email Verified
    </p>

    <!-- Error -->
    <p v-if="error" style="color:red;font-size:12px">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import {
  requestEmailVerification,
  verifyEmailCode
} from "../api/api";

const props = defineProps({
  modelValue: String
});

const emit = defineEmits(["update:modelValue", "verified"]);

const email = ref(props.modelValue || "");
const code = ref("");
const codeSent = ref(false);
const verified = ref(false);
const loading = ref(false);
const error = ref("");

watch(email, (val) => {
  emit("update:modelValue", val);
});

const sendCode = async () => {
  loading.value = true;
  error.value = "";

  try {
    await requestEmailVerification(email.value);
    codeSent.value = true;
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
};

const confirmCode = async () => {
  loading.value = true;
  error.value = "";

  try {
    await verifyEmailCode(email.value, code.value);
    verified.value = true;
    emit("verified", true);
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.verify-btn {
  margin-top: 6px;
  padding: 8px;
  width: 100%;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
}

.confirm-btn {
  margin-top: 6px;
  padding: 8px;
  width: 100%;
  background: #22c55e;
  color: white;
  border: none;
  border-radius: 8px;
}
</style>
